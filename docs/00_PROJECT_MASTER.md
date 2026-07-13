# Hermes AI OS

> **Status:** Em desenvolvimento
>
> **Versão:** 0.0.1
>
> **Modelo de negócio:** Open Core
>
> **Fase atual:** M0 — Foundation
>
> **Último EPIC concluído:** EPIC-004 — Foundation Reproducibility
>
> **Última Sprint concluída:** SPRINT-03 — Reproducible Onboarding Baseline
>
> **Sprint atual:** nenhuma
>
> **Responsável:** Sandro Prates
>
> **Última verificação:** 13/07/2026

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

### `2ebed11`

DT-008 implementada com `.env.example` sanitizado, exceção segura no `.gitignore`,
teste contratual e documentação operacional alinhada.

### `b1ab2ea`

Documentação final da SPRINT-03 e handoff de 13/07/2026 preparados e commitados.

### `313de97`

Estado transitório de publicação removido da documentação permanente.

## Último trabalho concluído

### EPIC-004 — Foundation Reproducibility — Concluída

### SPRINT-03 — Reproducible Onboarding Baseline — Concluída

- DT-008 concluída no commit `2ebed11`;
- `.env.example` sanitizado e rastreado;
- `.env` e variantes reais permanecem ignorados;
- contrato de configuração protegido por dois testes automatizados;
- 44 testes e Ruff aprovados;
- endpoints, Request ID e formatos de logging preservados;
- nenhuma dependência ou funcionalidade de produto adicionada.

A EPIC-004 possuía somente a SPRINT-03 e a DT-008 como escopo formal; todos os critérios
funcionais foram atendidos. O snapshot oficial será atualizado separadamente como
artefato técnico de continuidade. Nenhuma nova Sprint foi ativada.

## Trabalho concluído anterior

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

- 44 testes coletados;
- 44 testes aprovados;
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

## Sprint concluída

- EPIC-004 — Foundation Reproducibility.
- SPRINT-03 — Reproducible Onboarding Baseline.
- Status: `completed`.
- Objetivo: tornar o onboarding documentado reproduzível a partir de um clone limpo.
- Task concluída: DT-008 — versionar e validar um `.env.example` sanitizado (`completed`).

A baseline publicada em `51d3747` foi comprovada antes da ativação, e a implementação
foi commitada em `2ebed11`. EPIC-004, SPRINT-03 e DT-008 estão concluídas. A documentação
e o handoff estão comprovados por `b1ab2ea` e `313de97`. O snapshot oficial será
atualizado pelo fluxo técnico. Nenhuma nova Sprint foi ativada.

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
