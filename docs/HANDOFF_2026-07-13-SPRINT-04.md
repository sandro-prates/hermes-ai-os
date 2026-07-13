# Hermes AI OS  Project Handoff

## 1. Estado Geral

- Projeto: Hermes AI OS.
- Versão: `0.0.1`.
- Milestone: M0 — Foundation (`in_progress`).
- Última Sprint concluída: SPRINT-04 — Foundation Integrity Baseline.
- Sprint ativa: nenhuma.
- Próxima Sprint planejada: nenhuma.
- Implementação da SPRINT-04: commit `2dc6365` —
  `test(api): protect base endpoint contracts`.

## 2. Arquitetura Atual

- Backend FastAPI em `apps/backend/app`.
- Aplicação e endpoint raiz em `app.main`.
- API versionada em `app.api.v1`, com health check.
- Configuração central em `app.core.settings.Settings` com `pydantic-settings`.
- Observabilidade central em `app.core.observability`.
- Logging console e JSON configurado com `logging.config.dictConfig`.
- Middleware ASGI puro e correlação por `ContextVar`.
- Snapshot como projeção determinística da árvore Git, sem autorreferência.

## 3. Funcionalidades Implementadas

- `GET /` e `GET /api/v1/health`.
- Geração, preservação e retorno do Request ID no header configurado.
- Logs HTTP de início, conclusão e falha.
- Seleção de `LOG_LEVEL` e `LOG_FORMAT`.
- `.env.example` sanitizado e alinhado aos nove campos externos de `Settings`.
- Nenhuma funcionalidade de produto foi adicionada na SPRINT-04.

## 4. Contratos Protegidos

- `GET /`: HTTP 200, JSON público exato e Request ID gerado.
- `GET /api/v1/health`: HTTP 200, JSON público exato e Request ID gerado.
- Request ID recebido do cliente preservado exatamente.
- Contrato exato entre `Settings` e `.env.example`.
- Formatos de logging console e JSON.
- Snapshot determinístico, baseado em `git ls-tree HEAD` e sem autorreferência.

## 5. Estrutura Relevante

```text
apps/backend/app/
├── main.py
├── api/
│   ├── router.py
│   └── v1/health.py
└── core/
    ├── settings.py
    └── observability/
tests/
├── test_api.py
├── test_env_example.py
├── test_middleware.py
├── test_observability.py
└── test_project_snapshot.py
tools/
└── project_snapshot.py
docs/
├── 00_PROJECT_MASTER.md
├── 01_PROJECT_STATE.yaml
├── 02_BACKLOG.md
├── 03_CHANGELOG.md
├── PROJECT_SNAPSHOT.md
└── adr/
```

## 6. Qualidade Verificada

- Ruff: aprovado sem violações.
- Pytest: 51 testes aprovados.
- Aviso: 1 `StarletteDeprecationWarning` conhecido e não bloqueante.
- Importação de `app.main`: aprovada para Hermes AI OS `0.0.1`.
- `GET /`: HTTP 200.
- `GET /api/v1/health`: HTTP 200.
- Geração e preservação de Request ID: aprovadas.
- YAML do Project State: válido.

## 7. Documentação e ADRs

Documentos vivos:

- `README.md`.
- `docs/00_PROJECT_MASTER.md`.
- `docs/01_PROJECT_STATE.yaml`.
- `docs/02_BACKLOG.md`.
- `docs/03_CHANGELOG.md`.
- `docs/PROJECT_SNAPSHOT.md`.
- `docs/adr/README.md`.

ADRs aceitos:

- ADR-0001 — `pyproject.toml` como fonte principal.
- ADR-0002 — pacote central de observabilidade.
- ADR-0003 — middleware ASGI e `ContextVar`.
- ADR-0004 — documentação como continuidade.
- ADR-0005 — snapshot como projeção determinística da árvore Git.

## 8. Commits Relevantes

- `685b053` — baseline de planejamento da SPRINT-04 e snapshot final anterior.
- `2dc6365` — testes diretos da API base e ativação documental da SPRINT-04.

Nenhum hash é atribuído antecipadamente ao futuro commit documental ou ao futuro
commit do snapshot.

## 9. Dívidas e Limitações

- DT-007 permanece aberta, separada e não ativada.
- O aviso de depreciação de `TestClient`/`httpx` permanece conhecido.
- Estratégia de lock de dependências ainda não definida.
- CI/CD não identificado.
- Compatibilidade não comprovada em todos os sistemas e versões de Python declarados.
- Política de validação e tamanho de Request IDs recebidos não documentada.
- Banco de dados, runtime de agentes, memória, dashboard e integrações não implementados.

## 10. Continuidade

- Nenhuma Sprint está ativa.
- Nenhuma próxima Sprint foi aprovada.
- DT-007 não deve ser ativada automaticamente.
- A próxima conversa deve validar Git, código, testes e snapshot antes de planejar.
- A validade do snapshot deve ser consultada diretamente com
  `python tools/project_snapshot.py --check`.

## 11. Trabalhos que Não Devem Ser Repetidos

- Observabilidade, middleware ASGI, formatters e correlação por Request ID.
- DT-008 e o contrato sanitizado de `.env.example`.
- Gerador, determinismo, autorreferência e ADR-0005 do snapshot.
- Testes diretos dos contratos públicos de `GET /` e `GET /api/v1/health`.

## 12. Próximos Passos Elegíveis

- Auditar e selecionar um novo escopo somente após verificar a baseline operacional.
- Avaliar DT-007 como candidata, sem ativação automática.
- Avaliar estratégia de lock, compatibilidade e CI/CD somente mediante planejamento.
- Avaliar o aviso do `TestClient` separadamente, sem misturá-lo a outro escopo.

Nenhuma Sprint ou Task futura está planejada ou ativada por este handoff.
