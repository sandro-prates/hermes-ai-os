# Hermes AI OS — Backlog

> Última verificação: 12/07/2026
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

- [ ] Criar testes automatizados da API base.
- [x] Preencher `README.md` com onboarding reproduzível.
- [ ] Confirmar documentação histórica da Sprint correspondente.
- [ ] Validar Definition of Done retrospectiva.

---

# Dívida Técnica Atual

## DT-001 — Ausência de testes automatizados

**Status:** ✅ Resolvida

O Pytest atualmente coleta e aprova 32 testes automatizados.

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

# Próxima Sprint Planejada

## EPIC-004 — Foundation Reproducibility

### SPRINT-03 — Reproducible Onboarding Baseline

**Status:** `planned`

**Objetivo único:** tornar o onboarding documentado reproduzível a partir de um clone
limpo, sem adicionar dependências nem implementar funcionalidades de produto.

**Primeira Task:** versionar e validar um `.env.example` sanitizado.

**Justificativa:** o README instrui copiar `.env.example`, mas o arquivo está ignorado
e não rastreado. O comando falha em um clone limpo, quebrando o onboarding oficial.
Essa inconsistência operacional tem prioridade maior que DT-007.

**Escopo permitido:**

- ajustar `.gitignore` somente para permitir o template sanitizado;
- versionar `.env.example` sem segredos ou dados locais;
- cobrir as configurações declaradas em `Settings`;
- validar os comandos de onboarding a partir de uma cópia limpa;
- alinhar README e documentação viva aos resultados comprovados;
- atualizar documentação viva e snapshot pelo fluxo oficial.

**Critérios de aceitação:**

- `.env.example` rastreado, sanitizado e disponível em clone limpo;
- nenhum segredo, credencial ou valor específico da máquina incluído;
- template consistente com os campos de `Settings`;
- comandos PowerShell e Linux/macOS do README novamente validados;
- nenhuma dependência, arquitetura ou funcionalidade adicionada;
- Ruff e Pytest aprovados;
- documentação consistente, snapshot regenerado e `--check` aprovado;
- parada antes de commit e push para aprovação.

**Fora de escopo:** implementação de produto, novas dependências, lockfile, CI/CD,
banco de dados, runtime de agentes, memória, dashboard, integrações e preenchimento
da pesquisa tecnológica DT-007.

**Riscos:** versionar segredo acidentalmente; expor valores locais; deixar o template
divergente de `Settings`; ou ampliar o escopo para configuração de produto.

**Arquivos provavelmente envolvidos:** `.gitignore`, `.env.example`, `README.md`,
testes documentais aplicáveis, quatro documentos de continuidade e snapshot após o
futuro commit. ADR novo somente se surgir decisão arquitetural realmente nova.

**Ativação:** somente na próxima conversa. Nenhuma implementação foi iniciada.

---

## DT-007 — Pesquisa tecnológica vazia

**Status:** ⚠️ Aberta

Arquivo:

`docs/research/2026-07-12-stack-tecnologica.md`

O item foi deliberadamente adiado em favor da inconsistência operacional DT-008.

---

## DT-008 — `.env.example` ignorado e ausente do Git

**Status:** ⚠️ Aberta

O README instrui copiar `.env.example`, mas `.gitignore` ignora `.env.*` e o template
não está rastreado. O onboarding documentado não funciona integralmente em clone limpo.

**Planejamento:** primeira Task da SPRINT-03 (`planned`), ainda não iniciada.

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
