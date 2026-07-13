# ADR-0003 — Middleware ASGI puro e `ContextVar` para correlação

- **Status:** Accepted
- **Data:** 2026-07-12
- **Escopo:** Requisições HTTP
- **Implementação:** Parcial, validada manualmente

## Contexto

O Hermes AI OS precisa correlacionar logs gerados durante uma mesma requisição.

Essa correlação deverá funcionar em código assíncrono e permitir futura integração entre API, serviços, tracing distribuído e observabilidade externa.

Uma primeira implementação utilizou `BaseHTTPMiddleware`, mas a arquitetura foi alterada para middleware ASGI puro, evitando limitações conhecidas de propagação de contexto.

## Decisão

Usar:

- middleware ASGI puro;
- `ContextVar` para armazenar o Request ID;
- `Token` para restaurar o contexto anterior;
- header `X-Request-ID` para entrada e saída;
- UUID gerado automaticamente quando o cliente não envia um identificador.

O middleware deve:

1. ignorar scopes não HTTP;
2. obter ou gerar o Request ID;
3. definir o contexto;
4. registrar início da requisição;
5. capturar status da resposta;
6. adicionar o header à resposta;
7. registrar conclusão ou exceção;
8. restaurar o contexto no bloco `finally`.

## Consequências positivas

- Compatibilidade adequada com `async/await`.
- Menor risco de vazamento entre requisições.
- Base para tracing distribuído.
- Correlação automática nos logs.
- Independência de detalhes internos do FastAPI.

## Consequências negativas

- Middleware ASGI puro é mais detalhado que `BaseHTTPMiddleware`.
- Requer testes de concorrência e exceções.
- Request IDs recebidos ainda precisam de política de validação e limite de tamanho.
- A ordem futura dos middlewares precisará ser documentada e testada.

## Estado verificado

Foram validados manualmente:

- geração de Request ID;
- preservação de Request ID recebido;
- header de resposta;
- correlação nos logs;
- HTTP 200 no health endpoint;
- campos de método, caminho, status e duração.

Não há testes automatizados.