# Handoff — SPRINT-11 — 23/07/2026

## Estado entregue

- `SPRINT_11_STATUS=completed`
- `ADR_0009_STATUS=Accepted`
- `LAST_COMPLETED_SPRINT=SPRINT-11`
- `CURRENT_SPRINT=null`
- `PLANNED_SPRINT=null`
- `MILESTONE_M1_STATUS=in_progress`
- `NEW_EPIC_CREATED=NAO`
- `NEW_TASK_OR_DT_CREATED=NAO`
- `WORK_LAST_COMPLETED_TASK=null`
- `DT_009_HISTORICAL_SPRINT=SPRINT-06`
- `SPRINT_12_STATUS=NOT_ACTIVATED`
- `MASTER_3_STATUS=NOT_CREATED`
- `MASTER_2_STATUS=ACTIVE_SOLE_COORDINATOR`

DT-009 permanece exclusivamente histórica: foi ativada e concluída na SPRINT-06 e
é a última Task/DT formal criada. SPRINT-07 a SPRINT-11 não criaram nova Task
formal; portanto `work.last_completed.task` é `null`.

## Baseline e evidência aprovada

- baseline bloqueante: `88fa6871c8e73c02270f9be45c76154d28587559`;
- package final: `HERMES_SPRINT11_FINAL_PRIMARY_EVIDENCE_PACKAGE_20260723-054610.zip`;
- ZIP SHA-256: `c4769d901a6c4471ef37cb02741a537de221417c21c4352a48d94322135c3efd`;
- manifest SHA-256: `a5c3bea81977dcdead1f1b4ccc320702078fcee9a21b1b3d878db016881d9fe7`;
- `MASTER_2_FILE_REVIEW_STATUS=APPROVED`;
- `EVIDENCE_GATE=PASSED`;
- `ADR_0009_ACCEPTANCE_CRITERIA_SATISFIED=6_OF_6`.

O ZIP de evidência não foi copiado para o repositório.

## Publicação final aceita

O Quality Gate #12 (`29873254326`) e o Container Gate #10 (`29873254322`)
concluíram com `success` no SHA final. O Publish Container Run #5
(`29874199694`), attempt 1, foi o único `workflow_dispatch` para esse SHA e
concluiu com `success`.

- package: `ghcr.io/sandro-prates/hermes-ai-os`;
- visibilidade: `PRIVATE`;
- vínculo: `sandro-prates/hermes-ai-os`;
- Actions access: `WRITE`;
- herança: desabilitada;
- tag: `sha-88fa6871c8e73c02270f9be45c76154d28587559`;
- manifest digest:
  `sha256:c1a2a88d5cc2493ab0a3af06be9dda4dc8c07e724b07cbdb1907273f34f19a44`;
- config digest:
  `sha256:250486f19c036207b492e7addcffca5959c2abf8ad46fe8a1c5757f025277052`;
- um dispatch, um push e nenhum rerun para o HEAD final;
- smoke console, smoke JSON e logout: `SUCCESS`;
- acesso anônimo a token efetivo, tags e manifest: negado.

O bootstrap privado separado comprovou revogação do PAT temporário, probe
pós-revogação HTTP 401 e ausência de segredo persistido.

## Histórico de correções

O Run #2 registrou a falha de política privada que originou o INC-0001. Depois da
recuperação do package privado, o Run #3 expôs a fragilidade do tratamento de
RepoDigest; `131a06e` eliminou a dependência de `sed`. O Run #4 expôs SIGPIPE nos
checks de logs dos smokes; `fb64b92` tornou esses checks seguros. Os snapshots
correspondentes foram `10517ca` e `88fa687`.

Essas falhas são histórico de diagnóstico, não alternativas ao estado aceito. Não
houve rerun do Run #5 nem segundo push para o SHA final.

## Limites preservados

Nenhum deployment foi executado. SBOM, signing e attestation não foram criados.
SPRINT-12 não foi ativada e MASTER 3 não foi criado. M1 permanece `in_progress`.
O aviso conhecido e não bloqueante do `TestClient`/`httpx` permanece registrado.

## Retomada

MASTER 2 permanece o coordenador único ativo. A retomada deve ler os documentos
canônicos, este handoff e validar o Git diretamente. Não há Sprint ou Task ativa
ou planejada; qualquer SPRINT-12 ou MASTER 3 exige autorização explícita.
