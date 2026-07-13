from app.api.router import api_router
from app.core.observability import configure_logging
from app.core.observability.middleware import RequestLoggingMiddleware
from app.core.settings import settings
from fastapi import FastAPI

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
    }
