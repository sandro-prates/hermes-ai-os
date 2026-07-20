# Hermes AI OS — Handoff da SPRINT-10

> **Data:** 20/07/2026
>
> **Sprint:** SPRINT-10 — Snapshot Quality Gate Integrity
>
> **Status:** `completed`
>
> **Milestone:** M1 — Infraestrutura (`in_progress`)
>
> **Baseline técnica publicada:** `cb2171f315430c977ca929ffb468363a0d5f079e`

## 1. Identificação do projeto

O Hermes AI OS permanece na versão `0.0.1`, com modelo Open Core e orientação Local
First / Cloud Ready. A SPRINT-10 não criou EPIC, Task/DT formal ou ADR.

## 2. Objetivo concluído

A Sprint eliminou o comportamento fail-open dos gates ao vivo executados por
`tools/project_snapshot.py`.

Ruff, Pytest e importação agora são obrigatoriamente fail-closed:

- qualquer reprovação retorna exit code diferente de zero;
- nenhuma reprovação permite escrita do snapshot;
- nenhuma reprovação permite que `--check` declare validação;
- o caminho integralmente aprovado continua gerando e validando o relatório.

## 3. Defeito de origem

A ativação foi motivada por uma execução histórica de
`python tools/project_snapshot.py --check` que registrou Pytest interno reprovado,
mas retornou exit code zero e declarou o snapshot validado.

A suíte independente da mesma baseline estava aprovada. O defeito era a ausência de
propagação fechada da falha pelo gerador, e não uma reprovação da baseline publicada.

## 4. Baseline e commits comprovados

- baseline publicada anterior:
  `6464999e0657ac90a2175b9c698d2886119b4223`;
- ativação documental:
  `f5e2da5c5ba419711d3c2e97309a152bec7e1965`;
- snapshot da ativação:
  `a466ac52ff36ea0b1be95fbee8985dcacb18017e`;
- implementação técnica:
  `513afbaf64b11156d1859ed2bec8c85fff3cac7f`;
- snapshot pós-implementação publicado:
  `cb2171f315430c977ca929ffb468363a0d5f079e`.

## 5. Implementação técnica

Arquivos técnicos alterados pela Sprint:

```text
tools/project_snapshot.py
tests/test_project_snapshot.py
```

A implementação preserva:

- schema 3 do snapshot;
- projeção determinística da árvore commitada;
- uso de `git ls-tree HEAD`;
- exclusão autorreferencial de `docs/PROJECT_SNAPSHOT.md`;
- geração e `--check` no caminho de sucesso;
- contratos públicos existentes da aplicação.

## 6. Cobertura de regressão

Foram comprovados:

- 24 testes negativos específicos do comportamento fail-closed;
- falha de Ruff na geração;
- falha de Pytest na geração;
- falha de importação na geração;
- falha de Ruff em `--check`;
- falha de Pytest em `--check`;
- falha de importação em `--check`;
- preservação do arquivo quando qualquer gate reprova;
- retorno diferente de zero nos caminhos de falha.

`tests/test_project_snapshot.py` concluiu com 77 testes aprovados.

## 7. Validação local

A baseline publicada foi validada com:

- Python `3.14.6`;
- 161 testes aprovados;
- 1 `StarletteDeprecationWarning` conhecido e não bloqueante;
- Ruff aprovado;
- importação aprovada: FastAPI Hermes AI OS `0.0.1`;
- geração do snapshot aprovada;
- `--check --audit-working-tree` aprovado;
- `git diff --check` aprovado.

## 8. Aceitação remota

### Quality Gate

- run: `29723471112`;
- commit: `cb2171f315430c977ca929ffb468363a0d5f079e`;
- evento: `push`;
- branch: `main`;
- status: `completed`;
- conclusão: `success`;
- jobs aprovados:
  - `ubuntu-latest / Python 3.14`;
  - `windows-latest / Python 3.14`;
  - `ubuntu-latest / Python 3.13`;
  - `ubuntu-latest / Python 3.12`.

### Container Gate

- run: `29723471158`;
- commit: `cb2171f315430c977ca929ffb468363a0d5f079e`;
- evento: `push`;
- branch: `main`;
- status: `completed`;
- conclusão: `success`;
- job aprovado: `container-gate`.

## 9. Estado operacional

```text
project.phase.id=M1
project.phase.name=Infraestrutura
project.phase.status=in_progress
work.active.sprint=null
work.active.task=null
work.last_completed.sprint=SPRINT-10
work.last_completed.task=null
work.planned.sprint=null
work.planned.task=null
```

M0 — Foundation permanece `completed` somente como fato histórico.

## 10. Arquitetura preservada

- aplicação FastAPI em `apps/backend/app`;
- endpoints `GET /` e `GET /api/v1/health`;
- Settings com `pydantic-settings`;
- observabilidade central com logging console/JSON;
- middleware ASGI e correlação por `ContextVar`;
- geração, preservação e retorno de Request ID;
- `pyproject.toml` como fonte declarativa;
- `uv.lock` como lock oficial;
- Quality Gate reproduzível e somente leitura;
- baseline reproduzível de container Linux;
- Container Gate somente leitura;
- ADR-0001 a ADR-0008 permanecem `Accepted`.

## 11. Arquivos e áreas não alterados

A implementação da SPRINT-10 não alterou:

```text
apps/**
pyproject.toml
uv.lock
.github/workflows/**
Dockerfile
.dockerignore
docs/adr/**
```

Nenhuma dependência foi adicionada. Nenhuma imagem foi publicada. Nenhum registry,
Docker Compose ou deployment foi configurado.

## 12. Documentação de continuidade

Fontes obrigatórias para retomada:

1. `README.md`;
2. `docs/00_PROJECT_MASTER.md`;
3. `docs/01_PROJECT_STATE.yaml`;
4. `docs/02_BACKLOG.md`;
5. `docs/03_CHANGELOG.md`;
6. `docs/HANDOFF_2026-07-20-SPRINT-10.md`;
7. `docs/PROJECT_SNAPSHOT.md`;
8. ADRs aceitos em `docs/adr/`;
9. estado direto do Git.

## 13. Limitações atuais

- M1 — Infraestrutura continua em andamento;
- publicação de imagem permanece não autorizada;
- registry, Docker Compose e deployment não foram implementados;
- banco de dados, runtime de agentes, memória, dashboard e integrações externas não
  estão implementados;
- SPRINT-11 não está ativa nem planejada.

## 14. Regra de retomada

Antes de iniciar qualquer novo incremento:

1. ler os documentos de continuidade;
2. executar `git status --short --branch`;
3. comparar `HEAD`, `origin/main` e remoto;
4. validar o snapshot;
5. confirmar os gates aplicáveis;
6. obter autorização humana explícita.

Nenhuma SPRINT-11 ou outra implementação está autorizada por este handoff.
