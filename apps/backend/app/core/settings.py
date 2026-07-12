from functools import lru_cache

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

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()