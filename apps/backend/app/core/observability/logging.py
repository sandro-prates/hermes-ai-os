import logging
from logging.config import dictConfig

from app.core.observability.constants import HERMES_LOGGER_NAME
from app.core.observability.filters import RequestContextFilter
from app.core.observability.formatters import ConsoleFormatter, JsonFormatter
from app.core.settings import settings


def configure_logging() -> None:
    """
    Configura o logging central do Hermes AI OS.

    A configuração pode ser reutilizada pela API, workers,
    tarefas assíncronas, CLI e runtime de agentes.
    """

    log_level = settings.LOG_LEVEL.upper()
    log_format = settings.LOG_FORMAT

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_context": {
                "()": RequestContextFilter,
            },
        },
        "formatters": {
            "console": {
                "()": ConsoleFormatter,
                "format": (
                    "%(asctime)s | %(levelname)-8s | %(name)s | "
                    "[request_id=%(request_id)s] | %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": JsonFormatter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": log_format,
                "filters": ["request_context"],
                "level": log_level,
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            HERMES_LOGGER_NAME: {
                "handlers": ["console"],
                "level": log_level,
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }

    dictConfig(config)


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Retorna um logger pertencente ao namespace do Hermes AI OS.
    """

    if not name:
        return logging.getLogger(HERMES_LOGGER_NAME)

    return logging.getLogger(f"{HERMES_LOGGER_NAME}.{name}")