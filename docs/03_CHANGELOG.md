# Changelog — Hermes AI OS

Todas as mudanças relevantes do projeto serão registradas neste arquivo.

O formato segue uma adaptação de Keep a Changelog, mas somente fatos verificáveis no código e no Git devem ser incluídos.

---

## [Unreleased]

## [SPRINT-11] — 2026-07-23

SPRINT-11 — Container Artifact Publication Baseline concluída em M1, sem nova
EPIC ou Task/DT formal. ADR-0009 foi aceita com 6 de 6 critérios satisfeitos.

- baseline final `88fa6871c8e73c02270f9be45c76154d28587559`;
- Quality Gate #12, Container Gate #10 e Publish Container Run #5 aprovados;
- package `PRIVATE`, vínculo e controles de acesso comprovados;
- um dispatch, um push, nenhum rerun, smokes console/JSON e logout aprovados;
- `131a06e` corrigiu RepoDigest; `fb64b92` corrigiu SIGPIPE;
- Runs #2, #3 e #4 preservados como falhas intermediárias;
- pacote final aprovado: ZIP SHA-256
  `c4769d901a6c4471ef37cb02741a537de221417c21c4352a48d94322135c3efd`
  e manifest SHA-256
  `a5c3bea81977dcdead1f1b4ccc320702078fcee9a21b1b3d878db016881d9fe7`;
- nenhuma Sprint ou Task ativa ou planejada; DT-009 permanece na SPRINT-06;
- M1 permanece `in_progress`; SPRINT-12 e MASTER 3 não foram criados;
- nenhum deployment, SBOM, signing ou attestation foi executado;
- warning conhecido do `TestClient`/`httpx` permanece não bloqueante.

### Incidente de visibilidade no GHCR e recuperação local da SPRINT-11 — 2026-07-20

- run `29773487377` publicou o digest
  `sha256:d6705f96c24194d548b66facc4dd72904045de823e66bb0fb1f3fc3a9b687dec`
  e falhou na validação de política privada;
- auditoria read-only confirmou acesso anônimo a manifest por tag e digest, lista de
  tags e config OCI;
- visibilidade pública não foi autorizada, o package não foi excluído e a causa raiz
  permanece não comprovada;
- recuperação local exige package GHCR preexistente, metadata `private`, vínculo exato
  e acesso anônimo negado antes do login/build e novamente depois de futuro push;
- ADR-0009 permanece `Proposed`;
- exclusão, PAT, bootstrap, novo dispatch, rerun, push Git e fechamento da SPRINT-11
  permanecem não autorizados.


### Ativação documental da SPRINT-11 — 2026-07-20

- SPRINT-11 — Container Artifact Publication Baseline ativada em M1 com status
  `in_progress` sobre a baseline publicada `b01753473be47d24e4d14a2d7691cdd1f12a405d`;
- SPRINT-10 permanece como última Sprint concluída;
- nenhuma EPIC, Task ou DT formal criada;
- nenhuma Sprint ou Task planejada;
- GHCR preservado como registry selecionado pelo planejamento;
- primeiro package definido como `PRIVATE`, sem autorização de visibilidade pública;
- implementação técnica, workflow de publicação, Publication Gate, ADR-0009,
  autenticação no GHCR e publicação externa não iniciados;
- nenhuma aplicação, dependência, lock, Dockerfile, workflow, package ou visibilidade
  alterados nesta ativação.

## [SPRINT-10] — 2026-07-20

SPRINT-10 — Snapshot Quality Gate Integrity concluída em M1, sem nova EPIC,
Task/DT formal ou ADR.

### Adicionado

- regressões negativas para falhas de Ruff, Pytest e importação durante geração e
  `--check` do snapshot;
- handoff `docs/HANDOFF_2026-07-20-SPRINT-10.md`.

### Corrigido

- `tools/project_snapshot.py` passou a propagar de forma fail-closed qualquer
  reprovação dos gates ao vivo;
- falhas de Ruff, Pytest ou importação agora retornam exit code diferente de zero;
- geração e validação não prosseguem depois de gate reprovado;
- caminho de sucesso, projeção baseada em `HEAD` e exclusão autorreferencial foram
  preservados.

### Commits publicados

- implementação técnica:
  `513afbaf64b11156d1859ed2bec8c85fff3cac7f`;
- snapshot pós-implementação:
  `cb2171f315430c977ca929ffb468363a0d5f079e`.

### Validado

- 24 regressões negativas fail-closed aprovadas;
- 77 testes de `tests/test_project_snapshot.py` aprovados;
- 161 testes totais aprovados, com 1 warning conhecido;
- Ruff aprovado;
- importação FastAPI Hermes AI OS `0.0.1` aprovada;
- geração, `--check --audit-working-tree` e `git diff --check` aprovados;
- Quality Gate run `29723471112` concluído com `success` em quatro jobs;
- Container Gate run `29723471158` concluído com `success` no job
  `container-gate`.

### Preservado

- nenhum arquivo em `apps/`;
- `pyproject.toml` e `uv.lock`;
- workflows e Dockerfile;
- ADRs aceitas;
- implementação e contratos da baseline de container;
- ausência de publicação de imagem, registry, Docker Compose ou deployment.

### Continuidade

- SPRINT-10 passa de `in_progress` para `completed`;
- nenhuma Sprint, Task ou DT permanece ativa ou planejada;
- M0 permanece `completed` somente como fato histórico;
- M1 permanece `in_progress`;
- SPRINT-11 permanece não autorizada.

## [SPRINT-09] — 2026-07-19

SPRINT-09 — Reproducible Container Baseline concluída em M1, sem nova EPIC ou
Task/DT formal.

### Adicionado

- `Dockerfile` Linux multi-stage;
- `.dockerignore` restritivo;
- workflow `.github/workflows/container-gate.yml`;
- testes contratuais `tests/test_container_baseline.py` e
  `tests/test_container_gate_workflow.py`;
- ADR-0008 — Baseline reproduzível de container;
- handoff `docs/HANDOFF_2026-07-19-SPRINT-09.md`.

### Implementado

- Python `3.14.6` e uv `0.11.28` pinados por digest completo para `linux/amd64`;
- build multi-stage com `uv sync --locked --no-dev --no-editable`;
- runtime não root com UID/GID `10001:10001`;
- filesystem somente leitura;
- healthcheck com biblioteca padrão do Python;
- contratos de endpoints, Request ID e logging console/JSON;
- ausência de ferramentas e dependências de desenvolvimento na imagem runtime;
- Container Gate somente leitura, sem secrets, registry login, push de imagem,
  cache externo, artifacts, deployment ou comandos Git de escrita.

### Validado

- 14 testes focados e 133 testes totais aprovados, com 1 warning conhecido;
- Ruff, importação, snapshot e `git diff --check` aprovados;
- Quality Gate run `29689585477` concluído com `success`;
- Container Gate run `29689585471` concluído com `success`;
- ADR-0008 promovida de `Proposed` para `Accepted`;
- arquivos de aplicação, `pyproject.toml`, `uv.lock`, Quality Gate e contratos
  técnicos existentes preservados.

### Não realizado

- publicação de imagem;
- deployment;
- Docker Compose;
- configuração de registry;
- alteração de dependências ou do comportamento da aplicação.

### Continuidade

- SPRINT-09 passa de `in_progress` para `completed`;
- nenhuma Sprint ou Task permanece ativa ou planejada;
- M0 permanece `completed` como fato histórico;
- M1 permanece `in_progress`;
- SPRINT-10 não autorizada.

## [SPRINT-08] — 2026-07-18

SPRINT-08 — Automated Quality Gate concluída no M0, sem nova EPIC ou Task formal.

### Adicionado

- Workflow `.github/workflows/quality-gate.yml`.
- 43 testes contratuais em `tests/test_quality_gate_workflow.py`.
- ADR-0007 — GitHub Actions como quality gate reproduzível e somente leitura.
- Handoff oficial `docs/HANDOFF_2026-07-18-SPRINT-08.md`.

### Implementado

- Matriz com Ubuntu Python 3.12, 3.13 e 3.14 e Windows Python 3.14.
- Actions externas pinadas por SHA completo.
- `uv 0.11.28`, cutoff oficial, lock check e sincronização bloqueada.
- Snapshot check, Ruff, Pytest, importação e preservação da árvore rastreada.
- Permissões limitadas a `contents: read`, sem segredos, cache, artifacts,
  deployment, autofix ou comandos Git de escrita.

### Validado

- Implementação publicada no commit `49b5dd5`.
- Suíte local com 119 testes aprovados e 1 warning conhecido.
- Endpoints, Request ID, logging console e JSON aprovados.
- GitHub Actions run `29663968493` concluído com sucesso.
- Quatro jobs e todos os passos obrigatórios aprovados.
- `pyproject.toml`, `uv.lock`, `apps/` e `.venv` oficial preservados.
- ADR-0007 promovida de `Proposed` para `Accepted`.

### Continuidade

- SPRINT-08 passa de `in_progress` para `completed`.
- Nenhuma Sprint permanece ativa ou planejada.
- SPRINT-09 não foi autorizada.
- Nenhuma nova versão do produto ou release foi declarada.

## [SPRINT-07] — 2026-07-17

SPRINT-07 — Dependency Reproducibility Proof concluída no M0, sem nova EPIC ou
Task formal.

### Adicionado

- `uv.lock` canônico com `135871 bytes` e SHA-256
  `6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`.
- ADR-0006 e política deliberada de atualização do lock.
- Handoff oficial da SPRINT-07.

### Validado

- Duas resoluções independentes produziram locks byte-idênticos.
- Windows Python 3.14.6 e matriz Linux 3.12.13, 3.13.14 e 3.14.6 aprovados.
- Ruff, 76 testes, importação, endpoints, Request ID, logging e snapshot aprovados.
- Publicação remota concluída na baseline `85ef2616`.

### Limitações históricas

- Prova Linux em Docker Desktop/WSL2, não em host físico separado.
- Interoperabilidade de terceiros do `pylock.toml` não comprovada.
- `pylock.toml` não adotado oficialmente.

## [SPRINT-05] — 2026-07-13

SPRINT-05 — Technology Decision Baseline concluída no M0, sem nova EPIC.

### Adicionado

- Pesquisa da DT-007 preenchida e commitada em `126aff8`, com 19 referências oficiais,
  critérios objetivos, matriz comparativa, riscos e sequência recomendada.
- SPRINT-06 e SPRINT-07 registradas somente como candidatas, sem ativação.

### Concluído

- DT-007 concluída como pesquisa, sem adoção tecnológica.
- Escopo decisório concentrou-se em lock de dependências, matriz Python e quality
  gate/CI; temas posteriores permaneceram em matriz preparatória.
- Baseline de ativação verificada em `1dfd3ee`, sincronizada com `origin/main`, com
  snapshot aprovado, Ruff aprovado e 54 testes aprovados com 1 aviso conhecido.
- Nenhuma dependência, lockfile, workflow de CI, código de produto ou ADR foi criado.

## [SPRINT-04] — 2026-07-13

SPRINT-04 — Foundation Integrity Baseline encerrada no M0, sem nova EPIC.

### Adicionado

- Cobertura direta dos contratos públicos de `GET /` e `GET /api/v1/health` na
  aplicação FastAPI real.
- Validação do header configurado de Request ID nas respostas da API base.
- Três testes diretos adicionados no commit `2dc6365`.

### Alterado

- Alinhamento da baseline operacional e das contagens atuais nos documentos vivos.
- EPIC-004, SPRINT-03 e DT-008 permanecem concluídas; DT-007 continua aberta e não
  ativada.
- Nenhuma Sprint está ativa ou formalmente planejada.

### Corrigido

- Durante o fechamento técnico da SPRINT-04 foi identificada e corrigida a seleção
  obsoleta de Sprint no gerador: Sprint ativa tem precedência, seguida da última
  Sprint concluída e do fallback legado.
- A seleção da SPRINT-04 não reutiliza EPIC-004 ou DT-008, que pertencem ao registro
  histórico da SPRINT-03; ausência de EPIC ou Task formal é representada sem inventar
  identificadores.
- O schema 3 e os contratos determinísticos do snapshot foram preservados.
- O commit `686a630` tornou explícitos no snapshot os status da EPIC, Sprint e Task,
  a ausência de Sprint ativa ou planejada e as limitações atuais.
- Quatro testes de regressão foram adicionados ao contrato do snapshot.
- O commit `01ac0b0` explicitou o contrato funcional de Request ID: geração quando
  ausente, preservação do valor recebido, retorno no header, correlação por
  `ContextVar` e injeção nos logs.
- O commit `4f4e2bb` explicitou o contrato determinístico entre `Settings` e
  `.env.example`, incluindo `env_prefix`, aliases simples, `case_sensitive`,
  correspondência exata e falha fechada para ambiguidades ou colisões.
- O schema 3, a projeção Git determinística, o fingerprint e a exclusão
  autorreferencial foram preservados.

### Validado

- Baseline anterior à SPRINT-04 com 48 testes aprovados.
- Implementação da SPRINT-04 validada originalmente com 51 testes aprovados.
- Suíte atual com 54 testes aprovados e 1 aviso conhecido e não bloqueante após três
  regressões do contrato de seleção do snapshot.
- Três testes diretos da API base aprovados, cobrindo respostas públicas e Request ID.
- Ruff aprovado sem violações.
- Importação, `GET /`, `GET /api/v1/health`, geração e preservação de Request ID
  aprovadas.
- Nenhuma funcionalidade, dependência ou arquivo em `apps/` foi alterado.

### Continuidade

- O snapshot oficial é atualizado em commit exclusivo, validado por
  `python tools/project_snapshot.py --check`; Git é a fonte do estado de commit e
  publicação.
- Correções do gerador devem integrar `HEAD` antes da geração real do relatório, que
  permanece isolada em commit próprio.

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
