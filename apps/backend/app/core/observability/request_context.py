from contextvars import ContextVar, Token

from app.core.observability.constants import REQUEST_ID_CONTEXT_KEY

_request_id: ContextVar[str] = ContextVar(
    REQUEST_ID_CONTEXT_KEY,
    default="-",
)


def get_request_id() -> str:
    """
    Retorna o Request ID do contexto atual.
    """
    return _request_id.get()


def set_request_id(request_id: str) -> Token:
    """
    Define o Request ID e retorna o token necessário para restaurar o contexto.
    """
    return _request_id.set(request_id)


def reset_request_id(token: Token) -> None:
    """
    Restaura o contexto anterior, evitando vazamento entre requisições.
    """
    _request_id.reset(token)
