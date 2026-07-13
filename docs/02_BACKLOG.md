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

Nenhuma próxima Sprint está definida.

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
- [ ] Preencher `README.md`, atualmente vazio.
- [ ] Confirmar documentação histórica da Sprint correspondente.
- [ ] Validar Definition of Done retrospectiva.

---

# Dívida Técnica Atual

## DT-001 — Ausência de testes automatizados

**Status:** ✅ Resolvida

O Pytest coletou e aprovou 8 testes automatizados.

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

**Status:** ⚠️ Aberta

O arquivo existe no Git, mas possui tamanho zero.

---

## DT-007 — Pesquisa tecnológica vazia

**Status:** ⚠️ Aberta

Arquivo:

`docs/research/2026-07-12-stack-tecnologica.md`

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
