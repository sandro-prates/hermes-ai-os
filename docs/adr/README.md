# Architecture Decision Records — Hermes AI OS

Este diretório registra decisões arquiteturais relevantes do projeto.

## Status possíveis

- **Proposed:** decisão em avaliação.
- **Accepted:** decisão aprovada para o projeto.
- **Superseded:** substituída por outro ADR.
- **Deprecated:** não deve ser aplicada em novas implementações.

O status do ADR representa a decisão arquitetural, não significa necessariamente que toda a implementação foi concluída.

## ADRs

| ADR | Decisão | Status |
|---|---|---|
| [ADR-0001](ADR-0001-pyproject-como-fonte-de-dependencias.md) | Usar `pyproject.toml` como fonte principal de configuração e dependências Python | Accepted |
| [ADR-0002](ADR-0002-pacote-central-de-observabilidade.md) | Centralizar logging e futura observabilidade em `app.core.observability` | Accepted |
| [ADR-0003](ADR-0003-middleware-asgi-e-contextvars.md) | Usar middleware ASGI puro e `ContextVar` para correlação de requisições | Accepted |
| [ADR-0004](ADR-0004-documentacao-como-sistema-de-continuidade.md) | Usar documentação viva como mecanismo formal de continuidade | Accepted |

## Regra

Uma decisão arquitetural relevante deve ser registrada antes ou durante sua implementação.

Mudanças que substituam uma decisão aceita devem criar um novo ADR e marcar o anterior como `Superseded`.