# Hermes AI OS

Hermes AI OS é uma plataforma em desenvolvimento para criação, orquestração e
execução de agentes de Inteligência Artificial. O projeto busca combinar operação
**Local First**, evolução **Cloud Ready** e um modelo de negócio **Open Core**.

## Status

- Versão atual: `0.0.1`.
- Fase atual: `M1 — Infraestrutura`.
- `M0 — Foundation` concluído como fato histórico; `M1 — Infraestrutura`
  permanece em andamento.
- API FastAPI executável localmente.
- EPIC-003 / SPRINT-02 (Logging System) concluída.
- SPRINT-03 — Reproducible Onboarding Baseline concluída na EPIC-004.
- DT-008 concluída no commit `2ebed11`, com `.env.example` sanitizado e dois testes
  contratuais.
- EPIC-004 concluída; seu único incremento formal foi atendido pela SPRINT-03 e DT-008.
- SPRINT-04 — Foundation Integrity Baseline concluída no M0, sem nova EPIC.
- SPRINT-05 — Technology Decision Baseline concluída no M0, sem nova EPIC.
- SPRINT-06 — Continuity State Integrity concluída no M0, sem nova EPIC.
- DT-009 — Integridade do estado de continuidade concluída na SPRINT-06.
- SPRINT-07 — Dependency Reproducibility Proof concluída e publicada no commit
  `85ef261`.
- O `uv.lock` canônico foi adotado como lock oficial no commit `cf5dfda`,
  enquanto o `pyproject.toml` permanece como fonte declarativa.
- SPRINT-08 — Automated Quality Gate concluída no M0, sem nova EPIC ou Task formal.
  A implementação foi publicada no commit `49b5dd5`, e as quatro combinações da
  matriz foram aprovadas no GitHub Actions run `29663968493`.
- A baseline final da SPRINT-08 foi publicada no commit `df23d72`; o quality gate
  dessa baseline foi aprovado no GitHub Actions run `29664949487`.
- SPRINT-09 — Reproducible Container Baseline concluída e publicada em M1, sem
  nova EPIC ou Task/DT formal. A implementação está na baseline `29b0ece`, com
  Quality Gate `29689585477` e Container Gate `29689585471` aprovados.
- ADR-0008 — Baseline reproduzível de container aceita após comprovação local e
  remota.
- SPRINT-10 — Snapshot Quality Gate Integrity ativa em M1, sem nova EPIC ou
  Task/DT formal; a implementação técnica ainda não foi iniciada.
- O comportamento fail-open dos gates ao vivo de `tools/project_snapshot.py` está
  classificado como bloqueador antes da publicação de artefatos de container.
- DT-007 foi concluída como pesquisa no commit `126aff8`; suas recomendações somente
  se tornaram oficiais quando aprovadas e comprovadas na SPRINT-07.

## Funcionalidades implementadas

- API HTTP com endpoints raiz e de health check.
- Settings centralizados com `pydantic-settings` e suporte a arquivo `.env`.
- Logging central configurado com `logging.config.dictConfig`.
- Logs legíveis em console ou estruturados em JSON.
- Middleware ASGI para logs de requisições HTTP.
- Geração e preservação de `X-Request-ID`.
- Correlação de Request ID por `ContextVar`.
- Testes diretos dos contratos públicos de `GET /` e `GET /api/v1/health`.
- Testes automatizados de formatters, contexto e middleware.
- Análise estática com Ruff.
- Quality gate reproduzível em GitHub Actions, somente leitura e sem segredos.
- Matriz automatizada para Ubuntu Python 3.12, 3.13 e 3.14 e Windows Python 3.14.
- Validação automática de lock, snapshot, Ruff, Pytest, importação e preservação da
  árvore rastreada.
- Baseline reproduzível de container Linux com inputs pinados por digest completo.
- Build Docker multi-stage com Python `3.14.6`, instalação bloqueada pelo `uv.lock`
  e runtime mínimo.
- Runtime com UID/GID `10001:10001`, healthcheck e filesystem somente leitura.
- Ausência de ferramentas e dependências de desenvolvimento na imagem runtime.
- Container Gate somente leitura, sem secrets, registry login, publicação de imagem,
  cache externo, artifacts ou deployment.

## Arquitetura atual

O backend fica em `apps/backend`. `app.main` cria a aplicação FastAPI, registra o
router `/api/v1` e instala o middleware de observabilidade. As configurações ficam
em `app.core.settings`, e logging, formatters, contexto e middleware ficam no pacote
`app.core.observability`.

```text
Dockerfile
.dockerignore
.github/workflows/
├── quality-gate.yml
└── container-gate.yml
apps/backend/app/
├── api/
│   └── v1/health.py
├── core/
│   ├── observability/
│   └── settings.py
└── main.py
tests/
├── test_api.py
├── test_container_baseline.py
├── test_container_gate_workflow.py
├── test_env_example.py
├── test_middleware.py
├── test_observability.py
├── test_project_snapshot.py
├── test_project_state.py
└── test_quality_gate_workflow.py
tools/
└── project_snapshot.py
docs/
├── adr/
├── 00_PROJECT_MASTER.md
├── 01_PROJECT_STATE.yaml
├── 02_BACKLOG.md
├── 03_CHANGELOG.md
├── HANDOFF_2026-07-19-SPRINT-09.md
└── PROJECT_SNAPSHOT.md
```

## Container reproduzível

As entradas do build estão fixadas por tag legível e digest completo para
`linux/amd64`:

```text
python:3.14.6-slim-trixie@sha256:d4fea6e20c09820028eea3f5c17f5b8ebd2ecb9c2bf28e561681a74a96090e4f
ghcr.io/astral-sh/uv:0.11.28@sha256:5c3ab83183a73c5d319a77009eb425b60d5bb937f339fb7876788ebf567baf48
```

Build local aprovado:

```powershell
docker build --no-cache --pull=false --tag hermes-ai-os:local .
```

Execução local com filesystem somente leitura:

```powershell
docker run --rm --read-only --publish 8000:8000 hermes-ai-os:local
```

A imagem usa usuário não root, expõe a porta `8000`, possui healthcheck e preserva
os contratos de `GET /`, `GET /api/v1/health`, Request ID e logging console/JSON.
Nenhuma imagem foi publicada e nenhum deployment foi executado.

## Requisitos

- Python `>=3.12,<3.15`.
- Patches comprovados na SPRINT-07: Windows `3.14.6` e Linux `3.12.13`,
  `3.13.14` e `3.14.6`.
- Git para obter e versionar o projeto.
- `uv` para instalação reproduzível; a prova oficial utilizou `uv 0.11.28`.

Os comandos abaixo devem ser executados na raiz do repositório.

## Instalação reproduzível no Windows PowerShell

```powershell
uv sync --locked --all-extras
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
```

## Instalação reproduzível no Linux ou macOS

```bash
uv sync --locked --all-extras
source .venv/bin/activate
cp .env.example .env
```

O `pyproject.toml` continua sendo a fonte declarativa das dependências, e o
`uv.lock` versionado é a resolução oficial que deve ser consumida sem alteração.
A opção `--all-extras` instala também as ferramentas de desenvolvimento representadas
no lock para testes e análise estática.

A cópia de `.env.example` é opcional; sem `.env`, os defaults de `Settings` são
utilizados. O template permanece sanitizado e alinhado ao contrato de configuração.

## Executar a API

Com o ambiente virtual ativo:

```text
python -m uvicorn app.main:app --app-dir apps/backend --reload
```

A API fica disponível por padrão em `http://127.0.0.1:8000`. O modo `--reload` é
destinado ao desenvolvimento local.

## Endpoints

### `GET /`

Resposta padrão:

```json
{
  "project": "Hermes AI OS",
  "version": "0.0.1",
  "environment": "development",
  "status": "running"
}
```

### `GET /api/v1/health`

Resposta padrão:

```json
{
  "status": "healthy",
  "project": "Hermes AI OS",
  "version": "0.0.1",
  "environment": "development"
}
```

Todas as respostas HTTP incluem o header configurado por `REQUEST_ID_HEADER`.

No PowerShell:

```powershell
Invoke-WebRequest `
  -Uri http://127.0.0.1:8000/api/v1/health `
  -Headers @{ "X-Request-ID" = "meu-request-id" }
```

No Linux ou macOS:

```bash
curl -i \
  -H 'X-Request-ID: meu-request-id' \
  http://127.0.0.1:8000/api/v1/health
```

Se o cliente não enviar o header, a aplicação gera um UUID. Se o enviar, o valor é
preservado e devolvido na resposta.

## Configuração

As variáveis podem ser definidas no ambiente ou em um arquivo `.env` na raiz.

| Variável | Valores aceitos | Default | Finalidade |
|---|---|---|---|
| `APP_NAME` | Texto | `Hermes AI OS` | Nome exposto pela aplicação |
| `APP_VERSION` | Texto | `0.0.1` | Versão exposta pela aplicação |
| `ENVIRONMENT` | Texto | `development` | Identificação do ambiente |
| `DEBUG` | Booleano | `true` | Flag de desenvolvimento declarada em `Settings` |
| `HOST` | Endereço de bind | `127.0.0.1` | Host declarado para o servidor |
| `PORT` | Porta TCP | `8000` | Porta declarada para o servidor |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO` | Nível mínimo de logging |
| `LOG_FORMAT` | `console`, `json` | `console` | Formatter dos logs |
| `REQUEST_ID_HEADER` | Nome de header HTTP | `X-Request-ID` | Header de correlação |

Exemplo PowerShell para executar com logs JSON:

```powershell
$env:LOG_FORMAT = "json"
python -m uvicorn app.main:app --app-dir apps/backend --reload
```

Exemplo Linux ou macOS:

```bash
LOG_FORMAT=json python -m uvicorn app.main:app --app-dir apps/backend --reload
```

## Qualidade

Executar análise estática:

```text
python -m ruff check .
```

Executar os testes:

```text
python -m pytest
```

Estado atual verificado no fechamento da SPRINT-09: 133 testes aprovados e
1 aviso de depreciação não bloqueante do `TestClient` relacionado ao `httpx`.
Ruff, importação, endpoints, Request ID, logging, snapshot, os 43 contratos do
Quality Gate e os 14 contratos do container foram aprovados localmente. O Quality
Gate run `29689585477` aprovou as quatro combinações da matriz, e o Container Gate
run `29689585471` aprovou integralmente o contrato da imagem. Execute sempre os
comandos acima para obter o resultado local atual; a quantidade de testes pode evoluir.

## Dependências reproduzíveis

O `uv.lock` é o lock oficial do Hermes AI OS. O arquivo canônico possui
`135871 bytes` e SHA-256
`6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`.

Atualizações do lock são deliberadas: devem registrar a versão completa do `uv`, o
índice e o cutoff ou política temporal equivalente, revisar o diff completo, validar
ambiente limpo, executar todos os gates aplicáveis e usar commit específico. Testes,
onboarding e futura CI devem consumir o lock sem modificá-lo.

A política completa está no
[ADR-0006](docs/adr/ADR-0006-uv-lock-como-lock-oficial-de-dependencias.md).
O `pylock.toml` permanece somente como evidência experimental e não é um artefato
oficial do repositório.

## Snapshot do Projeto

O snapshot oficial reside em `docs/PROJECT_SNAPSHOT.md`, usa schema 3 e representa uma
projeção determinística da árvore Git, excluindo o próprio relatório. Para regenerá-lo:

```text
python tools/project_snapshot.py
```

Sua validade operacional deve ser confirmada sem escrita com:

```text
python tools/project_snapshot.py --check
```

A SPRINT-10 está ativa para tornar os gates ao vivo de Ruff, Pytest e importação
fail-closed: qualquer falha deverá retornar exit code diferente de zero e impedir
a escrita ou a validação do snapshot. Nesta ativação documental, o comportamento
técnico ainda não foi alterado.

## Documentação do projeto

- [Project Master](docs/00_PROJECT_MASTER.md)
- [Estado operacional](docs/01_PROJECT_STATE.yaml)
- [Backlog](docs/02_BACKLOG.md)
- [Changelog](docs/03_CHANGELOG.md)
- [Handoff da SPRINT-09](docs/HANDOFF_2026-07-19-SPRINT-09.md)
- [Architecture Decision Records](docs/adr/README.md)

## Limitações atuais

O projeto permanece em `M1 — Infraestrutura`, que ainda não está concluído. A
SPRINT-10 — Snapshot Quality Gate Integrity está ativa somente no plano documental;
a implementação técnica ainda não foi autorizada. A publicação de artefatos de
container permanece bloqueada até a comprovação do comportamento fail-closed.

A baseline de container cobre `linux/amd64`, mas não inclui Docker Compose, registry,
publicação de imagem, deployment, persistência ou orquestração. Banco de dados,
runtime de agentes, memória, dashboard e integrações externas ainda não estão
implementados. A prova Linux da SPRINT-07 ocorreu em Docker Desktop/WSL2, não em host
físico Linux administrado separadamente. A interoperabilidade de terceiros do
`pylock.toml` não foi comprovada, e o arquivo não foi adotado oficialmente.
