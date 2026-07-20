# Hermes AI OS

> **Status:** Em desenvolvimento
>
> **Versão:** 0.0.1
>
> **Modelo de negócio:** Open Core
>
> **Fase atual:** M1 — Infraestrutura
>
> **Último EPIC concluído:** EPIC-004 — Foundation Reproducibility
>
> **Última Sprint concluída:** SPRINT-09 — Reproducible Container Baseline
>
> **Sprint atual:** SPRINT-10 — Snapshot Quality Gate Integrity
>
> **Responsável:** Sandro Prates
>
> **Última verificação:** 19/07/2026

## Ativação da SPRINT-10 — 2026-07-19

### Estado de ativação

- **Milestone:** M1 — Infraestrutura (`in_progress`).
- **SPRINT-10 — Snapshot Quality Gate Integrity:** `in_progress`.
- **Última Sprint concluída:** SPRINT-09 — Reproducible Container Baseline.
- **EPIC, Task ou DT formal:** nenhuma criada.
- **Baseline publicada de ativação:**
  `6464999e0657ac90a2175b9c698d2886119b4223`.
- **Quality Gate da baseline:** run `29704668788`, `success`.
- **Container Gate da baseline:** run `29704668667`, `success`.
- **Nova ADR:** não requerida.

### Defeito bloqueador

Na publicação final da SPRINT-09, uma execução de
`python tools/project_snapshot.py --check` informou internamente
`Pytest executado: Reprovado — 92 aprovado(s), 3 aviso(s)`, mas o comando ainda
retornou exit code zero e declarou o snapshot validado. Na mesma baseline, a suíte
independente concluiu `133 passed, 1 warning` e os gates remotos terminaram com
`success`; portanto, o defeito confirmado é o comportamento fail-open do gerador,
não uma reprovação da baseline publicada.

### Objetivo vinculante

Corrigir futuramente `tools/project_snapshot.py` para que qualquer falha nos gates
ao vivo de Ruff, Pytest ou importação:

- resulte em exit code diferente de zero;
- impeça a escrita do snapshot;
- impeça que `--check` declare validação;
- preserve o caminho de sucesso e o contrato determinístico existente.

O defeito está classificado como bloqueador antes da publicação de artefatos de
container.

### Limites desta ativação

Esta etapa é exclusivamente documental. Não estão autorizados nesta ativação:
implementação técnica, mudanças em `tools/project_snapshot.py`, alterações em
`apps/`, novas dependências, publicação em GHCR ou outro registry, Docker Compose,
deployment, SPRINT-11 ou push. A implementação técnica dependerá de autorização
humana específica após os dois commits de ativação.

## Fechamento da SPRINT-09 — 2026-07-19

### Estado final

- **M0 — Foundation:** `completed`, como fato histórico.
- **M1 — Infraestrutura:** `in_progress`.
- **SPRINT-09 — Reproducible Container Baseline:** `completed`.
- **Sprint ativa:** nenhuma.
- **Sprint planejada:** nenhuma.
- **Task ativa ou planejada:** nenhuma.
- **EPIC, Task ou DT criada na Sprint:** nenhuma.
- **SPRINT-10:** não autorizada.

A SPRINT-09 estabeleceu uma baseline reproduzível de container Linux sem alterar a
aplicação, dependências ou lock. A implementação publicada está no HEAD
`29b0ecef81b319d369064d16435676f73e03c7ad`.

### Entregas e arquitetura

- `Dockerfile` Linux multi-stage;
- `.dockerignore` restritivo;
- Python `3.14.6` no builder e runtime;
- inputs Python e uv pinados por digest completo para `linux/amd64`;
- `uv sync --locked --no-dev --no-editable` no builder;
- runtime com UID/GID numéricos `10001:10001`;
- filesystem somente leitura comprovado;
- healthcheck com biblioteca padrão do Python;
- contratos de `GET /`, `GET /api/v1/health`, Request ID e logs console/JSON;
- ausência de ferramentas e dependências de desenvolvimento na imagem runtime;
- Container Gate somente leitura, sem secrets, registry login, push de imagem,
  cache externo, artifacts, deployment ou comandos Git de escrita.

### Evidência remota

- Quality Gate run `29689585477`: `completed/success`, quatro jobs aprovados;
- Container Gate run `29689585471`: `completed/success`, job `container-gate`
  aprovado;
- ADR-0008 promovida para `Accepted` após satisfação integral dos critérios.

### Limites preservados

Nenhuma imagem foi publicada, nenhum deployment foi executado, Docker Compose e
registry não foram configurados, nenhuma dependência foi adicionada e o comportamento
da aplicação não mudou. M1 permanece em andamento e nenhum próximo incremento está
autorizado.

## SPRINT-07 — Dependency Reproducibility Proof

**Status:** `completed` e publicada

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Task ou DT formal:** nenhuma criada para esta Sprint

**Última entrega concluída:** SPRINT-07; a última Task formal permanece DT-009,
concluída na SPRINT-06

**Estado histórico no fechamento local:** nenhuma Sprint seguinte estava ativa; a SPRINT-08 ainda não havia sido autorizada.

Baseline publicada conhecida antes da SPRINT-07:
`9cfefa8bf117bceb11bcbd5df2a18cc28f82303c`.

Baseline experimental das duas resoluções:
`ea5a1ffc456075c6938905759b32059e8b7e2b85`.

Baseline oficial antes da adoção:
`7513489c294a20ce5ee5f8e293f8111fbaf95af1`, branch `main`, ahead 4,
behind 0 e working tree limpa.

**Resultados comprovados:**

- metadados do `pyproject.toml` confirmados sem alteração;
- duas resoluções independentes produziram locks byte-idênticos;
- `uv 0.11.28` utilizado com índice `https://pypi.org/simple` e cutoff
  `2026-07-14T11:53:48.187Z`;
- Windows Python `3.14.6` aprovado;
- Linux em Docker Desktop/WSL2 com Python `3.12.13`, `3.13.14` e `3.14.6`
  aprovado;
- Ruff, 76 testes com 1 warning conhecido, importação, endpoints, Request ID,
  logging e snapshot aprovados;
- exportação e consumo do `pylock.toml` pelo uv aprovados como evidência
  experimental;
- validação independente do Master 2 aprovada;
- `uv.lock` canônico adotado oficialmente no commit
  `cf5dfdae11ddcb77137f8d75b11606b73bfc43a2`;
- ADR-0006 aceito com política oficial de atualização do lock.

**Política oficial:**

- `pyproject.toml` permanece como fonte declarativa;
- `uv.lock` é o lock oficial e versionado;
- instalações reproduzíveis devem consumir o lock sem modificá-lo;
- atualizações exigem mudança planejada, versão do uv, índice, cutoff ou política
  temporal equivalente, revisão integral do diff, ambiente limpo, gates completos,
  documentação e commit específico;
- futura CI deverá consumir o lock em modo bloqueado e não regenerá-lo
  incidentalmente.

**Limitações registradas no fechamento local da SPRINT-07:**

- o estado atual do servidor remoto não foi confirmado;
- a prova Linux não ocorreu em host físico administrado separadamente;
- CI não foi implementada;
- interoperabilidade de terceiros do `pylock.toml` não foi comprovada;
- `pylock.toml` não foi adotado oficialmente;
- os commits do fechamento permanecem locais;
- nenhum `fetch`, `pull` ou `push` foi executado;
- SPRINT-08 não foi ativada.

## SPRINT-08 — Automated Quality Gate

**Status:** `completed` e publicada

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Task ou DT formal:** nenhuma criada para esta Sprint

**Objetivo concluído:** implementar, validar localmente e comprovar remotamente um
automated quality gate reproduzível e somente leitura no GitHub Actions.

**Implementação publicada:** commit
`49b5dd5d8d240f6bbb4784c97e1d1242add0d040`.

**Execução remota de aceitação:** GitHub Actions run `29663968493`, com status
`completed` e conclusão `success`.

**Matriz aprovada:**

- `ubuntu-latest` com Python `3.12`;
- `ubuntu-latest` com Python `3.13`;
- `ubuntu-latest` com Python `3.14`;
- `windows-latest` com Python `3.14`.

**Contratos comprovados:**

- triggers restritos a `push` em `main`, `pull_request` para `main` e
  `workflow_dispatch`;
- `permissions: contents: read`, sem permissões de escrita;
- Actions externas pinadas por SHA completo;
- `uv 0.11.28` e cutoff `2026-07-14T11:53:48.187Z`;
- `uv lock --check` e `uv sync --locked --all-extras`;
- snapshot check, Ruff, Pytest, importação e preservação dos arquivos rastreados;
- ausência de segredos, cache, artifacts, deployment, autofix e comandos Git de
  escrita;
- 43 testes contratuais do workflow e 119 testes totais aprovados;
- ADR-0007 aceita após comprovação remota integral.

**Continuidade histórica:** no fechamento da SPRINT-08, nenhuma Sprint estava ativa
ou planejada e a SPRINT-09 ainda não havia sido autorizada.

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

- Branch operacional: `main`.
- Upstream configurado: `origin/main`.
- Baseline publicada da SPRINT-09 confirmada em
  `29b0ecef81b319d369064d16435676f73e03c7ad`, com `HEAD`, `origin/main` e
  `remote main` sincronizados antes do fechamento documental final.
- Divergência confirmada nessa baseline: ahead `0`, behind `0`.
- Working tree, staging, tracked unstaged e untracked validados como limpos antes
  do fechamento; `.git/index.lock` ausente.
- Baseline antes da adoção oficial do lock: `7513489`.
- A adoção do lock e do ADR-0006 ocorreu no commit `cf5dfda`, integrado à
  baseline publicada.
- A SPRINT-07 está publicada na baseline `85ef2616`.
- A implementação do quality gate está publicada em `49b5dd5`.
- O fechamento documental da SPRINT-08 está publicado em `31e4afd`.
- A baseline final publicada e sincronizada da SPRINT-08 é `df23d72`.
- O quality gate da baseline final da SPRINT-08 foi aprovado no run `29664949487`.
- A SPRINT-09 foi ativada em `fb3d63c`, recebeu snapshot em `68494de`, implementação
  de container em `ff01f10` e snapshot de implementação em `29b0ece`.
- A publicação de `29b0ece` foi comprovada por `git ls-remote`; Quality Gate
  `29689585477` e Container Gate `29689585471` concluíram com `success`.
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

### `cf5dfda`

`uv.lock` canônico adotado como lock oficial, ADR-0006 criado e índice de decisões
arquiteturais atualizado. O commit integra a baseline publicada.

### `61fa4b5`

Fechamento documental da SPRINT-07 — Dependency Reproducibility Proof.

### `85ef261`

Snapshot final da SPRINT-07 publicado e adotado como baseline da SPRINT-08.

### `50bc0d9`

Ativação documental da SPRINT-08 — Automated Quality Gate.

### `9359c1d`

Snapshot atualizado após a ativação da SPRINT-08.

### `49b5dd5`

Workflow reproduzível, testes contratuais, ADR-0007 proposta e snapshot da
implementação do quality gate.

### `31e4afd`

Fechamento documental da SPRINT-08 — Automated Quality Gate.

### `df23d72`

Snapshot final da SPRINT-08 publicado e adotado como baseline de ativação da
SPRINT-09.

### `fb3d63c`

M0 encerrado, M1 iniciado e SPRINT-09 ativada documentalmente.

### `68494de`

Snapshot atualizado após a ativação da SPRINT-09.

### `ff01f10`

Baseline reproduzível de container implementada com Dockerfile, `.dockerignore`,
Container Gate, testes contratuais e ADR-0008 proposta.

### `29b0ece`

Snapshot atualizado após a implementação e publicado como baseline remota de
aceitação da SPRINT-09.

## Trabalho concluído histórico

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

## Sprint concluída anterior

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
- Ao término da SPRINT-06, nenhuma Sprint estava ativa.

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

- 133 testes coletados;
- 133 testes aprovados;
- 1 aviso de depreciação do `TestClient`;
- 43 testes contratuais do Quality Gate;
- 14 testes contratuais da baseline e do Container Gate;
- Quality Gate run `29689585477` e Container Gate run `29689585471` aprovados.

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
- ADR-0006 — `uv.lock` como lock oficial de dependências.
- ADR-0007 — GitHub Actions como quality gate reproduzível e somente leitura.
- ADR-0008 — baseline reproduzível de container Linux.

O `pyproject.toml` permanece como fonte declarativa, e o `uv.lock` passa a ser o
artefato oficial de resolução reproduzível. Atualizações do lock são deliberadas,
auditáveis e separadas de mudanças funcionais. O `pylock.toml` permanece experimental.

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

- M0 — Foundation: `completed`.
- M1 — Infraestrutura: `in_progress`.
- M2 a M8: `pending`.

## Estado operacional corrente

- Última Sprint concluída: SPRINT-09 — Reproducible Container Baseline.
- Sprint ativa: SPRINT-10 — Snapshot Quality Gate Integrity (`in_progress`).
- Sprint planejada: nenhuma.
- Task ativa ou planejada: nenhuma.
- M0 — Foundation: `completed` como fato histórico.
- M1 — Infraestrutura: `in_progress`.
- Implementação técnica da SPRINT-10: não autorizada nesta ativação.
- Publicação de artefatos, Docker Compose e deployment: não autorizados.

A continuidade deve partir deste documento, do Project State, do handoff da
SPRINT-09, dos ADRs aceitos e da validação direta do Git. O próximo gate é a
autorização humana para a implementação técnica da SPRINT-10.

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
