# Hermes AI OS — Handoff da SPRINT-09

> **Data:** 19/07/2026
>
> **Sprint:** SPRINT-09 — Reproducible Container Baseline
>
> **Status:** `completed`
>
> **Milestone:** M1 — Infraestrutura (`in_progress`)
>
> **Baseline publicada:** `29b0ecef81b319d369064d16435676f73e03c7ad`

## 1. Identificação do projeto

O Hermes AI OS permanece na versão `0.0.1`, com modelo Open Core e operação Local
First / Cloud Ready. A SPRINT-09 não criou EPIC, Task ou DT formal.

## 2. Baseline inicial da Sprint

A ativação partiu da baseline final da SPRINT-08:
`df23d729069a637e914052ffc6a5a0d6d21ddf1d`.

## 3. Transição M0 → M1

M0 — Foundation foi registrado como `completed` por evidências históricas. M1 —
Infraestrutura foi iniciado e permanece `in_progress`; a conclusão da SPRINT-09 não
conclui M1.

## 4. Ativação da SPRINT-09

- `fb3d63c84ea479c456c13313fd580311176f1279` — fechamento do M0 e ativação;
- `68494de610d4270112b55bd916834b7e3178288e` — snapshot da ativação.

## 5. Escopo executado

Foi criada e validada uma baseline reproduzível de container Linux para a aplicação
FastAPI existente, sem alterar aplicação, dependências ou lock.

## 6. Arquivos implementados

- `Dockerfile`;
- `.dockerignore`;
- `.github/workflows/container-gate.yml`;
- `tests/test_container_baseline.py`;
- `tests/test_container_gate_workflow.py`;
- `docs/adr/ADR-0008-reproducible-container-baseline.md`;
- `docs/adr/README.md`.

## 7. Imagens e digests

```text
python:3.14.6-slim-trixie@sha256:d4fea6e20c09820028eea3f5c17f5b8ebd2ecb9c2bf28e561681a74a96090e4f
ghcr.io/astral-sh/uv:0.11.28@sha256:5c3ab83183a73c5d319a77009eb425b60d5bb937f339fb7876788ebf567baf48
PLATFORM=linux/amd64
```

## 8. Arquitetura do Dockerfile

O Dockerfile é multi-stage. Builder e runtime usam a mesma imagem Python. O uv é
copiado somente para o builder, que executa `uv sync --locked --no-dev
--no-editable`. O runtime recebe somente o ambiente instalado e `apps/backend`.

## 9. Política do `.dockerignore`

Git, workflows não necessários ao contexto, ambientes virtuais, caches, logs,
dados temporários, testes, documentação, experimentos e arquivos locais são
excluídos. `pyproject.toml`, `uv.lock` e `apps/backend` permanecem no contexto.

## 10. Testes contratuais

Foram adicionados 14 testes: 7 para a baseline do container e 7 para o workflow do
Container Gate. A suíte final coletou e aprovou 133 testes, com 1 warning conhecido.

## 11. Docker local

O build final sem cache foi aprovado com Docker Linux `amd64`. A imagem foi
inspecionada e executada localmente em modo somente leitura.

## 12. Usuário não root

A imagem configura e executa UID/GID `10001:10001`.

## 13. Filesystem read-only

A aplicação iniciou e permaneceu saudável com `--read-only` e sem escrita auxiliar
obrigatória.

## 14. Healthcheck

O healthcheck usa a biblioteca padrão do Python e terminou em `healthy`.

## 15. Endpoints

`GET /` e `GET /api/v1/health` retornaram HTTP 200 no runtime local e no Container
Gate.

## 16. Request ID

Foi comprovada a geração automática de Request ID e a preservação do valor enviado
pelo cliente.

## 17. Logging console e JSON

Os dois formatos produziram linhas válidas e correlacionadas por Request ID.

## 18. Inventário do runtime

O inventário das distribuições Python foi coletado. `pytest`, `ruff`, `httpx` e uv
não estão presentes, comprovando a ausência de ferramentas e dependências de
desenvolvimento na imagem runtime.

## 19. Quality Gate

GitHub Actions run `29689585477`, evento `push`, branch `main`, HEAD `29b0ece`,
status `completed`, conclusão `success`, com quatro jobs aprovados.

## 20. Container Gate

GitHub Actions run `29689585471`, evento `push`, branch `main`, HEAD `29b0ece`,
status `completed`, conclusão `success`, com o job `container-gate` aprovado.

## 21. Commits publicados

- `fb3d63c` — ativação documental;
- `68494de` — snapshot da ativação;
- `ff01f10` — implementação do container;
- `29b0ece` — snapshot da implementação e baseline publicada.

Os hashes dos dois commits finais de fechamento são determinados pelo Git após sua
criação e registrados no relatório externo pré-push, evitando autorreferência.

## 22. ADR-0008

A ADR-0008 foi promovida para `Accepted` após os dois gates remotos aprovados. A
decisão técnica implementada não foi alterada no fechamento.

## 23. Arquivos protegidos preservados

`pyproject.toml`, `uv.lock`, `apps/`, Quality Gate, gerador do snapshot, testes
técnicos existentes e ADR-0001 até ADR-0007 permaneceram preservados.

## 24. Itens fora do escopo

```text
IMAGE_PUBLISHED=NAO
DEPLOYMENT_EXECUTED=NAO
COMPOSE_IMPLEMENTED=NAO
REGISTRY_CONFIGURED=NAO
NEW_DEPENDENCIES=NAO
APPLICATION_BEHAVIOR_CHANGED=NAO
```

## 25. Estado documental final

- M0 — Foundation: `completed` como fato histórico;
- M1 — Infraestrutura: `in_progress`;
- SPRINT-09: `completed`;
- Sprint ativa: nenhuma;
- Sprint planejada: nenhuma;
- Task ativa ou planejada: nenhuma;
- última Sprint concluída: SPRINT-09.

## 26. Estado Git antes do fechamento

Antes das escritas documentais, `HEAD`, `origin/main` e `remote main` estavam em
`29b0ecef81b319d369064d16435676f73e03c7ad`, com ahead `0`, behind `0`, working
tree limpa, staging vazio, untracked vazio e `index.lock` ausente.

## 27. Continuidade

A SPRINT-10 não está autorizada. Nenhum próximo incremento está ativo ou planejado.
A retomada deve começar pelos documentos vivos, ADRs aceitos, snapshot e estado Git
real.
