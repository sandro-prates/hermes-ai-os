import pytest
from app.core.settings import settings
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    ("path", "expected_status"),
    (
        ("/", "running"),
        ("/api/v1/health", "healthy"),
    ),
)
def test_base_endpoint_contract(path: str, expected_status: str) -> None:
    response = client.get(path)

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    assert response.json() == {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": expected_status,
    }
    assert response.headers[settings.REQUEST_ID_HEADER]


def test_base_api_preserves_received_request_id() -> None:
    request_id = "hermes-foundation-integrity"

    response = client.get(
        "/api/v1/health",
        headers={settings.REQUEST_ID_HEADER: request_id},
    )

    assert response.status_code == 200
    assert response.headers[settings.REQUEST_ID_HEADER] == request_id
