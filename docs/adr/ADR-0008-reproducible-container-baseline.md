# ADR-0008 — Baseline reproduzível de container

- **Status:** Accepted
- **Data:** 19/07/2026
- **Escopo:** M0 → M1 / SPRINT-09 — Reproducible Container Baseline

## Contexto

O projeto possui uma aplicação FastAPI, um pyproject.toml declarativo, o
uv.lock como resolução oficial e um quality gate remoto. A transição de M0 para
M1 exige um artefato de execução Linux reproduzível, verificável localmente e no
GitHub Actions, sem alterar a aplicação ou a resolução de dependências.

## Decisão

Adotar um Dockerfile Linux multi-stage. A imagem oficial python:3.14.6-slim-trixie
é usada no builder e no runtime, fixada para linux/amd64 em
sha256:d4fea6e20c09820028eea3f5c17f5b8ebd2ecb9c2bf28e561681a74a96090e4f.
O uv oficial ghcr.io/astral-sh/uv:0.11.28 é copiado somente para o builder,
fixado em sha256:5c3ab83183a73c5d319a77009eb425b60d5bb937f339fb7876788ebf567baf48.
Os manifestos foram inspecionados e ambos possuem manifesto linux/amd64.

O builder copia pyproject.toml e uv.lock antes do código e executa
uv sync --locked --no-dev --no-editable. O runtime recebe apenas o ambiente
instalado e apps/backend, usa UID/GID numéricos não-root, expõe a porta 8000 e
possui healthcheck com a biblioteca padrão do Python. O runtime não contém uv,
testes ou documentação e é compatível com filesystem somente leitura.

O uv.lock oficial permanece inalterado. Não será usado Compose, registry,
deployment ou segredo nesta baseline.

## Consequências

### Positivas

- entradas de imagem e dependências são auditáveis;
- dev tools não entram no runtime;
- o mesmo contrato é validado localmente e pelo Container Gate;
- execução não-root e somente leitura reduzem a superfície operacional.

### Limitações

- a evidência local e remota cobre linux/amd64;
- os digests identificam entradas imutáveis, mas não tornam disponibilidade futura
  do registry garantida;
- a baseline não fornece publicação, deployment, persistência ou orquestração;
- a aceitação desta ADR depende de Quality Gate e Container Gate remotos aprovados.

## Política de atualização de digest

Atualizações devem ser deliberadas, registrar tag, digest completo, manifesto,
plataformas e data de verificação, executar todos os gates e preservar o lock.
Tags móveis nunca devem ser usadas sem digest.

## Rollback

O rollback é feito por commit Git normal que restaure o Dockerfile e os testes para
os digests anteriores. Não requer operação destrutiva, registry ou alteração da
aplicação.

## Critérios de aceitação

1. Dockerfile e .dockerignore satisfazem seus contratos estáticos.
2. O build local com os dois digests passa sem cache externo.
3. A imagem inicia com filesystem somente leitura e usuário não-root.
4. Healthcheck, /, /api/v1/health, Request ID e os dois formatos de log passam.
5. Pytest, Ruff e auditoria do snapshot passam sem alterar arquivos protegidos.
6. O Container Gate remoto e o Quality Gate remoto passam após publicação.

## Evidência de aceitação

- **Implementation HEAD:** `29b0ecef81b319d369064d16435676f73e03c7ad`;
- **Quality Gate:** run `29689585477` — `success`;
- **Container Gate:** run `29689585471` — `success`;
- **Python image:**
  `python:3.14.6-slim-trixie@sha256:d4fea6e20c09820028eea3f5c17f5b8ebd2ecb9c2bf28e561681a74a96090e4f`;
- **uv image:**
  `ghcr.io/astral-sh/uv:0.11.28@sha256:5c3ab83183a73c5d319a77009eb425b60d5bb937f339fb7876788ebf567baf48`.

O último critério foi comprovado pela publicação normal da baseline e pelos dois
workflows remotos concluídos com sucesso. A decisão é aceita sem alteração do
contrato técnico implementado.
