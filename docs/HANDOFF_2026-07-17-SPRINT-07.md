# Hermes AI OS — Handoff Oficial da SPRINT-07

## 1. Identificação

- Projeto: Hermes AI OS.
- Versão: `0.0.1`.
- Milestone: `M0 — Foundation`.
- Sprint: `SPRINT-07 — Dependency Reproducibility Proof`.
- Estado: concluída localmente.
- Responsável humano: Sandro Prates.
- Data do fechamento local: 17/07/2026.
- Shell oficial: Windows PowerShell 5.1.
- Repositório: `D:\Hermes-AI-OS`.

## 2. Baseline inicial

- Branch: `main`.
- HEAD inicial:
  `7513489c294a20ce5ee5f8e293f8111fbaf95af1`.
- `origin/main` local:
  `9cfefa8bf117bceb11bcbd5df2a18cc28f82303c`.
- Divergência inicial: ahead `4`, behind `0`.
- Working tree, staging e untracked: vazios.
- `index.lock`: ausente.
- `uv.lock` oficial: ausente.
- Estado atual do servidor remoto: não confirmado.

## 3. Objetivo da Sprint

Comprovar resolução determinística e reprodutibilidade das dependências em ambientes
isolados, avaliar o pylock somente como interoperabilidade experimental e fundamentar
uma decisão explícita sobre o lock oficial do projeto.

## 4. Resultados técnicos

- metadados do `pyproject.toml` confirmados sem alteração;
- duas resoluções independentes baseadas em `ea5a1ff`;
- locks A/B byte-idênticos;
- ambientes Windows independentes aprovados;
- matriz Linux aprovada;
- inventários normalizados e dependências representadas no lock;
- validação independente do Master 2 aprovada;
- nenhuma mudança em código de produto ou dependências declaradas.

## 5. Lock adotado

- Arquivo oficial: `uv.lock`.
- Tamanho: `135871 bytes`.
- SHA-256:
  `6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`.
- Origem canônica:
  `D:\Hermes-Experiments\SPRINT-07\resolution\area-a\uv.lock`.
- Comparação com area-a: byte-idêntica.
- Comparação com area-b: byte-idêntica.
- Adoção oficial registrada no commit local
  `cf5dfdae11ddcb77137f8d75b11606b73bfc43a2`.

## 6. Ferramenta uv

- Versão:
  `uv 0.11.28 (ebf0f43d7 2026-07-07 x86_64-pc-windows-msvc)`.
- Caminho da prova:
  `D:\Hermes-Experiments\SPRINT-07\tools\uv-0.11.28\uv.exe`.
- SHA-256:
  `533FE4044BC50B05AC89F4D07925597FDB5285369724E8986ECAB356818F09EE`.
- Índice explícito: `https://pypi.org/simple`.
- Cutoff: `2026-07-14T11:53:48.187Z`.

## 7. Matriz comprovada

### Windows

- Python `3.14.6`.

### Linux em Docker Desktop/WSL2

- Python `3.12.13`;
- Python `3.13.14`;
- Python `3.14.6`.

A prova Linux não representa validação em host físico administrado separadamente.

## 8. Gates finais

- YAML: aprovado.
- Ruff: aprovado.
- Pytest: 76 testes aprovados.
- Warnings: 1 aviso conhecido e não bloqueante.
- Importação da aplicação: aprovada.
- `GET /`: aprovado.
- `GET /api/v1/health`: aprovado.
- Request ID gerado: aprovado.
- Request ID preservado: aprovado.
- Logging console: aprovado.
- Logging JSON: aprovado.
- Snapshot: geração, auditoria e `--check` aprovados.
- Integridade do lock: aprovada.
- `pyproject.toml`: preservado.
- `.venv` oficial: preservada.

Os resultados completos e hashes dos logs ficam nos relatórios externos do Executor 2.

## 9. Política oficial

- `pyproject.toml` continua sendo a fonte declarativa.
- `uv.lock` é o lock oficial, versionado e reproduzível.
- Instalações e validações devem consumir o lock sem modificá-lo.
- Atualizações são deliberadas e devem registrar versão completa do uv, índice,
  cutoff ou política temporal equivalente.
- O diff completo deve ser revisado como artefato de segurança e supply chain.
- Ambiente limpo, Ruff, Pytest, runtime, snapshot e matriz aplicável devem ser
  validados.
- Mudança de lock deve usar commit específico e não deve ser misturada
  silenciosamente com mudança funcional.
- Futura CI deverá consumir o lock em modo bloqueado.

## 10. ADR

O ADR-0006 — `uv.lock` como lock oficial de dependências foi criado com status
`Accepted`. Ele complementa o ADR-0001: o `pyproject.toml` permanece declarativo,
enquanto o `uv.lock` fixa a resolução oficial.

## 11. Classificação do pylock

- Exportação: aprovada.
- Exportações A/B byte-idênticas: sim.
- Consumo pelo uv: aprovado.
- Adoção oficial: não.
- Interoperabilidade de terceiros: não comprovada.
- O `pylock.toml` não foi copiado para o repositório.

## 12. Arquivos do fechamento

- `uv.lock`;
- `README.md`;
- `docs/00_PROJECT_MASTER.md`;
- `docs/01_PROJECT_STATE.yaml`;
- `docs/02_BACKLOG.md`;
- `docs/03_CHANGELOG.md`;
- `docs/PROJECT_SNAPSHOT.md`;
- `docs/adr/README.md`;
- `docs/adr/ADR-0006-uv-lock-como-lock-oficial-de-dependencias.md`;
- `docs/HANDOFF_2026-07-17-SPRINT-07.md`.

`tests/test_project_state.py` somente integra o fechamento se uma atualização estrita
for objetivamente necessária; nenhum teste pode ser reduzido ou tornado permissivo.

## 13. Commits locais

- Commit 1:
  `cf5dfdae11ddcb77137f8d75b11606b73bfc43a2` —
  `build(deps): adopt reproducible uv lock`.
- O hash do commit documental que contém este handoff é registrado no relatório
  externo final, evitando auto-referência.
- O hash do commit exclusivo do snapshot também é registrado no relatório externo
  final.

## 14. Estado Git de continuidade

Ao final do fluxo autorizado, o estado esperado é:

- branch `main`;
- `origin/main` local preservado em
  `9cfefa8bf117bceb11bcbd5df2a18cc28f82303c`;
- ahead `7`, behind `0`;
- working tree limpa;
- staging e untracked vazios;
- três commits locais de fechamento;
- nenhum push executado.

A comprovação do estado efetivamente observado após o commit do snapshot fica no
relatório externo final do Executor 2.

## 15. Estado remoto

`REMOTE_STATE=UNCONFIRMED`.

A referência `origin/main` local não comprova o estado atual do servidor remoto.
Nenhuma operação de rede foi autorizada ou executada durante o fechamento local.

## 16. Operações não executadas

- `git fetch`;
- `git pull`;
- `git push`;
- merge;
- rebase;
- reset;
- clean;
- amend;
- atualização de dependências;
- regeneração do lock;
- sincronização da `.venv` oficial;
- ativação da SPRINT-08.

## 17. Limitações

- CI não foi implementada.
- Validação em host físico Linux separado não foi comprovada.
- Interoperabilidade de terceiros do pylock não foi comprovada.
- O estado remoto permanece não confirmado.
- A conclusão local não equivale a publicação ou release.

## 18. Continuidade

- Nenhuma Sprint está ativa.
- Nenhuma Sprint está planejada.
- SPRINT-08 permanece não ativada.
- Nenhuma Task fictícia foi criada para a SPRINT-07.
- A última Task formal concluída permanece DT-009, pertencente à SPRINT-06.
- Uma futura publicação exige revisão do Master 2 e autorização humana específica.

## 19. Declaração final

A prova técnica da SPRINT-07 foi concluída, validada independentemente e convertida
em política oficial pela adoção do `uv.lock` e do ADR-0006. O fechamento documental
e o snapshot final seguem em commits locais separados. O fluxo para obrigatoriamente
antes de qualquer operação remota.
