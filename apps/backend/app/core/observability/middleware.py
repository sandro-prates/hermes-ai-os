import time
import uuid

from app.core.observability import get_logger
from app.core.observability.request_context import (
    reset_request_id,
    set_request_id,
)
from app.core.settings import settings
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

logger = get_logger("http")


class RequestLoggingMiddleware:
    """
    Middleware ASGI para correlação e registro de requisições HTTP.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        request_id = headers.get(settings.REQUEST_ID_HEADER) or str(uuid.uuid4())
        token = set_request_id(request_id)

        method = scope.get("method", "-")
        path = scope.get("path", "-")
        status_code = 500
        start = time.perf_counter()

        logger.info(
            "HTTP request started",
            extra={
                "method": method,
                "path": path,
            },
        )

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code

            if message["type"] == "http.response.start":
                status_code = message["status"]

                response_headers = MutableHeaders(scope=message)
                response_headers[settings.REQUEST_ID_HEADER] = request_id

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)

        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000

            logger.exception(
                "HTTP request failed",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "elapsed_ms": round(elapsed_ms, 2),
                },
            )
            raise

        else:
            elapsed_ms = (time.perf_counter() - start) * 1000

            logger.info(
                "HTTP request completed",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "elapsed_ms": round(elapsed_ms, 2),
                },
            )

        finally:
            reset_request_id(token)
