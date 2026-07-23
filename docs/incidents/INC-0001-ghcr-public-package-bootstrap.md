# INC-0001 — Bootstrap público inesperado do package GHCR

## Estado

- `failed_run=29773487377`
- `published_digest=sha256:d6705f96c24194d548b66facc4dd72904045de823e66bb0fb1f3fc3a9b687dec`
- `anonymous_pull_confirmed=true`
- `public_visibility_authorized=false`
- `package_deleted=false`
- `root_cause=not_yet_proven`
- `recovery_status=resolved`

## Evidências confirmadas

A primeira publicação externa executou login, build e um único push antes de falhar
na verificação de política privada. Auditoria read-only posterior confirmou HTTP 200
para manifest por tag, manifest por digest, lista de tags e config OCI sem credenciais.
O digest e os labels OCI correspondem ao HEAD autorizado.

```text
ROOT_CAUSE=NOT_YET_PROVEN
SOURCE_LABEL_CAUSED_PUBLIC_VISIBILITY=NOT_PROVEN
REPOSITORY_PERMISSION_INHERITANCE_CAUSED_PUBLIC_VISIBILITY=NOT_PROVEN
PREEXISTING_PACKAGE_STATE=NOT_YET_PROVEN
MANUAL_VISIBILITY_CHANGE=NOT_DETECTED_BUT_NOT_DISPROVEN
```

Visibilidade, herança de permissões, vínculo com repositório e Actions access são
controles distintos. Nenhum deles será declarado como causa sem evidência adicional.

## Contenção histórica

O package e sua tag do incidente foram preservados como evidência durante a
recuperação. A causa raiz do bootstrap público inicial não foi retroativamente
inferida.

## Recuperação concluída

O package privado foi preparado por bootstrap administrativo separado, com PAT
temporário revogado e probe pós-revogação HTTP 401. O workflow normal passou a exigir
package preexistente, metadata privada, vínculo exato, Actions access explícito,
herança desabilitada e negação de acesso anônimo antes e depois do push.

```text
FINAL_RECOVERY_RUN=29874199694
FINAL_RECOVERY_RUN_NUMBER=5
FINAL_RECOVERY_HEAD=88fa6871c8e73c02270f9be45c76154d28587559
FINAL_PACKAGE_VISIBILITY=PRIVATE
FINAL_MANIFEST_DIGEST=sha256:c1a2a88d5cc2493ab0a3af06be9dda4dc8c07e724b07cbdb1907273f34f19a44
ANONYMOUS_ACCESS=DENIED
```

As falhas intermediárias dos Runs #2, #3 e #4 registraram, respectivamente, a
política ainda não recuperada e os defeitos depois corrigidos de RepoDigest e
SIGPIPE. O Run #5 teve um dispatch, um push, nenhum rerun, smokes console/JSON e
logout aprovados. O incidente está encerrado sem apagar seu histórico.
