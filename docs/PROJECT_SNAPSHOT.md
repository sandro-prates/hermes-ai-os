# Hermes AI OS  Project Snapshot

## 1. Identificação

- schema do snapshot: 3
- fingerprint SHA-256 da árvore projetada: `e036f246ad0d090e213c6cff729a85c2b68aa0af5d0781c0446a13d7f6aa725f`
- arquivos na projeção: 36
- projeto: Hermes AI OS
- versão: 0.0.1
- estado analisado: projeção determinística da árvore commitada
- observação: `docs/PROJECT_SNAPSHOT.md` é excluído da projeção para evitar autorreferência; o estado transitório é exibido somente no console.

## 2. Estado Atual

- EPIC: EPIC-003 — Logging System
- Sprint: SPRINT-02
- Task: README e onboarding reproduzível do Hermes AI OS
- status: completed
- próxima Task: Versionar e validar um .env.example sanitizado

## 3. Próxima Sprint Planejada

- EPIC: EPIC-004 — Foundation Reproducibility
- Sprint: SPRINT-03 — Reproducible Onboarding Baseline
- Status da Sprint: planned
- Objetivo: Tornar o onboarding documentado reproduzível a partir de um clone limpo
- Primeira Task: DT-008 — Versionar e validar um .env.example sanitizado
- Status da Task: planned
- Implementação iniciada: não

## 4. Estrutura Relevante

```text
├── .editorconfig
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

## 9. Observabilidade

- Pacote: `app.core.observability`.
- Formatos identificados no código: `console` e `json`.
- Header padrão de correlação: `X-Request-ID`.
- Contexto assíncrono: `ContextVar`.

## 10. Qualidade

- Ruff: estado commitado `passed`.
- Pytest: estado commitado `passed — 32 aprovado(s), 1 aviso(s)`.
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

## 12. Alterações Locais

- O estado transitório não integra o snapshot canônico.
- Staged, unstaged e untracked são exibidos no console antes da geração ou checagem.

## 13. Problemas Conhecidos

- Aviso de depreciação do `TestClient` relacionado ao `httpx`, não bloqueante.
- documento de pesquisa tecnológica vazio.

## 14. Dívida Técnica

- DT-007 — Pesquisa tecnológica vazia — ⚠️ Aberta
- DT-008 — `.env.example` ignorado e ausente do Git — ⚠️ Aberta

## 15. Próximo Passo Documentado

Versionar e validar um .env.example sanitizado
