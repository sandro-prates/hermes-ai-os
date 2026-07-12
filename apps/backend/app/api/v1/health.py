from fastapi import APIRouter

from app.core.settings import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }