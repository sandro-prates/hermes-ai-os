# ADR-0002 — Pacote central de observabilidade

- **Status:** Accepted
- **Data:** 2026-07-12
- **Escopo:** Backend e futuros runtimes
- **Implementação:** Parcial, SPRINT-02 em andamento

## Contexto

Logging é uma preocupação transversal que será utilizada pela API, runtime de agentes, workers, CLI, scheduler e integrações futuras.

Manter a configuração diretamente em `main.py` ou em um arquivo isolado e acoplado ao FastAPI dificultaria reutilização e evolução para métricas, tracing e serviços externos.

## Decisão

Centralizar a infraestrutura de logging no pacote:

`app.core.observability`

O pacote deve fornecer uma API pública mínima e reutilizável, atualmente composta por:

- `configure_logging()`;
- `get_logger()`.

A configuração utiliza a biblioteca padrão `logging` e `logging.config.dictConfig`.

## Consequências positivas

- Baixo acoplamento ao FastAPI.
- Reutilização por API, workers, agentes e CLI.
- Namespace consistente de logger.
- Evolução futura para JSON, OpenTelemetry, Loki, Grafana, Sentry ou outros destinos.
- Código de negócio não precisa conhecer handlers ou formatters.

## Consequências negativas

- O pacote passa a ser infraestrutura crítica.
- Mudanças incompatíveis podem afetar vários runtimes.
- Exige testes automatizados próprios.
- Pode precisar de adaptação futura para logging distribuído e processamento multiprocessado.

## Alternativas consideradas

### `logging.basicConfig`

Foi implementado inicialmente em `app/core/logging.py`, mas não fornece a modularidade desejada.

Esse arquivo não possui imports ativos e é candidato à remoção ou consolidação.

### Dependência imediata de `structlog`

Não foi adotada nesta fase para evitar uma dependência adicional antes de existir necessidade comprovada.

## Estado verificado

Console logging, filtro de contexto, formatter e middleware HTTP estão implementados localmente.

JSON logging e testes automatizados ainda estão pendentes.