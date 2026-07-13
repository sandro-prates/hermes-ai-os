# Hermes AI OS

> **Status:** Em desenvolvimento
>
> **Versão:** 0.0.1
>
> **Modelo de negócio:** Open Core
>
> **Fase atual:** M0 — Foundation
>
> **EPIC atual:** EPIC-003 — Logging System
>
> **Sprint atual:** SPRINT-02 — Em andamento
>
> **Responsável:** Sandro Prates
>
> **Última verificação:** 12/07/2026

---

# Retomada obrigatória

Toda nova conversa, pessoa ou assistente de IA deve:

1. Ler `docs/00_PROJECT_MASTER.md`.
2. Ler `docs/01_PROJECT_STATE.yaml`.
3. Ler `docs/02_BACKLOG.md`.
4. Ler `docs/03_CHANGELOG.md`.
5. Ler os ADRs aceitos em `docs/adr/`.
6. Executar `git status --short --branch`.
7. Validar a documentação contra Git, código e testes.

Quando houver divergência:

1. Git e código determinam o que existe.
2. Testes determinam o que foi validado.
3. A documentação deve ser corrigida.
4. Nenhum status deve ser inventado.

---

# Produto

O Hermes AI OS é uma plataforma Local First e Cloud Ready para criação, orquestração e execução de agentes de Inteligência Artificial.

## Missão

Permitir que pessoas e empresas automatizem tarefas complexas com IA de forma segura, modular e escalável.

## Visão

Evoluir desde uma instalação local até uma plataforma comercial gerenciada, com plugins, marketplace e recursos Enterprise.

## Princípios

- Simplicidade.
- Modularidade.
- Reprodutibilidade.
- Documentação viva.
- Produto primeiro.
- Evidência antes de status.

---

# Estado verificado

## Git

- Branch: `main`
- Upstream: `origin/main`
- Base Git verificada: 2a30fa4
- Commit anterior: `feec40a`
- Working tree: possui alterações locais não commitadas.

## Entregas commitadas

### `feec40a`

Bootstrap inicial do Hermes AI OS.

### `2a30fa4`

API v1, settings centralizados e health endpoint.

## Trabalho atual

### EPIC-003 — Logging System

### SPRINT-02 — Em andamento

Implementado e validado manualmente:

- pacote `app.core.observability`;
- logging com `dictConfig`;
- logger `hermes`;
- `ConsoleFormatter`;
- `JsonFormatter`;
- seleção entre `console` e `json` por `LOG_FORMAT`;
- contexto com `ContextVar`;
- middleware ASGI puro;
- geração e propagação de `X-Request-ID`;
- `settings.REQUEST_ID_HEADER` como fonte única do header;
- logs HTTP com método, caminho, status e duração;
- integração ao FastAPI;
- oito testes automatizados aprovados;
- `/` e `/api/v1/health` respondendo HTTP 200.

A Sprint ainda não atende à Definition of Done porque não foi commitada nem publicada.

Pendências principais:

- criar o commit da Sprint;
- publicar no repositório remoto.

---

# Qualidade atual

## Pytest

Resultado verificado:

- 8 testes coletados;
- 8 testes aprovados em `0.21s`;
- 1 aviso de depreciação do `TestClient`.

## Ruff

Resultado verificado:

`All checks passed!`

A análise estática está aprovada.

---

# Sistema de continuidade

- `docs/00_PROJECT_MASTER.md` — visão e porta de entrada.
- `docs/01_PROJECT_STATE.yaml` — estado operacional verificável.
- `docs/02_BACKLOG.md` — trabalho e dívida técnica.
- `docs/03_CHANGELOG.md` — histórico de mudanças.
- `docs/adr/` — decisões arquiteturais.

ADRs aceitos:

- ADR-0001 — `pyproject.toml`.
- ADR-0002 — pacote central de observabilidade.
- ADR-0003 — middleware ASGI e `ContextVar`.
- ADR-0004 — documentação como continuidade.

---

# Roadmap de alto nível

- M0 — Foundation
- M1 — Infraestrutura
- M2 — Backend
- M3 — Runtime de agentes
- M4 — Memória
- M5 — Dashboard
- M6 — Integrações
- M7 — Marketplace
- M8 — Enterprise

Somente M0 está em andamento. Os demais permanecem pendentes como milestones formais.

---

# Fluxo obrigatório

Pesquisa → Análise → Implementação → Testes → Validação → Documentação → Commit

# Definition of Done

Uma Task somente pode ser concluída quando:

- código implementado;
- testes aplicáveis executados;
- análise estática aprovada;
- documentação atualizada;
- `PROJECT_STATE` atualizado;
- changelog atualizado;
- ADR criado quando necessário;
- commit realizado.

# Regra de ouro

Qualquer pessoa ou IA deve conseguir retomar o Hermes AI OS lendo estes documentos e validando-os contra o repositório.
