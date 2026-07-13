import logging

import pytest
from app.core.observability.middleware import RequestLoggingMiddleware
from app.core.observability.request_context import get_request_id
from app.core.settings import settings
from fastapi import FastAPI
from fastapi.testclient import TestClient


class ListHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def create_test_app(*, failing: bool = False) -> FastAPI:
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    if failing:

        @app.get("/test")
        async def test_endpoint() -> None:
            raise RuntimeError("test failure")

    else:

        @app.get("/test")
        async def test_endpoint() -> dict[str, str]:
            return {"status": "ok"}

    return app


def test_middleware_generates_request_id_and_adds_response_header() -> None:
    response = TestClient(create_test_app()).get("/test")

    assert response.status_code == 200
    assert response.headers[settings.REQUEST_ID_HEADER]
    assert get_request_id() == "-"


def test_middleware_preserves_received_request_id() -> None:
    request_id = "received-request-id"

    response = TestClient(create_test_app()).get(
        "/test",
        headers={settings.REQUEST_ID_HEADER: request_id},
    )

    assert response.status_code == 200
    assert response.headers[settings.REQUEST_ID_HEADER] == request_id
    assert get_request_id() == "-"


def test_middleware_logs_request_completion() -> None:
    logger = logging.getLogger("hermes.http")
    handler = ListHandler()
    previous_level = logger.level
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    try:
        response = TestClient(create_test_app()).get("/test")
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)

    completed = [
        record
        for record in handler.records
        if record.getMessage() == "HTTP request completed"
    ]

    assert response.status_code == 200
    assert len(completed) == 1
    assert completed[0].method == "GET"
    assert completed[0].path == "/test"
    assert completed[0].status_code == 200
    assert completed[0].elapsed_ms >= 0


def test_middleware_logs_failure_and_restores_context() -> None:
    logger = logging.getLogger("hermes.http")
    handler = ListHandler()
    logger.addHandler(handler)

    try:
        with pytest.raises(RuntimeError, match="test failure"):
            TestClient(create_test_app(failing=True)).get("/test")
    finally:
        logger.removeHandler(handler)

    failures = [
        record
        for record in handler.records
        if record.getMessage() == "HTTP request failed"
    ]

    assert len(failures) == 1
    assert failures[0].method == "GET"
    assert failures[0].path == "/test"
    assert failures[0].status_code == 500
    assert failures[0].elapsed_ms >= 0
    assert failures[0].exc_info is not None
    assert get_request_id() == "-"