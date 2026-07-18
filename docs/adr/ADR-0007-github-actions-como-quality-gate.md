# ADR-0007 — GitHub Actions como quality gate

- **Status:** Accepted
- **Data:** 18/07/2026
- **Escopo:** M0 — Foundation / SPRINT-08 — Automated Quality Gate

## Contexto

O Hermes AI OS já possuía `pyproject.toml` como fonte declarativa, `uv.lock` como
resolução oficial e gates locais para Ruff, Pytest, importação e snapshot. Antes da
SPRINT-08, esses contratos ainda não eram executados de forma automatizada e
reproduzível no repositório remoto.

A SPRINT-08 deve introduzir esse controle sem modificar aplicação, dependências,
lockfile ou permissões de escrita.

## Decisão

Adotar GitHub Actions como quality gate inicial e somente leitura.

O workflow ficará em `.github/workflows/quality-gate.yml` e será disparado apenas
por `push` em `main`, `pull_request` direcionado a `main` e
`workflow_dispatch`.

Não serão usados `pull_request_target`, agendamentos, deployment, release,
artifacts, cache, segredos, filtros de caminhos ou publicação de pacotes.

## Matriz aprovada

| Sistema | Python |
|---|---|
| `ubuntu-latest` | `3.12` |
| `ubuntu-latest` | `3.13` |
| `ubuntu-latest` | `3.14` |
| `windows-latest` | `3.14` |

A estratégia usa `fail-fast: false`.

## Instalação reproduzível

O workflow instala Python explicitamente, instala `uv 0.11.28`, aplica o cutoff
`2026-07-14T11:53:48.187Z`, executa `uv lock --check` e sincroniza com
`uv sync --locked --all-extras`.

O `pyproject.toml` permanece declarativo e o `uv.lock` não pode ser regenerado
ou modificado pelo gate.

## Segurança e supply chain

As Actions externas ficam pinadas por SHA completo:

- `actions/checkout` v7.0.0:
  `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0`;
- `actions/setup-python` v6.3.0:
  `ece7cb06caefa5fff74198d8649806c4678c61a1`;
- `astral-sh/setup-uv` v8.3.2:
  `11f9893b081a58869d3b5fccaea48c9e9e46f990`.

O workflow define somente:

```yaml
permissions:
  contents: read
```

O checkout usa `persist-credentials: false`.

## Gates executados

1. checkout;
2. setup do Python;
3. setup do uv;
4. lock check;
5. sincronização bloqueada;
6. snapshot check;
7. Ruff sem autofix;
8. Pytest sem cacheprovider;
9. importação da aplicação;
10. confirmação de que arquivos rastreados não foram modificados.

## Consequências

### Positivas

- falha fechada e reproduzível;
- cobertura da matriz Python aprovada;
- evidência remota independente;
- proteção automática do lock, snapshot e contratos da aplicação;
- permissões mínimas e supply chain auditável.

### Custos e limitações

- quatro combinações aumentam o tempo de execução;
- cache permanece desabilitado;
- dependência operacional do GitHub Actions;
- runners Linux hospedados não equivalem a host físico separado.

## Rollback

O rollback deve ocorrer por commit Git normal, sem amend, rebase, reset destrutivo
ou force push.

## Evidência de aceitação

A decisão foi aceita após a publicação normal da implementação em `main` no commit
`49b5dd5d8d240f6bbb4784c97e1d1242add0d040` e a conclusão integral do GitHub
Actions run `29663968493`.

As quatro combinações foram aprovadas:

- `ubuntu-latest` / Python `3.12`;
- `ubuntu-latest` / Python `3.13`;
- `ubuntu-latest` / Python `3.14`;
- `windows-latest` / Python `3.14`.

Todos os passos obrigatórios concluíram com `success`. A auditoria também confirmou:

- somente `permissions: contents: read`;
- ausência de segredos, cache, artifacts e deployment;
- ausência de autofix e comandos Git de escrita;
- `pyproject.toml`, `uv.lock`, `apps/` e `.venv` oficial preservados;
- suíte local com 119 testes aprovados e 1 warning conhecido;
- snapshot, Ruff, importação, endpoints, Request ID e logging aprovados.

A ADR-0007 passa, portanto, de `Proposed` para `Accepted` no fechamento da
SPRINT-08.
