# Hermes AI OS  Project Handoff

## 1. Estado Geral

- Projeto: Hermes AI OS.
- Versão: `0.0.1`.
- Milestone: M0 — Foundation (`in_progress`).
- Última Sprint concluída: SPRINT-05 — Technology Decision Baseline.
- Sprint ativa: nenhuma.
- Próxima Sprint planejada: nenhuma.
- EPIC associada à SPRINT-05: nenhuma.
- Item concluído: DT-007 — pesquisa tecnológica.

## 2. Resultado da SPRINT-05

- Baseline de ativação: `1dfd3ee`, sincronizada com `origin/main`.
- Ativação documental: `2f79d8c`.
- Pesquisa preenchida e commitada: `126aff8`.
- Documento: `docs/research/2026-07-12-stack-tecnologica.md`.
- Temas decisórios: lock de dependências, matriz Python e quality gate/CI.
- Temas posteriores: matriz preparatória compacta.
- Nenhuma recomendação foi automaticamente aceita ou implementada.

## 3. Recomendações Pendentes de Aprovação

- Prototipar uv como candidato a lock universal e avaliar exportação `pylock.toml`.
- Manter Python 3.12, 3.13 e 3.14 como matriz candidata.
- Prototipar GitHub Actions somente após a decisão de lock.
- Não adotar `pip lock` como fonte única enquanto a capacidade permanecer
  experimental e específica de plataforma/versão.

## 4. Arquitetura Atual

- Backend FastAPI em `apps/backend/app`.
- Endpoints `GET /` e `GET /api/v1/health`.
- `Settings` com `pydantic-settings` e `.env.example` sanitizado.
- Observabilidade central, logging console/JSON, middleware ASGI e `ContextVar`.
- Snapshot determinístico baseado em `git ls-tree HEAD`, sem autorreferência.
- Nenhum banco, fila, runtime de agentes, memória, dashboard ou integração.

## 5. Qualidade Verificada

- Ruff aprovado.
- 54 testes aprovados.
- 1 `StarletteDeprecationWarning` conhecido.
- Importação de Hermes AI OS `0.0.1` aprovada.
- Endpoints e geração/preservação de Request ID aprovados.
- Nenhum arquivo em `apps/` alterado na SPRINT-05.

## 6. Decisões Não Tomadas

- Nenhuma ferramenta de lock adotada.
- Nenhuma matriz de CI aprovada.
- Nenhum workflow criado.
- Nenhuma dependência ou lockfile adicionado.
- Nenhum ADR criado ou aceito.
- Nenhuma escolha de banco, fila, agente, modelo, cloud, memória ou frontend.

## 7. Candidatas de Continuidade

### SPRINT-06 — Dependency Reproducibility Proof

Prova isolada de matriz Python e uv, sem adoção automática.

### SPRINT-07 — Automated Quality Gate

Protótipo de GitHub Actions após decisão de lock.

As duas são candidatas. Nenhuma está planejada ou ativada.

## 8. Fontes da Pesquisa

A pesquisa usa documentação oficial da Python Software Foundation, PyPA, Astral,
GitHub, PostgreSQL, SQLite, SQLAlchemy, Celery, Dramatiq, LangChain, Pydantic, BerriAI,
Docker e Kubernetes, consultada em 13/07/2026. URLs, versões e datas disponíveis estão
registradas no documento da DT-007.

## 9. Dívidas e Limitações

- Aviso de depreciação `TestClient`/`httpx` conhecido.
- Lock e CI ainda não definidos ou implementados.
- Compatibilidade multiplataforma ainda não automatizada.
- Banco, runtime de agentes, memória, dashboard e integrações não implementados.
- Pendências retrospectivas da documentação histórica da API permanecem separadas.

## 10. Trabalhos que Não Devem Ser Repetidos

- Observabilidade, middleware e Request ID.
- DT-008 e contrato de `.env.example`.
- Determinismo, autorreferência e seleção do snapshot.
- Testes diretos da API base.
- Pesquisa geral da DT-007; futuras Sprints devem executar provas focadas.

## 11. Reinício Seguro

1. validar Git, `origin/main` e working tree;
2. executar `python tools/project_snapshot.py --check`;
3. executar Ruff, Pytest e importação;
4. ler este handoff, o Project State, o Backlog e a pesquisa;
5. planejar uma candidata sem ativação automática;
6. exigir aprovação humana para adoção tecnológica ou ADR.

## 12. Snapshot e Publicação

O snapshot oficial deve ser consultado em `docs/PROJECT_SNAPSHOT.md` e validado com
`python tools/project_snapshot.py --check`. Atualizações usam commit exclusivo. Git é
a fonte para estado de commit e publicação; este handoff não antecipa hashes futuros.
