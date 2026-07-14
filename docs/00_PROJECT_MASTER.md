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
> **Última Sprint concluída:** SPRINT-06 — Continuity State Integrity
>
> **Sprint atual:** SPRINT-07 — Dependency Reproducibility Proof (in_progress)
>
> **Responsável:** Sandro Prates
>
> **Última verificação:** 13/07/2026

## SPRINT-07 — Dependency Reproducibility Proof

**Status:** `in_progress`

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Task ou DT formal ativa:** nenhuma

**Última entrega concluída:** SPRINT-06 e DT-009

**Sprint seguinte planejada:** nenhuma

Baseline publicada comprovada antes da ativação:
`9cfefa8bf117bceb11bcbd5df2a18cc28f82303c`.

Baseline local pré-SPRINT-07:
`ea5a1ffc456075c6938905759b32059e8b7e2b85`.

Branch `main`, ahead 2, behind 0 e working tree limpa foram comprovados antes da
ativação.

**Escopo autorizado:**

- ler diretamente o `pyproject.toml` e confirmar `requires-python`, dependências,
  extras e marcadores;
- instalar posteriormente uma versão específica do `uv` fora da `.venv` oficial,
  registrando versão, caminho e método de instalação;
- criar duas áreas experimentais independentes fora do repositório oficial,
  ambas baseadas em `ea5a1ff`, incluindo um clone Git completo;
- gerar um lock em cada área experimental e comparar os resultados;
- validar instalação e testes em ambientes limpos;
- testar imediatamente Windows com Python 3.14;
- avaliar `pylock.toml` somente como mecanismo de interoperabilidade;
- produzir relatório decisório;
- tratar Linux com Python 3.12, 3.13 e 3.14 como gate de encerramento, caso essas
  versões permaneçam na matriz aprovada.

**Restrições:**

- esta alteração apenas ativa documentalmente a Sprint;
- nenhum experimento ou instalação do `uv` está registrado como executado;
- nenhuma dependência pode ser alterada;
- nenhum `uv.lock` pode ser adicionado ou adotado no repositório oficial sem
  aprovação humana específica;
- CI e SPRINT-08 permanecem fora do escopo;
- código da aplicação, testes do produto, snapshot e handoffs permanecem inalterados;
- testes de governança podem ser ajustados somente para refletir o estado documental aprovado;
- o encerramento exige validação independente posterior;
- push não está autorizado.

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

### `686a630`

Contrato do snapshot corrigido para representar explicitamente o estado final, com
quatro testes de regressão adicionais.

### `777a0fe`

Qualidade atual e cobertura de regressão do snapshot registradas na documentação viva.

### `01ac0b0`

Contrato funcional de Request ID explicitado no snapshot: geração, preservação,
retorno no header, correlação por `ContextVar` e injeção nos logs.

### `4f4e2bb`

Contrato determinístico entre `Settings` e `.env.example` explicitado, incluindo
`env_prefix`, aliases, `case_sensitive` e validações fail-closed.

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
funcionais foram atendidos. O snapshot oficial é um artefato técnico de continuidade,
cuja validade deve ser verificada com `python tools/project_snapshot.py --check`.

## Sprint concluída anterior

### SPRINT-04 — Foundation Integrity Baseline — Concluída

- Milestone: M0 — Foundation.
- EPIC: nenhuma nova EPIC criada; EPIC-004 permanece concluída.
- Item funcional: pendência retrospectiva de testes automatizados da API base.
- Objetivo: proteger diretamente os contratos públicos de `GET /` e
  `GET /api/v1/health` e alinhar o estado documental corrente.
- Escopo funcional restrito a testes; nenhuma mudança de comportamento da aplicação.
- Implementação comprovada pelo commit `2dc6365`.
- Três testes diretos da aplicação real implementados e validados; a implementação
  foi encerrada com 51 testes aprovados.
- Suíte atual: 54 testes aprovados e 1 aviso conhecido e não bloqueante, após três
  regressões do contrato de seleção da Sprint no snapshot.
- Ruff aprovado sem violações.
- Importação, `GET /`, `GET /api/v1/health` e Request ID aprovados.
- Nenhuma dependência, funcionalidade de produto ou arquivo em `apps/` alterado.
- DT-007 permanece aberta, separada e não ativada.
- Definition of Done funcional e documental atendida.
- Nenhuma Sprint está ativa ou formalmente planejada.
- O snapshot oficial é mantido em commit exclusivo pelo fluxo de fechamento; seu
  estado deve ser consultado em `docs/PROJECT_SNAPSHOT.md`, validado com
  `python tools/project_snapshot.py --check` e confrontado com Git.

## Sprint concluída anterior

### SPRINT-05 — Technology Decision Baseline — Concluída

- Milestone: M0 — Foundation.
- EPIC: nenhuma nova EPIC.
- Item formal: DT-007 — pesquisa tecnológica.
- Objetivo: produzir uma baseline decisória para lock de dependências, matriz Python
  e quality gate/CI, mantendo os demais temas em matriz preparatória compacta.
- Resultado: pesquisa commitada em `126aff8`, com recomendações e decisões adiadas,
  sem adoção automática, ADR aceito, dependência, lockfile, CI ou código de produto.
- Baseline de ativação: `1dfd3ee`, sincronizada com `origin/main`, snapshot schema 3,
  Ruff aprovado e 54 testes aprovados com 1 aviso conhecido.
- Recomendação imediata: prova de reprodutibilidade de dependências antes de CI.
- As identificações SPRINT-06 e SPRINT-07 registradas na pesquisa da SPRINT-05 eram
  candidatas provisórias, não ativadas ou planejadas. Com a ativação da Continuity
  State Integrity como SPRINT-06, elas passam a ser referenciadas operacionalmente
  como SPRINT-07 — Dependency Reproducibility Proof e SPRINT-08 — Automated Quality
  Gate, sem adoção ou ativação.

## Última Sprint concluída

### SPRINT-06 — Continuity State Integrity — Concluída

- Milestone: M0 — Foundation.
- EPIC: nenhuma nova EPIC.
- Item formal: DT-009 — Integridade do estado de continuidade.
- Objetivo: separar inequivocamente trabalho ativo, última entrega concluída e trabalho
  planejado no estado operacional.
- Estado operacional: schema 2 com `work.active`, `work.last_completed` e
  `work.planned` como fonte única; SPRINT-06 e DT-009 formam a última entrega.
- Ativação documental: `4e2619c`.
- Implementação, migração e testes: `30416fe`.
- Próxima Sprint formalmente planejada: nenhuma.
- Não inclui adoção tecnológica, dependências, CI ou código de aplicação.
- Implementação local validada com 76 testes aprovados, 1 aviso conhecido, Ruff,
  YAML, importação, endpoints, Request ID e logging aprovados.
- Nenhuma Sprint está ativa.

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

- 76 testes coletados;
- 76 testes aprovados;
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

O gerador oficial reside em `tools/project_snapshot.py`; o relatório reside em
`docs/PROJECT_SNAPSHOT.md`, usa schema 3 e exclui o próprio caminho da projeção. O
relatório deve ser regenerado e verificado com `--check` sempre que a árvore projetada
mudar.

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
e o handoff estão comprovados por `b1ab2ea` e `313de97`. A continuidade do snapshot
segue o contrato do ADR-0005 e é verificada operacionalmente por `--check`. Nenhuma
nova Sprint foi ativada.

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
