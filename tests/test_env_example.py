import re
from pathlib import Path

from app.core.settings import Settings

ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = ROOT / ".env.example"


def external_settings_names() -> set[str]:
    prefix = Settings.model_config.get("env_prefix", "")
    names: set[str] = set()
    for name, field in Settings.model_fields.items():
        alias = field.validation_alias or field.alias or name
        assert isinstance(alias, str), f"Alias complexo não suportado para {name}"
        names.add(f"{prefix}{alias}")
    return names


def parse_env_example() -> dict[str, str]:
    assert ENV_EXAMPLE.is_file()
    values: dict[str, str] = {}
    for number, raw_line in enumerate(ENV_EXAMPLE.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        assert "=" in line, f"Linha inválida em .env.example: {number}"
        key, value = line.split("=", 1)
        assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key), f"Chave inválida: {key}"
        assert key not in values, f"Chave duplicada: {key}"
        values[key] = value
    return values


def test_env_example_matches_settings_contract(monkeypatch) -> None:
    values = parse_env_example()
    expected_names = external_settings_names()

    assert set(values) == expected_names
    for name in expected_names:
        monkeypatch.delenv(name, raising=False)

    loaded = Settings(_env_file=ENV_EXAMPLE, _env_file_encoding="utf-8")

    assert loaded.LOG_LEVEL == "INFO"
    assert loaded.LOG_FORMAT == "console"
    assert loaded.REQUEST_ID_HEADER == "X-Request-ID"


def test_env_example_has_no_objective_secret_or_local_path_markers() -> None:
    content = ENV_EXAMPLE.read_text(encoding="utf-8")
    forbidden = (
        r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY",
        r"gh[pousr]_[A-Za-z0-9]{20,}",
        r"sk-[A-Za-z0-9]{20,}",
        r"[A-Za-z]:[\\/]Users[\\/]",
        r"/(?:home|Users)/[^/]+/",
    )

    assert all(re.search(pattern, content) is None for pattern in forbidden)
