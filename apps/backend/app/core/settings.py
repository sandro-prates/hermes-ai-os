from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuração central do Hermes AI OS.

    Todas as configurações da aplicação devem ser declaradas aqui.
    """

    APP_NAME: str = "Hermes AI OS"
    APP_VERSION: str = "0.0.1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["console", "json"] = "console"
    REQUEST_ID_HEADER: str = "X-Request-ID"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
