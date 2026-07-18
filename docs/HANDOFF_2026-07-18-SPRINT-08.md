# Hermes AI OS — Project Handoff — SPRINT-08

## 1. Estado geral

- **Projeto:** Hermes AI OS
- **Versão:** 0.0.1
- **Milestone:** M0 — Foundation
- **Sprint encerrada:** SPRINT-08 — Automated Quality Gate
- **Status:** `completed`
- **EPIC nova:** nenhuma
- **Task ou DT formal nova:** nenhuma
- **Próxima Sprint:** não autorizada
- **Data do fechamento:** 18/07/2026

A SPRINT-08 implementou e comprovou um quality gate reproduzível e somente leitura
no GitHub Actions. Nenhuma funcionalidade de produto, dependência ou permissão de
escrita foi adicionada.

## 2. Baseline inicial

A ativação partiu da baseline publicada:

```text
85ef2616bdfe4573d9bf8bf2abecde06e76aac6a
```

Condições comprovadas antes da ativação:

- branch `main`;
- `HEAD`, `origin/main` e `remote main` sincronizados;
- ahead `0`, behind `0`;
- working tree e staging limpos;
- `.git/index.lock` ausente;
- Python local `3.14.6`;
- Ruff aprovado;
- 76 testes aprovados e 1 warning conhecido;
- importação e snapshot aprovados;
- `uv 0.11.28`;
- `uv.lock` com `135871 bytes` e SHA-256
  `6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`.

## 3. Escopo executado

O escopo ficou restrito a:

- ativação e fechamento documental da SPRINT-08;
- workflow GitHub Actions;
- testes automatizados do contrato do workflow;
- ADR-0007;
- matriz aprovada de sistemas e versões Python;
- consumo bloqueado do `uv.lock`;
- gates de snapshot, Ruff, Pytest e importação;
- verificação de que arquivos rastreados não são modificados;
- publicação normal e inspeção remota.

Não houve alteração em `apps/`, `pyproject.toml`, `uv.lock` ou dependências.

## 4. Arquivos implementados

- `.github/workflows/quality-gate.yml`;
- `tests/test_quality_gate_workflow.py`;
- `docs/adr/ADR-0007-github-actions-como-quality-gate.md`;
- `docs/adr/README.md`;
- documentação viva e snapshots pelo fluxo oficial.

## 5. Workflow

Nome:

```text
Quality Gate
```

Triggers:

- `push` em `main`;
- `pull_request` direcionado a `main`;
- `workflow_dispatch`.

Permissões:

```yaml
permissions:
  contents: read
```

A estratégia usa `fail-fast: false` e timeout de 20 minutos por job.

## 6. Matriz comprovada

| Sistema | Python | Resultado no run 29663968493 |
|---|---:|---|
| `ubuntu-latest` | `3.12` | `success` |
| `ubuntu-latest` | `3.13` | `success` |
| `ubuntu-latest` | `3.14` | `success` |
| `windows-latest` | `3.14` | `success` |

A simulação local externa do job Windows também foi repetida com Python real
`3.14.6`, após uma primeira tentativa ter utilizado 3.12.8 e ter sido corretamente
rejeitada como evidência do job 3.14.

## 7. Actions, versões e SHAs

| Action | Versão | SHA completo |
|---|---|---|
| `actions/checkout` | `v7.0.0` | `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0` |
| `actions/setup-python` | `v6.3.0` | `ece7cb06caefa5fff74198d8649806c4678c61a1` |
| `astral-sh/setup-uv` | `v8.3.2` | `11f9893b081a58869d3b5fccaea48c9e9e46f990` |

O checkout usa `persist-credentials: false`.

## 8. Instalação reproduzível

O gate utiliza:

```text
uv 0.11.28
UV_EXCLUDE_NEWER=2026-07-14T11:53:48.187Z
PYTHONPATH=apps/backend
```

Comandos de dependências:

```text
uv lock --check
uv sync --locked --all-extras
```

O gate não regenera deliberadamente o lock e consome a resolução versionada.

## 9. Comandos do gate

Ordem obrigatória:

```text
uv lock --check
uv sync --locked --all-extras
uv run --locked python tools/project_snapshot.py --check
uv run --locked ruff check . --no-cache
uv run --locked python -m pytest -p no:cacheprovider
uv run --locked python -c "from app.main import app; ..."
git diff --exit-code -- .
```

## 10. Testes e gates locais

Resultados antes da primeira publicação:

- 43 testes contratuais do workflow aprovados;
- 119 testes totais aprovados;
- 1 warning de depreciação conhecido e não ocultado;
- Ruff aprovado;
- snapshot check aprovado;
- importação `Hermes AI OS 0.0.1` aprovada;
- `GET /` aprovado;
- `GET /api/v1/health` aprovado;
- Request ID gerado e preservado;
- logging console aprovado;
- logging JSON aprovado;
- hashes de `pyproject.toml`, `uv.lock` e `.venv` oficial preservados.

## 11. Commits principais

```text
50bc0d9 docs(project): activate sprint 08 automated quality gate
9359c1d docs(project): refresh snapshot after sprint 08 activation
49b5dd5 ci(quality): add reproducible automated quality gate
```

O fechamento documental usa o commit:

```text
docs(project): close sprint 08 automated quality gate
```

O snapshot final usa commit exclusivo:

```text
docs(project): refresh sprint 08 final snapshot
```

Os hashes dos dois commits finais são determinados pelo Git após sua criação e
registrados no relatório externo final, evitando autorreferência documental.

## 12. Publicação e execução remota de aceitação

A implementação foi publicada normalmente em `main` no commit:

```text
49b5dd5d8d240f6bbb4784c97e1d1242add0d040
```

Execução de aceitação:

```text
Run ID: 29663968493
Status: completed
Conclusion: success
Jobs: 4
```

Todos os jobs executaram com sucesso:

- checkout;
- setup do Python;
- setup do uv;
- lock check;
- sincronização bloqueada;
- snapshot check;
- Ruff;
- Pytest;
- importação;
- preservação da árvore rastreada.

## 13. Segurança e permissões

Foi comprovada a ausência de:

- segredos;
- cache;
- upload ou download de artifacts;
- deployment;
- permissões de escrita;
- comandos Git de escrita;
- autofix;
- publicação de pacotes;
- filtros de caminhos que evitassem o gate.

Nenhum force push foi autorizado ou executado.

## 14. ADR-0007

A ADR-0007 foi criada como `Proposed` e somente mudou para `Accepted` depois da
publicação da implementação e da aprovação integral do run `29663968493`.

Decisão aceita: usar GitHub Actions como quality gate reproduzível, somente leitura,
com Actions pinadas por SHA completo e consumo bloqueado do lock oficial.

## 15. Preservação comprovada

- `pyproject.toml`: inalterado;
- `uv.lock`: inalterado;
- `apps/`: inalterado;
- `.venv` oficial: preservada;
- ADR-0006: preservada;
- warning conhecido: não ocultado;
- dependências novas: nenhuma.

## 16. Limitações

- runners Linux hospedados não equivalem a host físico Linux separado;
- o quality gate inicial não usa cache;
- não há artifacts, deployment ou entrega contínua;
- a interoperabilidade de terceiros do `pylock.toml` continua não comprovada;
- `pylock.toml` não foi adotado oficialmente;
- o warning do `TestClient` permanece conhecido e não bloqueante.

## 17. Decisões não tomadas

A SPRINT-08 não decidiu ou iniciou:

- banco de dados;
- migrations;
- filas ou workers;
- runtime de agentes;
- memória;
- dashboard;
- integrações;
- cloud deployment;
- marketplace;
- recursos Enterprise;
- nova política de release;
- SPRINT-09.

## 18. Estado documental final

```text
work.active.sprint=null
work.active.task=null
work.last_completed.sprint=SPRINT-08
work.planned.sprint=null
work.planned.task=null
ADR-0007=Accepted
SPRINT-09=inactive
```

## 19. Estado Git de continuidade

Antes do fechamento documental:

```text
HEAD=origin/main=remote main=49b5dd5d8d240f6bbb4784c97e1d1242add0d040
ahead=0
behind=0
working tree=clean
staging=empty
index.lock=absent
```

Após os commits finais e o push normal, o Executor deve confirmar novamente:

- `HEAD = origin/main = remote main`;
- ahead `0`, behind `0`;
- working tree e staging limpos;
- workflow final integralmente verde.

Os hashes finais e a execução disparada pelo push de fechamento são registrados no
relatório externo final, evitando autorreferência neste handoff.

## 20. Continuidade

Nenhuma Sprint está ativa ou planejada. A SPRINT-09 não está autorizada.

Uma nova Sprint somente pode começar após definição explícita de escopo e autorização
humana. A retomada deve começar pela leitura da documentação viva, dos ADRs aceitos e
pela validação direta do Git.
