# Hermes AI OS

Hermes AI OS é uma plataforma em desenvolvimento para criação, orquestração e
execução de agentes de Inteligência Artificial. O projeto busca combinar operação
**Local First**, evolução **Cloud Ready** e um modelo de negócio **Open Core**.

## Status

- Versão atual: `0.0.1`.
- Fase atual: `M0 — Foundation`.
- API FastAPI executável localmente.
- EPIC-003 / SPRINT-02 (Logging System) concluída.
- SPRINT-03 — Reproducible Onboarding Baseline concluída na EPIC-004.
- DT-008 concluída no commit `2ebed11`, com `.env.example` sanitizado e dois testes
  contratuais.
- Nenhuma nova Sprint está ativa; snapshot final, handoff e publicação permanecem no
  fluxo formal de encerramento.
- EPIC-004 permanece `in_progress` até a conclusão desse fluxo formal.

## Funcionalidades implementadas

- API HTTP com endpoints raiz e de health check.
- Settings centralizados com `pydantic-settings` e suporte a arquivo `.env`.
- Logging central configurado com `logging.config.dictConfig`.
- Logs legíveis em console ou estruturados em JSON.
- Middleware ASGI para logs de requisições HTTP.
- Geração e preservação de `X-Request-ID`.
- Correlação de Request ID por `ContextVar`.
- Testes automatizados de formatters, contexto e middleware.
- Análise estática com Ruff.

## Arquitetura atual

O backend fica em `apps/backend`. `app.main` cria a aplicação FastAPI, registra o
router `/api/v1` e instala o middleware de observabilidade. As configurações ficam
em `app.core.settings`, e logging, formatters, contexto e middleware ficam no pacote
`app.core.observability`.

```text
apps/backend/app/
├── api/
│   └── v1/health.py
├── core/
│   ├── observability/
│   └── settings.py
└── main.py
tests/
├── test_env_example.py
├── test_middleware.py
├── test_observability.py
└── test_project_snapshot.py
tools/
└── project_snapshot.py
docs/
├── adr/
├── 00_PROJECT_MASTER.md
├── 01_PROJECT_STATE.yaml
├── 02_BACKLOG.md
├── 03_CHANGELOG.md
└── PROJECT_SNAPSHOT.md
```

## Requisitos

- Python `>=3.12,<3.15`.
- Git para obter e versionar o projeto.

Os comandos abaixo devem ser executados na raiz do repositório.

## Instalação no Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

## Instalação no Linux ou macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
cp .env.example .env
```

O extra `dev` instala as ferramentas declaradas no `pyproject.toml` para testes e
análise estática. A cópia de `.env.example` é opcional; sem `.env`, os defaults de
`Settings` são utilizados.

O `.env.example` é um template sanitizado com os defaults suportados por `Settings`.
A cópia para `.env` continua opcional quando os defaults forem adequados.

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

Baseline verificada no fechamento de 13/07/2026: 44 testes aprovados e 1 aviso de
depreciação não bloqueante do `TestClient` relacionado ao `httpx`. Execute sempre o
comando acima para obter o resultado atual; a quantidade de testes pode evoluir.

## Snapshot do Projeto

Para atualizar o relatório técnico reutilizável do estado atual:

```text
python tools/project_snapshot.py
```

## Documentação do projeto

- [Project Master](docs/00_PROJECT_MASTER.md)
- [Estado operacional](docs/01_PROJECT_STATE.yaml)
- [Backlog](docs/02_BACKLOG.md)
- [Changelog](docs/03_CHANGELOG.md)
- [Architecture Decision Records](docs/adr/README.md)

## Limitações atuais

O projeto ainda está no M0. Banco de dados, runtime de agentes, memória, dashboard e
integrações externas ainda não estão implementados. Também não há estratégia de lock
de dependências nem validação comprovada em todos os sistemas operacionais e versões
de Python suportadas. O documento de pesquisa tecnológica permanece vazio.
