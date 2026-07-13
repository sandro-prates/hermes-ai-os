# Hermes AI OS  Project Snapshot

## 1. Identificação

- schema do snapshot: 3
- fingerprint SHA-256 da árvore projetada: `4f069e2d34549cb188c76058280fcd720bdc26768b2fd39f0f257cb76e2362ff`
- arquivos na projeção: 39
- projeto: Hermes AI OS
- versão: 0.0.1
- estado analisado: projeção determinística da árvore commitada
- origem da projeção: entradas rastreadas em HEAD obtidas por `git ls-tree HEAD`
- ordenação da projeção: determinística pelo caminho relativo
- metadados excluídos: branch, upstream, hash, data e mensagem de commit
- observação: `docs/PROJECT_SNAPSHOT.md` é excluído da projeção para evitar autorreferência; o estado transitório é exibido somente no console.

## 2. Estado Atual

- EPIC: EPIC-004 — Foundation Reproducibility
- Status da EPIC: completed
- Sprint: SPRINT-03 — Reproducible Onboarding Baseline
- Status da Sprint: completed
- Task: DT-008 — Versionar e validar um .env.example sanitizado
- Status da Task: completed

## 3. Continuidade de Sprint

- Sprint ativa: nenhuma
- Próxima Sprint planejada: nenhuma

## 4. Estrutura Relevante

```text
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── Hermes-AI-OS.code-workspace
├── LICENSE
├── pyproject.toml
├── README.md
├── apps
│   └── backend
│       └── app
│           ├── main.py
│           ├── api
│           │   ├── __init__.py
│           │   ├── router.py
│           │   └── v1
│           │       ├── __init__.py
│           │       └── health.py
│           └── core
│               ├── settings.py
│               └── observability
│                   ├── __init__.py
│                   ├── constants.py
│                   ├── filters.py
│                   ├── formatters.py
│                   ├── logging.py
│                   ├── middleware.py
│                   └── request_context.py
├── docs
│   ├── 00_PROJECT_MASTER.md
│   ├── 01_PROJECT_STATE.yaml
│   ├── 02_BACKLOG.md
│   ├── 03_CHANGELOG.md
│   ├── HANDOFF_2026-07-12.md
│   ├── HANDOFF_2026-07-13.md
│   ├── adr
│   │   ├── ADR-0001-pyproject-como-fonte-de-dependencias.md
│   │   ├── ADR-0002-pacote-central-de-observabilidade.md
│   │   ├── ADR-0003-middleware-asgi-e-contextvars.md
│   │   ├── ADR-0004-documentacao-como-sistema-de-continuidade.md
│   │   ├── ADR-0005-snapshot-como-projecao-da-arvore-git.md
│   │   └── README.md
│   └── research
│       └── 2026-07-12-stack-tecnologica.md
├── tests
│   ├── test_env_example.py
│   ├── test_middleware.py
│   ├── test_observability.py
│   └── test_project_snapshot.py
└── tools
    └── project_snapshot.py
```

## 5. Arquitetura Implementada

- Backend FastAPI em `apps/backend/app`.
- Configuração central em `app.core.settings`.
- API versionada em `app.api.v1`.
- Observabilidade central em `app.core.observability`.
- Módulos Python identificados:
- `app.api`
- `app.api.router`
- `app.api.v1`
- `app.api.v1.health`
- `app.core.observability`
- `app.core.observability.constants`
- `app.core.observability.filters`
- `app.core.observability.formatters`
- `app.core.observability.logging`
- `app.core.observability.middleware`
- `app.core.observability.request_context`
- `app.core.settings`
- `app.main`

## 6. Funcionalidades Verificadas

- Aplicação FastAPI: validação commitada registrada como `passed`.
- Endpoints identificados por inspeção AST do código Python.
- Middleware ASGI e observabilidade presentes no pacote `app.core.observability`.

## 7. Endpoints Identificados

- `GET /` — `apps/backend/app/main.py`
- `GET /api/v1/health` — `apps/backend/app/api/v1/health.py`

## 8. Configuração e Dependências

- Python requerido: `>=3.12,<3.15`.
- Dependências diretas:
- `fastapi>=0.139,<1.0`
- `uvicorn[standard]>=0.51,<1.0`
- `pydantic-settings>=2.14,<3.0`
- `orjson>=3.11,<4.0`
- Contrato de configuração reproduzível:
- `.env.example` presente, sanitizado e rastreado na projeção.
- Variáveis do template correspondem exatamente aos campos externos suportados por `Settings`.
- Variáveis suportadas, na ordem declarada em `Settings`: `APP_NAME`, `APP_VERSION`, `ENVIRONMENT`, `DEBUG`, `HOST`, `PORT`, `LOG_LEVEL`, `LOG_FORMAT`, `REQUEST_ID_HEADER`.
- A formação dos nomes externos considera `env_prefix` e aliases simples (`validation_alias` ou `alias`); os nomes canônicos são preservados na renderização.
- Comparação de chaves não sensível a maiúsculas e minúsculas, conforme `case_sensitive=false`.
- Aliases complexos e configurações ambíguas são rejeitados de forma fail-closed.
- Colisões no template ou nos nomes externos de `Settings`, assim como chaves ausentes, adicionais ou duplicadas, são rejeitadas.
- `.env.example` carregado e validado com sucesso por `pydantic-settings`.
- Contrato protegido por `tests/test_env_example.py`.
- Arquivo `.env` real ausente da projeção rastreada.

## 9. Observabilidade

- Pacote: `app.core.observability`.
- Formatos identificados no código: `console` e `json`.
- Header de correlação configurável por `Settings.REQUEST_ID_HEADER`; padrão `X-Request-ID`.
- Request ID gerado automaticamente quando ausente.
- Request ID enviado pelo cliente preservado.
- Request ID incluído no header da resposta.
- Contexto assíncrono de correlação baseado em `ContextVar`.
- Request ID do contexto injetado nos registros de log.

## 10. Qualidade

- Ruff: estado commitado `passed`.
- Pytest: estado commitado `passed — 48 aprovado(s), 1 aviso(s)`.
- importação da aplicação: estado commitado `passed`.

## 11. Documentação e ADRs

- `docs/00_PROJECT_MASTER.md` — presente em HEAD
- `docs/01_PROJECT_STATE.yaml` — presente em HEAD
- `docs/02_BACKLOG.md` — presente em HEAD
- `docs/03_CHANGELOG.md` — presente em HEAD

- ADR-0001 — `pyproject.toml` como fonte principal do projeto Python — Accepted
- ADR-0002 — Pacote central de observabilidade — Accepted
- ADR-0003 — Middleware ASGI puro e `ContextVar` para correlação — Accepted
- ADR-0004 — Documentação viva como sistema formal de continuidade — Accepted
- ADR-0005 — Snapshot como projeção determinística da árvore Git — Accepted

## 12. Problemas Conhecidos

- Aviso de depreciação do `TestClient` relacionado ao `httpx`, não bloqueante.
- documento de pesquisa tecnológica vazio.

## 13. Dívida Técnica

- DT-007 — Pesquisa tecnológica vazia — ⚠️ Aberta — separada do escopo encerrado e não ativada

## 14. Próximo Passo Documentado

Não identificado

## 15. Limitações Atuais

- Banco de dados ainda não implementado.
- Runtime de agentes ainda não implementado.
- Memória ainda não implementada.
- Dashboard ainda não implementado.
- Integrações externas ainda não implementadas.
