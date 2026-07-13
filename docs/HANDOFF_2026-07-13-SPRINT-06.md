# Hermes AI OS — Project Handoff

## 1. Estado Geral

- Projeto: Hermes AI OS.
- Versão: `0.0.1`.
- Milestone: M0 — Foundation (`in_progress`).
- Última Sprint concluída: SPRINT-06 — Continuity State Integrity.
- Item concluído: DT-009 — Integridade do estado de continuidade.
- EPIC: nenhuma nova EPIC.
- Sprint ativa: nenhuma.
- Próxima Sprint formalmente planejada: nenhuma.

## 2. Resultado da SPRINT-06

- Project State migrado para schema 2.
- `work.active`, `work.last_completed` e `work.planned` são a fonte operacional única.
- Campos operacionais legados removidos do documento atual.
- Leitura do schema 1 preservada somente para compatibilidade retroativa.
- Estados ambíguos, incompletos ou duplicados falham de forma fechada.
- Modo `--check` informa validação sem sugerir escrita.
- ADR-0004 e ADR-0005 permanecem `Accepted` e foram alinhados factualmente.

## 3. Estado Operacional

- `work.active.sprint`: `null`.
- `work.active.task`: `null`.
- `work.last_completed.sprint`: SPRINT-06 (`completed`).
- `work.last_completed.task`: DT-009 (`completed`).
- `work.planned.sprint`: `null`.
- `work.planned.task`: `null`.

O histórico completo permanece em Git, Backlog, Changelog e handoffs históricos; não
é duplicado no Project State.

## 4. Arquitetura Preservada

- Aplicação FastAPI em `apps/backend/app`.
- `GET /` e `GET /api/v1/health`.
- Settings com `pydantic-settings` e `.env.example` sanitizado.
- Observabilidade central com logging console/JSON, middleware ASGI e `ContextVar`.
- Geração, preservação e retorno de Request ID.
- Snapshot determinístico baseado na árvore rastreada em `HEAD`.

Nenhum arquivo em `apps/`, dependência, lockfile ou workflow de CI foi alterado pela
SPRINT-06.

## 5. Testes e Qualidade

- Ruff aprovado sem violações.
- 76 testes aprovados.
- 1 `StarletteDeprecationWarning` conhecido e não bloqueante.
- YAML do Project State válido.
- Importação aprovada: Hermes AI OS `0.0.1`.
- Endpoints e Request ID aprovados.
- Logging console e JSON aprovados.
- Contrato `.env.example`/`Settings` aprovado.

## 6. Testes Novos e Ampliados

- `tests/test_project_state.py`: contrato real do schema 2 e rejeições fail-closed.
- `tests/test_project_snapshot.py`: schema 2, compatibilidade schema 1, exclusividade
  de estados, mensagens do CLI e estabilidade física do `--check`.

## 7. Commits Comprovados

- `da7a583` — snapshot final da SPRINT-05 e baseline da SPRINT-06.
- `4e2619c` — ativação documental da SPRINT-06.
- `30416fe` — implementação do schema 2, migração e testes.

Este documento não antecipa hashes de commits posteriores.

## 8. Continuidade do Snapshot

- Fonte oficial: `docs/PROJECT_SNAPSHOT.md`.
- Geração: `python tools/project_snapshot.py`.
- Validação sem escrita: `python tools/project_snapshot.py --check`.
- Atualização: commit exclusivo.
- Estado de commit e publicação: consultar diretamente no Git.

## 9. Candidatas Operacionais

- SPRINT-07 — Dependency Reproducibility Proof: candidata, não planejada ou ativada.
- SPRINT-08 — Automated Quality Gate: candidata, não planejada ou ativada.

As identificações SPRINT-06 e SPRINT-07 na pesquisa da SPRINT-05 eram provisórias e
foram preservadas naquele documento histórico.

## 10. Limitações Mantidas

- Banco de dados não implementado.
- Runtime de agentes não implementado.
- Memória não implementada.
- Dashboard não implementado.
- Integrações externas não implementadas.
- Estratégia de lock e CI ainda não adotadas.
- Warning de depreciação do `TestClient` permanece conhecido.

## 11. Trabalhos que Não Devem Ser Repetidos

- Observabilidade e Request ID.
- Contrato `.env.example`/`Settings`.
- Cobertura direta da API base.
- Pesquisa geral da DT-007.
- Migração do Project State para schema 2.
- Contratos determinísticos e autorreferenciais do snapshot.

## 12. Retomada

Na próxima conversa:

1. validar Git e working tree diretamente;
2. executar `python tools/project_snapshot.py --check`;
3. executar Ruff e a suíte completa;
4. ler Project Master, Project State, Backlog, Changelog, ADRs e este handoff;
5. não ativar SPRINT-07, SPRINT-08 ou qualquer outro trabalho automaticamente.
