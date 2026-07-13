# Changelog — Hermes AI OS

Todas as mudanças relevantes do projeto serão registradas neste arquivo.

O formato segue uma adaptação de Keep a Changelog, mas somente fatos verificáveis no código e no Git devem ser incluídos.

---

## [Unreleased]

O snapshot final ainda não foi adotado.
Nenhuma nova Sprint foi ativada.

---

## [EPIC-004-SPRINT-03] — 2026-07-13

### EPIC-004 / SPRINT-03 — Reproducible Onboarding Baseline

**Status:** Concluída

**EPIC-004:** concluída; o snapshot é um artefato técnico de continuidade e não
condiciona seu status funcional.

**Git:** implementação da DT-008 no commit `2ebed11`

### Adicionado

- Exceção específica de `.env.example` adicionada após as regras protetivas de `.env`.
- Template sanitizado alinhado a todos os campos atuais de `Settings`.
- Dois testes de contrato adicionados para chaves, validação Pydantic e marcadores objetivos
  de segredo ou caminho pessoal.

### Alterado

- README alinhado ao template disponível e à cópia opcional.
- Documentação viva alinhada ao encerramento da SPRINT-03.

### Validado

- 44 testes aprovados e 1 aviso conhecido e não bloqueante.
- Ruff aprovado sem violações.
- Importação, endpoints, Request ID e formatos de logging preservados.
- Nenhuma dependência ou funcionalidade de produto adicionada.
- `.env` e variantes reais permanecem ignorados; `.env.example` está rastreado.
- DT-007 permanece aberta e fora do escopo.

### Baseline publicada anteriormente

- `2fcbd17`: README e onboarding concluídos.
- `1c02fb0`, `19b61d7` e `0866657`: ferramenta de snapshot implementada, corrigida e
  protegida contra autorreferência.
- `e1c3587`: snapshot oficial adotado e validado após o próprio commit.
- `main` e `origin/main` verificados e sincronizados em `e1c3587` antes deste
  fechamento documental.

### Estado dos incrementos recentes

- README e onboarding concluídos no commit `2fcbd17`.
- Estados factuais dos ADRs 0001–0003 alinhados em `2fcbd17`.
- Gerador determinístico de snapshot e testes adicionados em `1c02fb0`.
- `docs/PROJECT_SNAPSHOT.md` adotado oficialmente em `e1c3587` e validado com
  `python tools/project_snapshot.py --check` após o próprio commit.
- DT-008 implementada no commit `2ebed11`.
- Documentação final e handoff da SPRINT-03 commitados em `b1ab2ea`.
- Estado transitório de publicação removido em `313de97`.

### Adicionado

- README operacional com instalação, execução, endpoints, configuração, qualidade,
  arquitetura, documentação e limitações atuais.
- Instruções equivalentes para Windows PowerShell, Linux e macOS.

### Corrigido

- Autorreferência que invalidava o snapshot após o commit do próprio relatório.
- Dependência canônica de hash, data e mensagem do HEAD removida do snapshot.
- Árvore e fingerprint passaram a excluir explicitamente o próprio snapshot.
- Semântica do snapshot canônico definida sobre HEAD e sua árvore rastreada.
- Estado transitório da working tree removido do conteúdo canônico e mantido como
  precondição e saída de console do gerador.
- Arquivos ignorados e apenas existentes no filesystem removidos da árvore do snapshot.
- Estados de implementação dos ADRs 0001, 0002 e 0003, que ainda declaravam trabalho
  parcial ou não commitado apesar das evidências em `a1d0d21`.
- Estado Git dos documentos de continuidade após `ded359d`.

### Validado

- Resolução de `python -m pip install --dry-run -e ".[dev]"`.
- Execução com `python -m uvicorn app.main:app --app-dir apps/backend --reload`.
- Endpoints `/` e `/api/v1/health`, Request ID gerado e Request ID preservado.
- Logging nos formatos `console` e `json`, Ruff e 8 testes automatizados.

---

## [EPIC-003-SPRINT-02] — 2026-07-12

### EPIC-003 / SPRINT-02 — Logging System

**Status:** Concluída — Definition of Done atendida

**Git:** commit `a1d0d21` (`feat(observability): complete logging system sprint`), publicado em `origin/main`

### Adicionado

- `pyproject.toml` como configuração central de projeto, dependências, pytest e Ruff.
- Configurações `LOG_LEVEL`, `LOG_FORMAT` e `REQUEST_ID_HEADER`.
- Pacote `app.core.observability`.
- Configuração central de logging baseada em `logging.config.dictConfig`.
- Namespace de logger `hermes`.
- Função pública `get_logger()`.
- `ConsoleFormatter` para logs legíveis no ambiente local.
- `JsonFormatter` baseado em `orjson`.
- Seleção do formatter por `LOG_FORMAT`.
- Campos estruturados:
  - método HTTP;
  - caminho;
  - status HTTP;
  - duração em milissegundos.
- `RequestContextFilter` para injeção automática de `request_id`.
- Contexto de requisição baseado em `ContextVar`.
- Restauração segura do contexto usando `Token`.
- Middleware ASGI puro para logging HTTP.
- Geração automática de `X-Request-ID`.
- Preservação de `X-Request-ID` recebido.
- Inclusão de `X-Request-ID` no header de resposta.
- Logs automáticos de:
  - início da requisição;
  - conclusão da requisição;
  - falha da requisição.

### Alterado

- `apps/backend/app/main.py` passou a configurar observabilidade e registrar o middleware HTTP.
- `apps/backend/app/core/settings.py` passou a declarar configurações relacionadas ao logging.

### Validado manualmente

- Importação completa da aplicação com resultado `IMPORT_OK`.
- Inicialização do Uvicorn.
- Endpoint `/api/v1/health` respondendo com HTTP 200.
- Geração automática de Request ID.
- Propagação de Request ID recebido.
- Retorno do Request ID no header da resposta.
- Correlação do mesmo Request ID nos logs.
- Registro de campos HTTP estruturados no console.
- Logging JSON estruturado com Request ID e campos HTTP.
- Requisição de teste com duração medida de aproximadamente `0.002054` segundos.
- Oito testes automatizados aprovados.
- Ruff aprovado sem violações.

### Corrigido

- `pyproject.toml` inicialmente continha UTF-8 BOM, impedindo o parser TOML.
- O BOM foi removido e o pytest passou a carregar a configuração.
- `filters.py` chegou a conter somente `...` durante a implementação e foi corrigido com a classe `RequestContextFilter`.
- A configuração do filtro no `dictConfig` foi alterada para usar a classe importada diretamente.
- Os quatro erros Ruff `I001` foram corrigidos.
- `REQUEST_ID_HEADER` foi consolidado em `Settings`.
- O módulo legado `apps/backend/app/core/logging.py` foi removido.

### Pendências conhecidas

- Staging, whitespace e finais de linha validados sem erros.
- Existe um aviso de depreciação do `TestClient` relacionado ao `httpx`; é uma observação não bloqueante.

---

## [0.0.1-foundation-api] — 2026-07-12

### Commit `2a30fa4`

**Mensagem:** `feat(core): add API v1, settings and health endpoint`

### Adicionado

- `.editorconfig`.
- `LICENSE`.
- `README.md`.
- Pacote `app.api`.
- Router com prefixo `/api/v1`.
- Endpoint `/api/v1/health`.
- Configuração central com `pydantic-settings`.
- Metadados de nome e versão na aplicação FastAPI.

### Alterado

- `apps/backend/app/main.py`.

### Limitações verificadas

- `README.md` foi criado vazio.
- Nenhum teste automatizado correspondente foi localizado.
- A documentação histórica da Sprint não foi localizada.

---

## [0.0.1-bootstrap] — 2026-07-12

### Commit `feec40a`

**Mensagem:** `chore: bootstrap Hermes AI OS foundation`

### Adicionado

- `.gitignore`.
- Workspace `Hermes-AI-OS.code-workspace`.
- Aplicação FastAPI inicial.
- `docs/00_PROJECT_MASTER.md`.
- `docs/research/2026-07-12-stack-tecnologica.md`.

### Limitações verificadas

- O documento de pesquisa tecnológica foi criado vazio.
- A documentação principal ficou desatualizada após o avanço do código.
