# Hermes AI OS

> **Status:** Em desenvolvimento
>
> **Versão:** 0.0.1
>
> **Modelo de negócio:** Open Core
>
> **Fase atual:** M0 — Foundation
>
> **Último EPIC concluído:** EPIC-003 — Logging System
>
> **Última Sprint concluída:** SPRINT-02 — Logging System
>
> **Próxima Sprint planejada:** SPRINT-03 — Reproducible Onboarding Baseline
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
- Baseline publicada antes do fechamento documental: `e1c3587`.
- Commit do encerramento documental: `ed233ff`.
- O estado operacional de branch, upstream e working tree deve ser consultado
  diretamente com Git.

## Entregas commitadas

### `feec40a`

Bootstrap inicial do Hermes AI OS.

### `2a30fa4`

API v1, settings centralizados e health endpoint.

### `a1d0d21`

Sistema de observabilidade, logging JSON, correlação de requisições e testes automatizados.

### `ded359d`

Fechamento documental da EPIC-003 / SPRINT-02.

### `2fcbd17`

README operacional e alinhamento factual dos ADRs 0001–0003.

### `1c02fb0`

Gerador determinístico e testes do snapshot técnico do projeto.

### `19b61d7`

Snapshot baseado exclusivamente no estado commitado.

### `0866657`

Autorreferência removida por projeção determinística da árvore Git.

### `e1c3587`

Snapshot oficial adotado e validado após o próprio commit.

### `ed233ff`

Encerramento documental e handoff oficial preparados.

## Último trabalho concluído

### EPIC-003 — Logging System

### SPRINT-02 — Concluída

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
- testes automatizados de observabilidade aprovados;
- `/` e `/api/v1/health` respondendo HTTP 200.

A Sprint atende à Definition of Done.

Evidência Git:

- commit `a1d0d21` — `feat(observability): complete logging system sprint`;
- publicado em `origin/main`;
- `main` e a referência remota local `origin/main` sincronizadas nesse commit.
- após o push da Sprint, a working tree foi registrada como limpa naquele ponto histórico.

---

# Qualidade atual

## Pytest

Resultado verificado:

- 32 testes coletados;
- 32 testes aprovados;
- 1 aviso de depreciação do `TestClient`.

O aviso de depreciação é uma observação conhecida e não bloqueia o fechamento.

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
- ADR-0005 — snapshot como projeção determinística da árvore Git.

O `README.md` é a entrada operacional para instalação, execução e validação local.

O gerador e `docs/PROJECT_SNAPSHOT.md` estão commitados. O modo `--check` foi aprovado
após o commit do próprio relatório.

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

## Próxima Sprint planejada

- EPIC-004 — Foundation Reproducibility.
- SPRINT-03 — Reproducible Onboarding Baseline.
- Status: `planned`.
- Objetivo: tornar o onboarding documentado reproduzível a partir de um clone limpo.
- Primeira Task: versionar e validar um `.env.example` sanitizado.

A Sprint somente poderá ser ativada na próxima conversa. Nenhuma implementação foi
iniciada neste encerramento.

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
