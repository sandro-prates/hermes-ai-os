from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github/workflows/publish-container.yml"
CHECKOUT_SHA = "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"

LOGIN_STATE_FILE = "${{ runner.temp }}/hermes-ghcr-login-state"
DIGEST_STATE_FILE = "${{ runner.temp }}/hermes-published-digests"
LOGIN_STATE_STEPS = {
    "Authenticate to GHCR with GITHUB_TOKEN",
    "Logout defensively after every login attempt",
}
DIGEST_STATE_STEPS = {
    "Push exactly once and capture the final manifest digest",
    "Inspect registry digest and verify private linked package",
    "Remove tag, pull exclusively by digest, and validate RepoDigest",
    "Smoke the pulled digest with console logging",
    "Smoke the pulled digest with JSON logging",
}


def raw() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def workflow() -> dict[str, Any]:
    loaded = yaml.load(raw(), Loader=yaml.BaseLoader)
    assert isinstance(loaded, dict)
    return loaded


def job(name: str) -> dict[str, Any]:
    return workflow()["jobs"][name]


def commands(name: str) -> str:
    return "\n".join(str(step.get("run", "")) for step in job(name)["steps"])


def test_yaml_is_valid_and_name_is_exact() -> None:
    assert workflow()["name"] == "Publish Container"


def test_trigger_is_exclusively_workflow_dispatch_with_required_inputs() -> None:
    triggers = workflow()["on"]
    assert set(triggers) == {"workflow_dispatch"}
    inputs = triggers["workflow_dispatch"]["inputs"]
    assert set(inputs) == {"expected_sha", "confirm_external_publication"}
    assert inputs["expected_sha"]["required"] == "true"
    assert inputs["expected_sha"]["type"] == "string"
    assert inputs["confirm_external_publication"] == {
        "description": "Confirm that this run may publish externally to private GHCR",
        "required": "true",
        "type": "boolean",
        "default": "false",
    }


def test_global_and_job_permissions_are_exact() -> None:
    assert workflow()["permissions"] == {}
    assert job("verify-gates")["permissions"] == {"actions": "read", "contents": "read"}
    assert job("publish-container")["permissions"] == {"contents": "read", "packages": "write"}
    for forbidden in (
        "contents: write",
        "actions: write",
        "deployments: write",
        "attestations: write",
        "id-token: write",
        "read-all",
        "write-all",
    ):
        assert forbidden not in raw().lower()


def test_jobs_are_exact_and_publication_depends_on_gates() -> None:
    assert set(workflow()["jobs"]) == {"verify-gates", "publish-container"}
    assert job("publish-container")["needs"] == "verify-gates"
    assert "publication_authorized == 'true'" in job("publish-container")["if"]


def test_dispatch_guard_requires_main_exact_full_sha_and_human_confirmation() -> None:
    text = commands("verify-gates")
    assert "refs/heads/main" in text
    assert 'r"[0-9a-f]{40}"' in text
    assert 'CURRENT_SHA"] != expected' in text
    assert "CONFIRM_EXTERNAL_PUBLICATION" in text
    assert '!= "true"' in text


def test_both_independent_push_gates_are_bound_to_expected_sha() -> None:
    text = commands("verify-gates")
    assert 'approved_run("quality-gate.yml")' in text
    assert 'approved_run("container-gate.yml")' in text
    for fragment in (
        'run.get("head_sha") == expected',
        'run.get("head_branch") == "main"',
        'run.get("event") == "push"',
        'run.get("status") == "completed"',
        'run.get("conclusion") == "success"',
    ):
        assert fragment in text
    assert set(job("verify-gates")["outputs"]) == {
        "expected_sha",
        "quality_gate_run_id",
        "container_gate_run_id",
        "publication_authorized",
    }


def test_checkout_uses_approved_full_pin_sha_ref_and_no_credentials() -> None:
    checkout = next(
        step
        for step in job("publish-container")["steps"]
        if "actions/checkout@" in step.get("uses", "")
    )
    assert checkout["uses"] == f"actions/checkout@{CHECKOUT_SHA}"
    assert checkout["with"] == {"ref": "${{ inputs.expected_sha }}", "persist-credentials": "false"}
    assert "# v7.0.0" in raw()


def test_authentication_uses_github_token_and_never_pat() -> None:
    text = raw()
    assert "github.token" in text
    assert "--password-stdin" in text
    assert not re.search(r"\bPAT\b", text, re.IGNORECASE)
    assert "secrets." not in text


def test_two_authenticated_preflights_are_ordered_around_build() -> None:
    names = [step["name"] for step in job("publish-container")["steps"]]
    first = names.index("Authenticated registry preflight before build")
    build = names.index("Build one local linux amd64 image with required OCI labels")
    second = names.index("Authenticated registry preflight immediately before push")
    push = names.index("Push exactly once and capture the final manifest digest")
    assert first < build < second < push
    assert commands("publish-container").count("TAG_CONFIRMED_ABSENT=SIM") == 2


@pytest.mark.parametrize(
    "fragment",
    [
        "unauthorized",
        "forbidden",
        "timeout",
        "network",
        "tls",
        "rate limit",
        "registry",
        "empty",
        "invalid json",
        "http",
        "ambiguous 404",
        "manifest_unknown",
    ],
)
def test_preflight_fail_closed_taxonomy_is_explicit(fragment: str) -> None:
    assert fragment in commands("publish-container").lower()


def test_existing_tag_is_a_hard_stop_and_manifest_inspect_is_not_canonical() -> None:
    text = commands("publish-container").lower()
    assert "tag exists" in text or "tag already exists" in text
    assert "overwrite and rebuild forbidden" in text
    assert "docker manifest inspect" not in text


def test_full_sha_tag_policy_and_no_floating_tag() -> None:
    assert "IMAGE_TAG: sha-${{ needs.verify-gates.outputs.expected_sha }}" in raw()
    assert not re.search(r"(?i)(?:^|[\s:/])latest(?:$|[\s'\"])", raw())
    assert "short_sha" not in raw().lower()


def test_build_is_single_platform_local_and_has_required_oci_labels() -> None:
    text = commands("publish-container")
    assert "docker build --no-cache --pull=false --platform linux/amd64" in text
    assert "buildx" not in text.lower()
    assert "qemu" not in text.lower()
    for label in (
        "org.opencontainers.image.source",
        "org.opencontainers.image.revision",
        "org.opencontainers.image.version",
        "org.opencontainers.image.title",
    ):
        assert label in text


def test_exactly_one_push_and_anchored_final_digest() -> None:
    text = commands("publish-container")
    assert len(re.findall(r"(?m)^docker push |^\s*docker push ", text)) == 1
    assert "^${IMAGE_TAG}: digest: (sha256:[0-9a-f]{64}) size: [0-9]+$" in text


def test_triple_digest_validation_and_canonical_pull() -> None:
    text = commands("publish-container")
    for name in (
        "PUSH_REPORTED_MANIFEST_DIGEST",
        "REGISTRY_INSPECTED_MANIFEST_DIGEST",
        "PULLED_IMAGE_REPODIGEST",
    ):
        assert name in text
    assert "Docker-Content-Digest" in text
    assert "sha256:[0-9a-f]{64}" in text
    assert 'canonical="$IMAGE_NAME@$REGISTRY_INSPECTED_MANIFEST_DIGEST"' in text
    assert 'docker pull "$canonical"' in text


def test_repodigest_uses_explicit_image_prefix_and_bash_parameter_expansion() -> None:
    script = publication_step(
        "Remove tag, pull exclusively by digest, and validate RepoDigest"
    )["run"]
    assert "{{index .RepoDigests 0}}" in script
    assert "{{range .RepoDigests}}" not in script
    assert 'repo_digest_prefix="${IMAGE_NAME}@sha256:"' in script
    assert '[[ "$repo_digest_entry" == "$repo_digest_prefix"* ]]' in script
    assert 'repo_digest=${repo_digest_entry#"${IMAGE_NAME}@"}' in script
    assert not re.search(r"docker image inspect[^\n]*\|\s*sed\b", script)


def test_repodigest_rejects_other_repository_or_missing_sha256_prefix() -> None:
    script = publication_step(
        "Remove tag, pull exclusively by digest, and validate RepoDigest"
    )["run"]
    prefix_check = script.index(
        '[[ "$repo_digest_entry" == "$repo_digest_prefix"* ]]'
    )
    extraction = script.index('repo_digest=${repo_digest_entry#"${IMAGE_NAME}@"}')
    digest_check = script.index('[[ "$repo_digest" =~ $digest_pattern ]]')
    assert prefix_check < extraction < digest_check
    assert 'repo_digest_prefix="${IMAGE_NAME}@sha256:"' in script
    assert "digest_pattern='^sha256:[0-9a-f]{64}$'" in script


def test_repodigest_is_compared_with_both_reported_digests_before_smoke() -> None:
    steps = job("publish-container")["steps"]
    validation_index = next(
        index
        for index, step in enumerate(steps)
        if step["name"]
        == "Remove tag, pull exclusively by digest, and validate RepoDigest"
    )
    script = steps[validation_index]["run"]
    assert (
        'test "$PUSH_REPORTED_MANIFEST_DIGEST" = '
        '"$REGISTRY_INSPECTED_MANIFEST_DIGEST"'
    ) in script
    assert (
        'test "$REGISTRY_INSPECTED_MANIFEST_DIGEST" = "$repo_digest"'
    ) in script
    smoke_names = {
        "Smoke the pulled digest with console logging",
        "Smoke the pulled digest with JSON logging",
    }
    assert all(
        validation_index < index
        for index, step in enumerate(steps)
        if step["name"] in smoke_names
    )


def test_post_publication_private_visibility_and_repository_link_are_required() -> None:
    text = commands("publish-container")
    assert "api.github.com/users/sandro-prates/packages/container/hermes-ai-os" in text
    assert 'package.get("visibility") != "private"' in text
    assert 'repository.get("full_name") != "sandro-prates/hermes-ai-os"' in text
    assert "ACTUAL_PACKAGE_VISIBILITY=private" in text
    assert "PACKAGE_LINKED_REPOSITORY=sandro-prates/hermes-ai-os" in text


@pytest.mark.parametrize(
    "fragment",
    [
        "linux",
        "amd64",
        "Python 3.14.6",
        "10001:10001",
        "--read-only",
        "Health.Status",
        "http://127.0.0.1:18000/",
        "/api/v1/health",
        "x-request-id",
        "generated",
        "preserved",
        "LOG_FORMAT=console",
        "LOG_FORMAT=json",
        "pytest",
        "ruff",
        "httpx",
        "uv",
        "/app/tests",
        "/app/docs",
    ],
)
def test_runtime_smoke_contract_is_complete_and_digest_only(fragment: str) -> None:
    text = commands("publish-container")
    assert fragment in text
    smoke = (
        text[text.index("Smoke the pulled digest with console logging") :]
        if "Smoke the pulled digest with console logging" in text
        else text
    )
    assert "@$REGISTRY_INSPECTED_MANIFEST_DIGEST" in smoke


def test_console_smoke_captures_complete_logs_before_fail_closed_assertion() -> None:
    script = publication_step("Smoke the pulled digest with console logging")["run"]
    capture = 'docker logs "$container" >"$log_file" 2>&1'
    display = 'cat "$log_file"'
    assertion = "grep -Fq 'request_id' \"$log_file\""
    assert capture in script
    assert script.index(capture) < script.rindex(display) < script.index(assertion)
    assert 'logs_status=$?' in script
    assert 'exit "$logs_status"' in script
    assert not re.search(
        r"docker logs[^\n]*\|\s*(?:grep(?:\s+[^\n|]*)?\s+-q|head|sed\b)",
        script,
    )
    assert "|| true" not in script[script.index(capture) : script.index(assertion)]


def test_httpx_absence_probe_is_quiet_and_requires_no_production_dependency() -> None:
    script = publication_step("Smoke the pulled digest with console logging")["run"]
    assert 'importlib.util.find_spec(\\"httpx\\")' in script
    assert 'import httpx' not in script
    assert "pip install" not in script


def test_both_smokes_capture_logs_and_json_remains_after_console() -> None:
    steps = job("publish-container")["steps"]
    names = [step["name"] for step in steps]
    console_name = "Smoke the pulled digest with console logging"
    json_name = "Smoke the pulled digest with JSON logging"
    assert names.index(console_name) < names.index(json_name)
    for name, required in ((console_name, "request_id"), (json_name, '\"request_id\"')):
        script = publication_step(name)["run"]
        assert 'docker logs "$container" >"$log_file" 2>&1' in script
        assert 'cat "$log_file"' in script
        assert f"grep -Fq '{required}' \"$log_file\"" in script
        assert 'exit "$logs_status"' in script


def test_logout_is_always_and_tracks_three_states() -> None:
    logout = next(
        step for step in job("publish-container")["steps"] if "Logout defensively" in step["name"]
    )
    assert logout["if"] == "always()"
    text = commands("publish-container")
    for state in (
        "LOGIN_STATE=NOT_ATTEMPTED",
        "LOGIN_STATE=ATTEMPTED_NOT_CONFIRMED",
        "LOGIN_STATE=SUCCEEDED",
    ):
        assert state in text
    assert "docker logout ghcr.io" in logout["run"]


def test_no_git_writes_or_out_of_scope_capabilities() -> None:
    text = raw().lower()
    assert not re.search(
        r"\bgit\s+(add|commit|push|reset|rebase|pull|merge|tag|checkout|restore|clean)\b",
        commands("publish-container").lower(),
    )
    for forbidden in (
        "deployment",
        "docker-compose",
        "docker compose",
        "attestation",
        "sbom",
        "cosign",
        "signing",
        "id-token",
    ):
        assert forbidden not in text

def test_runner_context_is_absent_from_job_level_env() -> None:
    for job_definition in workflow()["jobs"].values():
        environment = job_definition.get("env", {})
        assert all("${{ runner." not in str(value) for value in environment.values())

    publication_environment = job("publish-container")["env"]
    assert "LOGIN_STATE_FILE" not in publication_environment
    assert "DIGEST_STATE_FILE" not in publication_environment


def test_login_state_file_uses_runner_temp_only_in_authorized_steps() -> None:
    steps = job("publish-container")["steps"]
    actual = {
        step["name"]
        for step in steps
        if step.get("env", {}).get("LOGIN_STATE_FILE") == LOGIN_STATE_FILE
    }
    assert actual == LOGIN_STATE_STEPS

    for step in steps:
        environment = step.get("env", {})
        if step["name"] in LOGIN_STATE_STEPS:
            assert environment["LOGIN_STATE_FILE"] == LOGIN_STATE_FILE
        else:
            assert "LOGIN_STATE_FILE" not in environment


def test_digest_state_file_uses_runner_temp_only_in_authorized_steps() -> None:
    steps = job("publish-container")["steps"]
    actual = {
        step["name"]
        for step in steps
        if step.get("env", {}).get("DIGEST_STATE_FILE") == DIGEST_STATE_FILE
    }
    assert actual == DIGEST_STATE_STEPS

    for step in steps:
        environment = step.get("env", {})
        if step["name"] in DIGEST_STATE_STEPS:
            assert environment["DIGEST_STATE_FILE"] == DIGEST_STATE_FILE
        else:
            assert "DIGEST_STATE_FILE" not in environment


def test_runner_context_scope_is_explicitly_limited_to_step_env() -> None:
    runner_expressions: list[tuple[str, str, str]] = []
    for job_name, job_definition in workflow()["jobs"].items():
        for key, value in job_definition.get("env", {}).items():
            if "${{ runner." in str(value):
                runner_expressions.append((job_name, f"job.env.{key}", str(value)))
        for step in job_definition["steps"]:
            for key, value in step.get("env", {}).items():
                if "${{ runner." in str(value):
                    runner_expressions.append(
                        (job_name, f"step.env.{step['name']}.{key}", str(value))
                    )

    expected = {
        *{
            ("publish-container", f"step.env.{name}.LOGIN_STATE_FILE", LOGIN_STATE_FILE)
            for name in LOGIN_STATE_STEPS
        },
        *{
            ("publish-container", f"step.env.{name}.DIGEST_STATE_FILE", DIGEST_STATE_FILE)
            for name in DIGEST_STATE_STEPS
        },
    }
    assert set(runner_expressions) == expected
    assert raw().count("${{ runner.") == len(expected)


def test_context_scope_repair_adds_no_action_or_install_dependency() -> None:
    action_uses = [
        step["uses"]
        for job_definition in workflow()["jobs"].values()
        for step in job_definition["steps"]
        if "uses" in step
    ]
    assert action_uses == [f"actions/checkout@{CHECKOUT_SHA}"]
    assert not re.search(
        r"(?m)^\s*(?:python\s+-m\s+)?pip\s+install\b",
        commands("publish-container"),
    )

PRIVATE_PACKAGE_PREFLIGHT_STEP = "Verify preconfigured private GHCR package"
PRIVATE_PACKAGE_POST_PUSH_STEP = (
    "Inspect registry digest and verify private linked package"
)


def publication_step(name: str) -> dict:
    matches = [
        step
        for step in job("publish-container")["steps"]
        if step["name"] == name
    ]
    assert len(matches) == 1
    return matches[0]


def test_private_package_preflight_precedes_login_build_and_push() -> None:
    names = [step["name"] for step in job("publish-container")["steps"]]
    assert names.index(PRIVATE_PACKAGE_PREFLIGHT_STEP) < names.index(
        "Authenticate to GHCR with GITHUB_TOKEN"
    )
    assert names.index(PRIVATE_PACKAGE_PREFLIGHT_STEP) < names.index(
        "Build one local linux amd64 image with required OCI labels"
    )
    assert names.index(PRIVATE_PACKAGE_PREFLIGHT_STEP) < names.index(
        "Push exactly once and capture the final manifest digest"
    )
    step = publication_step(PRIVATE_PACKAGE_PREFLIGHT_STEP)
    assert step["env"] == {"GH_TOKEN": "${{ github.token }}"}
    assert "docker " not in step["run"]


def test_private_package_preflight_requires_complete_metadata() -> None:
    script = publication_step(PRIVATE_PACKAGE_PREFLIGHT_STEP)["run"]
    for required in (
        "PACKAGE_API",
        "VERSIONS_API",
        "package metadata visibility is absent",
        "package metadata visibility is not private",
        "package repository metadata is absent",
        "package repository link is not the expected repository",
        "package versions are absent",
        "package version metadata is absent",
        "package version tags field is absent",
        "preconfigured package has no probe tag",
        "PACKAGE_EXISTS=SIM",
        "PACKAGE_METADATA_VISIBILITY=private",
        "PACKAGE_REPOSITORY_LINK=",
        "PRIVATE_PACKAGE_PREFLIGHT=APPROVED",
    ):
        assert required in script
    for blocking_status in (401, 403, 404, 429):
        assert f"{blocking_status}:" in script
    for blocking_failure in (
        "empty response",
        "invalid JSON",
        "URLError",
        "TimeoutError",
        "socket.timeout",
        "ssl.SSLError",
    ):
        assert blocking_failure in script


def test_anonymous_probe_follows_registry_v2_bearer_flow() -> None:
    for name in (
        PRIVATE_PACKAGE_PREFLIGHT_STEP,
        PRIVATE_PACKAGE_POST_PUSH_STEP,
    ):
        script = publication_step(name)["run"]
        for required in (
            "WWW-Authenticate",
            "Bearer",
            "realm",
            "service",
            "scope",
            "repository:{IMAGE_REPOSITORY}:pull",
            "https://ghcr.io/v2/{IMAGE_REPOSITORY}/tags/list",
            "https://ghcr.io/v2/{IMAGE_REPOSITORY}/manifests/{probe_tag}",
            "token_url",
            "anonymous_bearer",
            "ANONYMOUS_PULL_TOKEN_GRANTED=NAO",
            "ANONYMOUS_TAG_LIST_ACCESS=DENIED",
            "ANONYMOUS_MANIFEST_ACCESS=DENIED",
        ):
            assert required in script
        assert "initial_status != 401" in script
        assert "tags_status" in script
        assert "manifest_status" in script
        assert "anonymous content access allowed" in script


def test_initial_registry_challenge_is_not_private_evidence() -> None:
    script = publication_step(PRIVATE_PACKAGE_PREFLIGHT_STEP)["run"]
    challenge_index = script.index("initial_status != 401")
    token_index = script.index("token_url")
    tags_index = script.index("tags_status")
    manifest_index = script.index("manifest_status")
    approval_index = script.index("PRIVATE_PACKAGE_PREFLIGHT=APPROVED")
    assert challenge_index < token_index < tags_index < manifest_index
    assert manifest_index < approval_index


def test_workflow_has_no_bootstrap_or_package_mutation_mode() -> None:
    text = raw()
    dispatch = workflow()["on"]["workflow_dispatch"]
    assert set(dispatch["inputs"]) == {
        "expected_sha",
        "confirm_external_publication",
    }
    assert not re.search(r"(?i)\bpat\b|personal access token", text)
    assert "secrets." not in text
    assert not re.search(
        r'method\s*=\s*["\'](?:POST|PATCH|PUT|DELETE)["\']',
        text,
    )
    for forbidden in (
        "delete package",
        "delete tag",
        "change visibility",
        "set visibility",
        "bootstrap mode",
        "workflow rerun",
        "gh run rerun",
    ):
        assert forbidden not in text.lower()


def test_normal_publication_uses_only_github_token() -> None:
    token_values = []
    for job_definition in workflow()["jobs"].values():
        for step in job_definition["steps"]:
            environment = step.get("env", {})
            for key in ("GH_TOKEN", "GHCR_TOKEN"):
                if key in environment:
                    token_values.append(environment[key])
    assert token_values
    assert set(token_values) == {"${{ github.token }}"}


def test_post_push_repeats_private_and_anonymous_denial_checks() -> None:
    script = publication_step(PRIVATE_PACKAGE_POST_PUSH_STEP)["run"]
    for required in (
        "verified_package_metadata()",
        "verify_anonymous_access_denied(image_tag)",
        "PACKAGE_METADATA_VISIBILITY=private",
        "PACKAGE_REPOSITORY_LINK=",
        "ANONYMOUS_PULL_TOKEN_GRANTED=NAO",
        "ANONYMOUS_TAG_LIST_ACCESS=DENIED",
        "ANONYMOUS_MANIFEST_ACCESS=DENIED",
        "AUTHENTICATED_MANIFEST_DIGEST=",
        "PRIVATE_PACKAGE_POST_PUSH=APPROVED",
    ):
        assert required in script


def test_pull_and_smoke_follow_post_push_private_gate() -> None:
    steps = job("publish-container")["steps"]
    names = [step["name"] for step in steps]
    gate_index = names.index(PRIVATE_PACKAGE_POST_PUSH_STEP)
    downstream = (
        "Remove tag, pull exclusively by digest, and validate RepoDigest",
        "Smoke the pulled digest with console logging",
        "Smoke the pulled digest with JSON logging",
    )
    assert all(gate_index < names.index(name) for name in downstream)


def test_private_package_recovery_preserves_publication_contract() -> None:
    text = raw()
    assert text.count("docker push ") == 1
    assert ":latest" not in text
    assert "IMAGE_TAG: latest" not in text
    assert set(workflow()["on"]) == {"workflow_dispatch"}
    assert set(workflow()["jobs"]) == {"verify-gates", "publish-container"}
    verify_script = job("verify-gates")["steps"][0]["run"]
    assert 'approved_run("quality-gate.yml")' in verify_script
    assert 'approved_run("container-gate.yml")' in verify_script
    assert "workflow rerun" not in text.lower()
    assert "gh run rerun" not in text.lower()
