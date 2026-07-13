import json
import logging

from app.core.observability.formatters import ConsoleFormatter, JsonFormatter
from app.core.observability.request_context import (
    get_request_id,
    reset_request_id,
    set_request_id,
)


def test_request_id_defaults_to_placeholder() -> None:
    assert get_request_id() == "-"


def test_request_id_can_be_set_and_restored() -> None:
    token = set_request_id("test-request-id")

    try:
        assert get_request_id() == "test-request-id"
    finally:
        reset_request_id(token)

    assert get_request_id() == "-"


def test_console_formatter_includes_structured_fields() -> None:
    formatter = ConsoleFormatter("%(message)s")
    record = logging.LogRecord(
        name="hermes.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request completed",
        args=(),
        exc_info=None,
    )
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.elapsed_ms = 1.25

    output = formatter.format(record)

    assert output == (
        "request completed | method=GET path=/health "
        "status_code=200 elapsed_ms=1.25"
    )


def test_json_formatter_returns_structured_json() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="hermes.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request completed",
        args=(),
        exc_info=None,
    )
    record.request_id = "json-test-id"
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.elapsed_ms = 1.25

    payload = json.loads(formatter.format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "hermes.test"
    assert payload["request_id"] == "json-test-id"
    assert payload["message"] == "request completed"
    assert payload["method"] == "GET"
    assert payload["path"] == "/health"
    assert payload["status_code"] == 200
    assert payload["elapsed_ms"] == 1.25
    assert "timestamp" in payload