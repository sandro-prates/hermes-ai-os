# ADR-0009 — Política de publicação do artefato de container

- **Status:** Accepted
- **Data:** 20/07/2026
- **Escopo:** M1 / SPRINT-11 — Controlled Container Artifact Publication

## Contexto

A baseline reproduzível de container Linux já é validada pelo Quality Gate e pelo
Container Gate. Falta estabelecer como uma revisão já aprovada pode ser publicada
como artefato imutável, sem transformar a publicação em deployment nem ampliar as
credenciais do repositório.

## Decisão

Publicar no GHCR sob o namespace
`ghcr.io/sandro-prates/hermes-ai-os`, com visibilidade obrigatoriamente privada e
vínculo obrigatório ao repositório `sandro-prates/hermes-ai-os`. A publicação normal usa somente o `GITHUB_TOKEN`; PAT e segredo persistente
adicional são proibidos no workflow normal. Um eventual PAT classic temporário para
bootstrap administrativo externo é apenas proposta e exige autorização separada.

O workflow é exclusivamente manual (`workflow_dispatch`) e exige confirmação
humana, branch `main` e SHA Git integral de 40 caracteres igual ao SHA da execução.
Antes de publicar, consulta separadamente o Quality Gate e o Container Gate e
aceita apenas runs de `push`, concluídos com sucesso, no mesmo SHA e branch.

As permissões são mínimas por job: `actions: read` e `contents: read` para a
verificação; `contents: read` e `packages: write` para a publicação. Não há
permissões globais.

## Identidade, tags e plataforma

A única tag permitida é `sha-<FULL_40_CHARACTER_SHA>`. Tags flutuantes, `latest`,
SHA curto, sobrescrita, rebuild e no-op idempotente quando a tag já existe são
proibidos. A imagem é construída localmente uma única vez para `linux/amd64`, sem
push no build, multi-arch, QEMU ou cache externo.

O build aplica os labels OCI `source`, `revision`, `version` e `title`. Não declara
licença sem comprovação contratual separada.

## Preflight fail-closed

São realizados dois preflights autenticados pela Registry HTTP API V2: um após o
login e antes do build; outro imediatamente antes do push. Somente uma resposta
autenticada, válida e inequívoca `MANIFEST_UNKNOWN` confirma
`TAG_CONFIRMED_ABSENT=SIM`.

Tag existente, unauthorized, forbidden, timeout, erro de rede ou TLS, rate limit,
erro de registry, resposta vazia, JSON inválido, HTTP inesperado, 404 ambíguo e
token vazio ou inválido encerram o job. Um exit code genérico e `docker manifest
inspect` não classificam ausência.

## Digest e validação posterior

O digest canônico é o manifest digest no formato `sha256:<64 hex>`. Após o único
push, o workflow exige igualdade entre o digest final ancorado reportado pelo
push, o header `Docker-Content-Digest` consultado no registry e o `RepoDigest` da
imagem removida localmente e puxada exclusivamente por digest.

A referência canônica resultante é
`ghcr.io/sandro-prates/hermes-ai-os@sha256:<registry_manifest_digest>`. Image ID,
config digest, layer digest, cache digest e build ID não servem como evidência.
Uma API autenticada também deve provar visibilidade `private` e vínculo ao
repositório esperado; o workflow não corrige visibilidade ou permissões.

## Contrato de runtime

Somente o artefato puxado por digest participa do smoke final. Ele deve comprovar
`linux/amd64`, Python 3.14.6, usuário `10001:10001`, filesystem read-only,
healthcheck saudável, `GET /`, `GET /api/v1/health`, Request ID gerado e preservado,
logging console e JSON e ausência de pytest, Ruff, httpx, uv, tests e docs.

## Retenção, logout e limites

A retenção é manual; esta decisão não autoriza exclusão ou sobrescrita automática.
O workflow distingue login não tentado, tentado não confirmado e bem-sucedido.
Após qualquer tentativa há logout defensivo em etapa `always()`, obrigatório e
falhável quando o login foi confirmado.

Deployment, Compose, multi-arch, attestation, SBOM e signing permanecem fora de
escopo. A publicação não usa PAT e não concede autorização de deployment.

## Riscos residuais

- indisponibilidade ou mudança operacional das APIs do GitHub e GHCR;
- corrida externa entre o segundo preflight e o push, tratada como falha, nunca
  como autorização para sobrescrever;
- retenção e recuperação dependem de operação manual futura autorizada;
- o `GITHUB_TOKEN` depende das políticas e permissões efetivas do repositório.

## Rollback

O rollback técnico ocorre por commit Git normal que remova o workflow ou restaure
sua versão anterior. Artefatos já publicados não são alterados ou excluídos por
este workflow; qualquer ação no package exige autorização operacional separada.

## Critérios de aceitação

1. Os testes contratuais e todos os gates locais passam sem alterar arquivos
   protegidos.
2. Quality Gate e Container Gate aprovam o mesmo SHA de `push` em `main`.
3. Uma execução manual futura autorizada confirma ausência duas vezes e publica
   exatamente uma tag integral, sem sobrescrita.
4. Os três manifest digests são válidos e iguais.
5. Visibilidade privada, vínculo ao repositório, pull por digest e smoke completo
   são comprovados.
6. O logout obrigatório conclui com sucesso.

Os seis critérios foram satisfeitos pela publicação final autorizada da baseline
`88fa6871c8e73c02270f9be45c76154d28587559`. O Quality Gate #12 e o Container Gate
#10 foram aprovados; o Publish Container Run #5 (attempt 1) concluiu com sucesso,
com um dispatch, um push, nenhum rerun, smokes console e JSON aprovados e logout
concluído.

## Emenda de recuperação do package privado da SPRINT-11

O workflow normal não cria o primeiro package. A publicação exige package GHCR
preexistente, metadata `private`, vínculo exato com `sandro-prates/hermes-ai-os`,
Actions access explicitamente configurado e herança de acesso desabilitada.

Antes do login e do build, e novamente depois de um futuro push, o workflow executa
metadata autenticada e probe anônimo completo do Registry V2. Challenge HTTP 401
isolado não comprova privacidade. O gate somente aprova quando token com acesso efetivo
de pull, lista de tags e manifestos não são obtidos anonimamente.

O workflow não corrige visibilidade, vínculo, herança, Actions access, package ou tags.
Falhas de autenticação, autorização, rede, rate limit, JSON ou campos ausentes são
bloqueantes. Publicações normais continuam usando exclusivamente `github.token`.

O incidente do run `29773487377` publicou o digest
`sha256:d6705f96c24194d548b66facc4dd72904045de823e66bb0fb1f3fc3a9b687dec`
e comprovou acesso anônimo, sem autorização de visibilidade pública. A causa raiz
permanece não comprovada; o package atual permanece evidência até gate destrutivo.

O bootstrap administrativo privado foi executado como operação externa separada.
A evidência aprovada comprova revogação do PAT temporário, probe pós-revogação HTTP
401 e ausência de segredo persistido. O workflow normal final permaneceu restrito ao
`github.token`.

```text
FINAL_PACKAGE_VISIBILITY=PRIVATE
FINAL_MANIFEST_DIGEST=sha256:c1a2a88d5cc2493ab0a3af06be9dda4dc8c07e724b07cbdb1907273f34f19a44
FINAL_REPOSITORY_LINK=sandro-prates/hermes-ai-os
ADR_0009_ACCEPTANCE_CRITERIA_SATISFIED=6_OF_6
```

Os commits `131a06e` e `fb64b92` corrigiram, respectivamente, a validação de
RepoDigest sem `sed` e o risco de SIGPIPE nos checks de logs dos smokes. As falhas
intermediárias dos Runs #2, #3 e #4 permanecem como histórico; somente o Run #5 da
baseline final constitui a aceitação.

Deployment, SBOM, signing e attestation não foram executados.

**Status da decisão:** `Accepted` em 23/07/2026.
