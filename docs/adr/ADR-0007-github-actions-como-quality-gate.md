# ADR-0007 — GitHub Actions como quality gate

- **Status:** Proposed
- **Data:** 18/07/2026
- **Escopo:** M0 — Foundation / SPRINT-08 — Automated Quality Gate

## Contexto

O Hermes AI OS já possui `pyproject.toml` como fonte declarativa, `uv.lock` como
resolução oficial e gates locais para Ruff, Pytest, importação e snapshot. Ainda
não existe execução automatizada e reproduzível desses contratos no repositório
remoto.

A SPRINT-08 deve introduzir esse controle sem modificar aplicação, dependências,
lockfile ou permissões de escrita.

## Decisão proposta

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

## Critérios para Accepted

Esta ADR somente poderá mudar de `Proposed` para `Accepted` quando:

- os arquivos forem publicados normalmente em `main`;
- as quatro combinações concluírem com sucesso;
- todos os passos obrigatórios forem comprovados;
- nenhuma permissão de escrita, segredo, cache, artifact ou deployment for usado;
- `pyproject.toml`, `uv.lock`, `apps/` e a `.venv` oficial permanecerem preservados;
- o resultado remoto for registrado no fechamento da SPRINT-08.
