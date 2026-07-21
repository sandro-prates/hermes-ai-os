# INC-0001 — Bootstrap público inesperado do package GHCR

## Estado

- `failed_run=29773487377`
- `published_digest=sha256:d6705f96c24194d548b66facc4dd72904045de823e66bb0fb1f3fc3a9b687dec`
- `anonymous_pull_confirmed=true`
- `public_visibility_authorized=false`
- `package_deleted=false`
- `root_cause=not_yet_proven`
- `recovery_status=local_correction_in_progress`

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

## Contenção

O package e sua tag permanecem preservados como evidência. Não estão autorizados
exclusão, alteração de visibilidade, novo dispatch, rerun, login, pull, push ou bootstrap.

## Recuperação proposta

O workflow normal deixará de criar o primeiro package e exigirá package previamente
preparado e comprovado como privado. O preflight e o pós-push deverão validar metadata,
vínculo exato, negação de acesso anônimo e digest autenticado.

```text
PAT_BOOTSTRAP_METHOD=PROPOSED
PAT_CREATION_AUTHORIZED=NAO
BOOTSTRAP_PUSH_AUTHORIZED=NAO
```

Uma eventual operação administrativa futura poderá avaliar PAT classic temporário com
escopo candidato `write:packages`, sem `repo` e sem `delete:packages`, tag temporária
distinta, ausência inicial de `org.opencontainers.image.source`, configuração manual
de vínculo sem herança, Actions access explícito, logout e revogação imediata. Esse
método não está aprovado e depende de autorização própria.
