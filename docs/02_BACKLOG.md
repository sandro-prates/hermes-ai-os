# Hermes AI OS — Backlog

> Última verificação: 18/07/2026
>
> Fonte de verdade operacional: `docs/01_PROJECT_STATE.yaml`
>
> Regra: nenhum item deve ser marcado como concluído sem evidência no código, Git, testes e documentação aplicável.

---

# Legenda

| Status | Significado |
|---|---|
| ✅ Concluído | Implementado, validado, documentado e commitado |
| 🟡 Em andamento | Implementação iniciada, mas Definition of Done ainda não atendida |
| ⚠️ Dívida técnica | Problema conhecido que precisa ser resolvido |
| ⏳ Pendente | Ainda não implementado |
| 🔍 A validar | Existe indício, mas falta evidência suficiente |

---

# Último trabalho concluído

## EPIC-003 — Logging System

**Status:** ✅ Concluído

**Sprint:** SPRINT-02

**Objetivo:** implementar logging profissional, correlação de requisições e uma base modular de observabilidade.

## Entregas implementadas e validadas manualmente

- [x] Criar pacote `app.core.observability`.
- [x] Configurar logging com `logging.config.dictConfig`.
- [x] Criar namespace de logger `hermes`.
- [x] Criar função pública `get_logger()`.
- [x] Criar `ConsoleFormatter`.
- [x] Criar filtro para injeção automática de `request_id`.
- [x] Criar contexto assíncrono com `ContextVar`.
- [x] Restaurar o contexto com `Token`.
- [x] Criar middleware ASGI puro.
- [x] Gerar `X-Request-ID` quando ausente.
- [x] Preservar `X-Request-ID` enviado pelo cliente.
- [x] Retornar `X-Request-ID` no header da resposta.
- [x] Registrar início da requisição.
- [x] Registrar conclusão da requisição.
- [x] Registrar exceções com `logger.exception`.
- [x] Registrar método HTTP.
- [x] Registrar caminho da requisição.
- [x] Registrar status HTTP.
- [x] Registrar duração em milissegundos.
- [x] Integrar middleware ao FastAPI.
- [x] Validar manualmente `/api/v1/health` com HTTP 200.
- [x] Validar propagação de Request ID.
- [x] Validar formatter estruturado no console.

## Fechamento da Sprint

- [x] Implementar `JsonFormatter`.
- [x] Fazer `LOG_FORMAT` selecionar entre `console` e `json`.
- [x] Definir uma única fonte para `REQUEST_ID_HEADER`.
- [x] Remover `apps/backend/app/core/logging.py`.
- [x] Criar testes unitários para `request_context`.
- [x] Criar testes unitários para os formatters.
- [x] Criar testes de integração para o middleware.
- [x] Testar geração automática de Request ID.
- [x] Testar preservação de Request ID recebido.
- [x] Testar header de resposta.
- [x] Testar logs de conclusão e erro.
- [x] Corrigir quatro violações Ruff `I001`.
- [x] Validar codificação, whitespace e finais de linha no estado final.
- [x] Reexecutar `pytest`.
- [x] Reexecutar `ruff check`.
- [x] Atualizar documentação final da Sprint.
- [x] Atualizar `docs/01_PROJECT_STATE.yaml`.
- [x] Atualizar `docs/03_CHANGELOG.md`.
- [x] Criar commit da Sprint (`a1d0d21`).
- [x] Confirmar publicação em `origin/main`.
- [x] Confirmar `pyproject.toml` rastreado e incluído no commit.

## Definition of Done da Sprint

- [x] Código implementado.
- [x] Testes automatizados criados e aprovados.
- [x] Ruff aprovado sem violações.
- [x] Documentação atualizada.
- [x] `PROJECT_STATE` atualizado.
- [x] ADRs relevantes registrados.
- [x] Commit realizado.
- [x] Alterações publicadas no repositório remoto.

**Resultado:** Definition of Done atendida.

Na conclusão da SPRINT-02, nenhuma Sprint subsequente havia sido definida.

---

# Task atual do M0 — sem Sprint

## README e onboarding reproduzível do Hermes AI OS

**Status:** ✅ Concluída no commit `2fcbd17`

- [x] Criar README operacional e factual.
- [x] Documentar instalação para Windows PowerShell, Linux e macOS.
- [x] Validar resolução da instalação editável com extras de desenvolvimento.
- [x] Validar o comando de execução da API com Uvicorn.
- [x] Documentar endpoints, configurações, qualidade e limitações.
- [x] Corrigir estados factuais dos ADRs 0001, 0002 e 0003.
- [x] Reexecutar validações de código, testes e runtime.
- [x] Criar commit exclusivamente documental (`2fcbd17`).

Nenhuma Sprint foi criada para esta Task.

---

# Sprint concluída anterior

## SPRINT-07 — Dependency Reproducibility Proof

**Status:** ✅ Concluída e publicada (`completed`)

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Task ou DT formal:** nenhuma criada para esta Sprint

**Última Task formal concluída:** DT-009, pertencente à SPRINT-06

**Sprint ativa:** SPRINT-08 — Automated Quality Gate

**Sprint seguinte planejada:** nenhuma; a SPRINT-08 está ativa, não apenas planejada

**Objetivo:** comprovar a resolução determinística e a reprodutibilidade das
dependências, adotar o lock canônico autorizado e estabelecer sua política oficial.

**Critérios de aceitação:**

- [x] metadados do `pyproject.toml` confirmados sem alteração;
- [x] `uv 0.11.28` utilizado fora da `.venv` oficial, com versão, caminho e
  SHA-256 documentados;
- [x] duas áreas experimentais independentes preservadas fora do repositório,
  ambas baseadas em `ea5a1ff`;
- [x] locks A/B gerados e comprovados como byte-idênticos;
- [x] lock canônico com `135871 bytes` e SHA-256
  `6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`;
- [x] Windows Python `3.14.6` validado;
- [x] Linux em Docker Desktop/WSL2 com Python `3.12.13`, `3.13.14` e `3.14.6`
  validado;
- [x] Ruff, 76 testes, 1 warning conhecido, importação, endpoints, Request ID,
  logging e snapshot aprovados;
- [x] exportação e consumo do `pylock.toml` pelo uv avaliados;
- [x] interoperabilidade de terceiros classificada como não comprovada;
- [x] validação independente do Master 2 aprovada;
- [x] `uv.lock` adotado oficialmente no commit local `cf5dfda`;
- [x] ADR-0006 criado e aceito;
- [x] política deliberada de atualização do lock documentada;
- [x] fechamento documental local realizado;
- [x] publicação remota concluída na baseline `85ef2616bdfe4573d9bf8bf2abecde06e76aac6a`.

**Decisões:**

- `pyproject.toml` permanece como fonte declarativa;
- `uv.lock` é o lock oficial e versionado;
- `pylock.toml` permanece somente como evidência experimental;
- atualizações do lock devem usar processo planejado, gates completos e commit
  específico;
- futura CI deverá consumir o lock sem modificá-lo.

**Limitações registradas no fechamento local da SPRINT-07:**

- o estado remoto ainda não havia sido confirmado naquele fechamento;
- nenhum `fetch`, `pull` ou `push` havia sido executado naquele fechamento;
- a prova Linux ocorreu em Docker Desktop/WSL2, não em host físico separado;
- CI ainda não havia sido implementada;
- interoperabilidade de terceiros do pylock não foi comprovada;
- a SPRINT-08 ainda não havia sido iniciada naquele fechamento.

**Evidências principais:** relatórios canônicos de determinismo, Windows, matriz
Linux, pylock, validação independente, ADR-0006 e commits locais do fechamento.

---

# Última Sprint Concluída

## SPRINT-08 — Automated Quality Gate

**Status:** ✅ Concluída e publicada (`completed`)

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Task ou DT formal:** nenhuma criada para esta Sprint

**Objetivo concluído:** implementar e validar um automated quality gate
reproduzível e somente leitura no GitHub Actions.

**Critérios de aceitação:**

- [x] workflow `.github/workflows/quality-gate.yml` criado;
- [x] triggers restritos a `push` em `main`, `pull_request` para `main` e
  `workflow_dispatch`;
- [x] `permissions: contents: read` e nenhuma permissão de escrita;
- [x] matriz com Ubuntu Python 3.12, 3.13 e 3.14 e Windows Python 3.14;
- [x] `fail-fast: false`;
- [x] Actions externas pinadas por SHA completo e versão humana registrada;
- [x] `uv 0.11.28` e cutoff oficial da SPRINT-07;
- [x] `uv lock --check` e `uv sync --locked --all-extras`;
- [x] snapshot check, Ruff, Pytest, importação e preservação da árvore rastreada;
- [x] 43 testes automatizados do contrato do workflow;
- [x] suíte local com 119 testes aprovados e 1 warning conhecido;
- [x] execução remota `29663968493` concluída com sucesso nos quatro jobs;
- [x] ausência de segredos, cache, artifacts, deployment, autofix, permissões de
  escrita e comandos Git de escrita;
- [x] `pyproject.toml`, `uv.lock`, `apps/` e `.venv` oficial preservados;
- [x] ADR-0007 aceita após comprovação remota.

**Evidência principal:** implementação publicada em `49b5dd5`; GitHub Actions run
`29663968493` integralmente verde.

**Continuidade:** nenhuma Sprint está ativa ou planejada. A SPRINT-09 não foi
autorizada.

---

# Trabalho Histórico Verificado

## Bootstrap do Hermes AI OS

**Evidência Git:** `feec40a`

**Situação:** implementação commitada.

Entregas verificadas:

- [x] `.gitignore`.
- [x] Workspace do VS Code.
- [x] Aplicação FastAPI inicial.
- [x] `docs/00_PROJECT_MASTER.md`.
- [x] Estrutura inicial de pesquisa.

Observações:

- O documento de pesquisa tecnológica existe, mas está vazio.
- A conformidade integral com a Definition of Done histórica não foi comprovada.

---

## API base, Settings e Health Endpoint

**Evidência Git:** `2a30fa4`

**Situação:** implementação commitada.

Entregas verificadas:

- [x] Router `/api/v1`.
- [x] Endpoint `/api/v1/health`.
- [x] Settings centralizados.
- [x] Metadados da aplicação FastAPI.
- [x] `.editorconfig`.
- [x] `LICENSE`.
- [x] `README.md` criado.

Pendências retrospectivas verificadas:

- [x] Criar testes automatizados da API base — concluídos na SPRINT-04, com
  implementação comprovada pelo commit `2dc6365`.
- [x] Preencher `README.md` com onboarding reproduzível.
- [ ] Confirmar documentação histórica da Sprint correspondente.
- [ ] Validar Definition of Done retrospectiva.

---

# Dívida Técnica Atual

## DT-001 — Ausência de testes automatizados

**Status:** ✅ Resolvida

Na resolução original desta dívida, o Pytest coletava e aprovava 32 testes. A
quantidade atual deve ser obtida pela suíte completa e é registrada no estado de
qualidade vigente.

---

## DT-002 — Ruff não aprovado

**Status:** ✅ Resolvida

Os quatro erros `I001` foram corrigidos e `python -m ruff check .` foi aprovado.

---

## DT-003 — Logging legado não utilizado

**Status:** ✅ Resolvida

O módulo redundante `apps/backend/app/core/logging.py` foi removido.

---

## DT-004 — Contrato incompleto de LOG_FORMAT

**Status:** ✅ Resolvida

`LOG_FORMAT` seleciona os formatters `console` e `json`, ambos validados.

---

## DT-005 — REQUEST_ID_HEADER duplicado

**Status:** ✅ Resolvida

`app.core.settings.Settings.REQUEST_ID_HEADER` é a fonte única utilizada pelo middleware.

---

## DT-006 — README vazio

**Status:** ✅ Resolvida no commit `2fcbd17`

O README operacional foi criado e seus comandos principais foram validados.

---

## Ferramenta de snapshot técnico

**Status:** ✅ Concluída

- [x] Comprovar a autorreferência em clone temporário.
- [x] Definir projeção estável da árvore Git no ADR-0005.
- [x] Excluir o próprio snapshot da projeção e do fingerprint.
- [x] Remover metadados de commit do conteúdo canônico.
- [x] Adicionar prova automatizada do fluxo de commit do snapshot.
- [x] Gerar, validar e adotar oficialmente `docs/PROJECT_SNAPSHOT.md` (`e1c3587`).

---

# Sprint Concluída

## EPIC-004 — Foundation Reproducibility

### SPRINT-03 — Reproducible Onboarding Baseline

**Status da EPIC:** `completed`

**Status da Sprint:** `completed`

**Objetivo único:** tornar o onboarding documentado reproduzível a partir de um clone
limpo, sem adicionar dependências nem implementar funcionalidades de produto.

**Task concluída:** DT-008 — versionar e validar um `.env.example` sanitizado
(`completed`, commit `2ebed11`).

**Justificativa:** na baseline, o README instruía copiar `.env.example`, mas o arquivo
estava ignorado e ausente da árvore Git. O comando falhava em um clone limpo, quebrando
o onboarding oficial. Essa inconsistência operacional tem prioridade maior que DT-007.

**Escopo permitido:**

- ajustar `.gitignore` somente para permitir o template sanitizado;
- versionar `.env.example` sem segredos ou dados locais;
- cobrir as configurações declaradas em `Settings`;
- validar os comandos de onboarding a partir de uma cópia limpa;
- alinhar README e documentação viva aos resultados comprovados;
- atualizar documentação viva e snapshot pelo fluxo oficial.

**Critérios de aceitação:**

- [x] `.env.example` sanitizado, rastreado e preparado para distribuição;
- [x] nenhum segredo, credencial ou valor específico da máquina incluído;
- [x] template consistente com os campos de `Settings`;
- [x] sem dependência, arquitetura ou funcionalidade adicionada;
- [x] contrato de configuração protegido por dois testes automatizados;
- [x] 44 testes e Ruff aprovados;
- [x] implementação registrada no commit `2ebed11`.

**Continuidade técnica:** o snapshot oficial é regenerado e verificado pelo fluxo
oficial sempre que a árvore projetada muda. Esse artefato não condiciona o status
funcional da EPIC, da Sprint ou da Task.

**Fora de escopo:** implementação de produto, novas dependências, lockfile, CI/CD,
banco de dados, runtime de agentes, memória, dashboard, integrações e preenchimento
da pesquisa tecnológica DT-007.

**Riscos:** versionar segredo acidentalmente; expor valores locais; deixar o template
divergente de `Settings`; ou ampliar o escopo para configuração de produto.

**Arquivos provavelmente envolvidos:** `.gitignore`, `.env.example`, `README.md`,
testes documentais aplicáveis, quatro documentos de continuidade e snapshot no
fechamento formal. ADR novo somente se surgir decisão arquitetural realmente nova.

**Encerramento:** baseline `51d3747` comprovada e implementação concluída em `2ebed11`.
A EPIC-004, a SPRINT-03 e a DT-008 estão concluídas. SPRINT-03 e DT-008 eram o único
escopo formal documentado da EPIC. A documentação e o handoff estão comprovados por
`b1ab2ea` e `313de97`. Nenhuma nova Sprint foi ativada.

---

# SPRINT-04 Encerrada

## SPRINT-04 — Foundation Integrity Baseline

**Status:** ✅ Concluída

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC criada; EPIC-004 permanece concluída.

**Item funcional:** pendência retrospectiva “Criar testes automatizados da API base”.

**Objetivo:** proteger diretamente os contratos públicos existentes de `GET /` e
`GET /api/v1/health`, incluindo o header configurado de Request ID, e alinhar os
documentos vivos à baseline Git atual.

**Escopo permitido:**

- criar testes diretos contra a aplicação FastAPI real;
- validar status HTTP, JSON público e Request ID;
- corrigir contagens atuais e separar baselines históricas do estado corrente;
- manter código da aplicação e comportamento público inalterados.

**Critérios de aceitação:**

- [x] contratos de `GET /` protegidos diretamente;
- [x] contratos de `GET /api/v1/health` protegidos diretamente;
- [x] header configurado de Request ID validado na aplicação real;
- [x] nenhuma alteração funcional em `apps/`;
- [x] implementação validada com 51 testes e Ruff aprovados;
- [x] fechamento técnico validado com 54 testes após três regressões do snapshot;
- [x] importação, endpoints e Request ID aprovados;
- [x] documentação viva de encerramento preparada;
- [x] novo handoff preparado sem sobrescrever os anteriores;
- [x] implementação registrada no commit `2dc6365`;

**Snapshot e publicação:** o snapshot oficial é mantido em commit exclusivo. Sua
validade é comprovada por `python tools/project_snapshot.py --check`; Git determina
se o artefato foi commitado e publicado.

**Definition of Done:** atendida no escopo funcional e documental da Sprint. Snapshot
e publicação seguem o processo técnico de continuidade sem alterar esse status.

**Continuidade:** nenhuma Sprint está ativa ou formalmente planejada. DT-007 permanece
aberta, separada e não ativada.

**Fora do escopo:** DT-007, nova EPIC, dependências, lockfile, CI/CD, banco de dados,
agentes, memória, dashboard, integrações, política nova de Request ID e correção do
aviso do `TestClient`.

---

## DT-007 — Pesquisa tecnológica

**Status:** ✅ Concluída como pesquisa na SPRINT-05

Arquivo:

`docs/research/2026-07-12-stack-tecnologica.md`

O item foi deliberadamente adiado em favor da inconsistência operacional DT-008.
DT-007 não integra formalmente a EPIC-004 e foi ativada explicitamente apenas como
pesquisa documental da SPRINT-05. O documento foi preenchido, revisado e commitado em
`126aff8`. A conclusão não aceita ou implementa suas recomendações.

---

# SPRINT-05 Encerrada

## SPRINT-05 — Technology Decision Baseline

**Status:** ✅ Concluída

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Item formal:** DT-007 — Pesquisa tecnológica

**Objetivo:** definir recomendações verificáveis para gerenciamento e lock de
dependências, matriz oficial de versões do Python e quality gate/CI; preparar os
demais temas sem implementação.

**Critérios de aceite:**

- [x] preencher e revisar o documento de pesquisa com fontes oficiais atuais;
- [x] separar fatos, inferências, recomendações e decisões adiadas;
- [x] classificar alternativas como adotar, prototipar, adiar, rejeitar ou pendente
  de aprovação humana;
- [x] recomendar a sequência técnica das duas próximas Sprints;
- [x] não adicionar dependências, lockfile, CI, código de produto ou ADR aceito;
- [x] aprovar Ruff, testes, importação, endpoints e Request ID;
- [x] atualizar documentação viva e preparar handoff no fluxo de fechamento.

**Fora do escopo:** implementação de banco, migrations, filas, workers, agentes,
modelos, memória, dashboard, integrações, cloud, lockfile, CI/CD, novas dependências,
alteração de aplicação e aceitação automática de ADRs.

**Evidência:** ativação `2f79d8c`; pesquisa `126aff8`.

**Continuidade histórica:** as identificações SPRINT-06 e SPRINT-07 eram candidatas
provisórias, não ativadas ou planejadas durante a SPRINT-05. Com a ativação da
Continuity State Integrity como SPRINT-06, elas passam a ser referenciadas
operacionalmente como SPRINT-07 — Dependency Reproducibility Proof e SPRINT-08 —
Automated Quality Gate, sem adoção ou ativação. O snapshot segue o fluxo oficial em
commit exclusivo.

---

# SPRINT-06 Encerrada

## SPRINT-06 — Continuity State Integrity

**Status:** ✅ Concluída

**Milestone:** M0 — Foundation

**EPIC:** nenhuma nova EPIC

**Item formal:** DT-009 — Integridade do estado de continuidade

**Objetivo:** tornar o Project State operacional inequívoco, migrando-o para o schema 2
com uma única fonte para trabalho ativo, última entrega concluída e planejamento.

**Critérios de aceite:**

- [x] `work.active`, `work.last_completed` e `work.planned` são a única fonte
  operacional;
- [x] campos legados não permanecem como fontes paralelas no schema 2;
- [x] leitura isolada do schema 1 permanece retrocompatível;
- [x] ambiguidades e estados incompatíveis falham de forma fechada;
- [x] `--check` valida sem sugerir escrita nem modificar o snapshot;
- [x] ADR-0004 e ADR-0005 permanecem `Accepted` e factualmente alinhados;
- [x] testes direcionados, Ruff, suíte completa, YAML e runtime são aprovados;
- [x] documentação viva e handoff são encerrados no fluxo oficial.

O snapshot oficial é mantido em commit exclusivo e sua situação deve ser consultada
em `docs/PROJECT_SNAPSHOT.md`, validada por `python tools/project_snapshot.py --check`
e confrontada com Git.

**Fora do escopo:** aplicação, dependências, lockfiles, CI, matriz Python, banco,
agentes, memória, dashboard, integrações, cloud e warning do `TestClient`.

---

## DT-009 — Integridade do estado de continuidade

**Status:** ✅ Concluída na SPRINT-06

Eliminar fontes operacionais paralelas no Project State, preservar leitura legada
isolada no gerador e proteger a migração com validações fail-closed e testes. A
implementação foi validada com 76 testes e permanece associada exclusivamente à
SPRINT-06.

---

## DT-008 — `.env.example` ignorado e ausente do Git

**Status:** ✅ Resolvida no commit `2ebed11`

Na baseline, o README instruía copiar `.env.example`, mas `.gitignore` ignorava `.env.*`
e o template não integrava a árvore Git. O onboarding documentado não funcionava
integralmente em clone limpo.

**Execução:** Task concluída na SPRINT-03. O template sanitizado está rastreado, e seu
contrato é protegido por dois testes automatizados. `.env` e variantes reais continuam
ignorados. A continuidade do snapshot segue o gerador oficial e a validação por
`python tools/project_snapshot.py --check`.

---

# Roadmap de Alto Nível

Os itens abaixo vêm do `PROJECT_MASTER` e ainda não representam Sprints planejadas ou aprovadas.

- [ ] M0 — Foundation
- [ ] M1 — Infraestrutura
- [ ] M2 — Backend
- [ ] M3 — Runtime de Agentes
- [ ] M4 — Memória
- [ ] M5 — Dashboard
- [ ] M6 — Integrações
- [ ] M7 — Marketplace
- [ ] M8 — Enterprise

---

# Regras de Priorização

1. Concluir a Sprint atual antes de iniciar uma nova.
2. Corrigir bloqueadores de testes e qualidade antes do commit.
3. Manter cada incremento executável.
4. Evitar adicionar dependências sem necessidade comprovada.
5. Registrar decisões arquiteturais relevantes em ADR.
6. Atualizar a documentação antes de declarar uma Sprint concluída.
7. Avaliar cada decisão pelo impacto em modularidade, escalabilidade e potencial comercial.
