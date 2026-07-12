from fastapi import FastAPI

from app.api.router import api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
    }