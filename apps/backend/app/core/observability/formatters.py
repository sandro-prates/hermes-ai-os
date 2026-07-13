import logging
from datetime import UTC, datetime
from typing import Any

import orjson

STRUCTURED_FIELDS = (
    "method",
    "path",
    "status_code",
    "elapsed_ms",
)


class ConsoleFormatter(logging.Formatter):
    """
    Formata logs legíveis para desenvolvimento local.

    Campos estruturados são adicionados somente quando estiverem presentes
    no registro, preservando compatibilidade com bibliotecas externas.
    """

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        details: list[str] = []

        for field_name in STRUCTURED_FIELDS:
            value: Any = getattr(record, field_name, None)

            if value is not None:
                details.append(f"{field_name}={value}")

        if not details:
            return message

        return f"{message} | {' '.join(details)}"


class JsonFormatter(logging.Formatter):
    """
    Formata registros de log como JSON estruturado.
    """

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, "request_id", "-"),
            "message": record.getMessage(),
        }

        for field_name in STRUCTURED_FIELDS:
            value: Any = getattr(record, field_name, None)

            if value is not None:
                payload[field_name] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return orjson.dumps(payload).decode("utf-8")
