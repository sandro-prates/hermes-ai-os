import logging

from app.core.observability.request_context import get_request_id


class RequestContextFilter(logging.Filter):
    """
    Injeta informações do contexto atual em todos os registros de log.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True
