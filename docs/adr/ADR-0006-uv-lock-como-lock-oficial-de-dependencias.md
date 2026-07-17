# ADR-0006 — uv.lock como lock oficial de dependências

- **Status:** Accepted
- **Data:** 17/07/2026
- **Escopo:** M0 — Foundation / SPRINT-07 — Dependency Reproducibility Proof

## Contexto

O `pyproject.toml` já era a fonte declarativa de configuração e dependências Python,
mas o repositório ainda não possuía um lockfile oficial versionado. A SPRINT-07
avaliou a resolução de dependências com `uv 0.11.28` e comprovou que duas
resoluções independentes produziram arquivos `uv.lock` byte-idênticos.

O lock canônico foi gerado com:

- versão completa: `uv 0.11.28 (ebf0f43d7 2026-07-07 x86_64-pc-windows-msvc)`;
- SHA-256 do executável: `533FE4044BC50B05AC89F4D07925597FDB5285369724E8986ECAB356818F09EE`;
- índice explícito: `https://pypi.org/simple`;
- cutoff: `2026-07-14T11:53:48.187Z`;
- tamanho: `135871 bytes`;
- SHA-256 do lock: `6F43C7C21D2DAB65E9FEDDC72958BCB20D8823DA3DBE761AEE8AB134A40E6923`.

A prova foi validada no Windows com Python `3.14.6` e em Docker Desktop
Linux/WSL2 com Python `3.12.13`, `3.13.14` e `3.14.6`. Ruff, 76 testes com
1 warning conhecido, importação, endpoints, Request ID, logging e snapshot
foram aprovados nos ambientes aplicáveis.

O estado atual do servidor remoto não foi confirmado. A decisão não inclui
implementação de CI nem adoção oficial de `pylock.toml`. A exportação e o
consumo do pylock pelo uv permanecem somente como evidência experimental;
interoperabilidade de terceiros não foi comprovada.

## Decisão

1. O `pyproject.toml` permanece como fonte declarativa das dependências Python.
2. O `uv.lock` passa a ser o lock oficial, versionado e reproduzível do projeto.
3. Instalações reproduzíveis devem consumir o lock sem modificá-lo.
4. Testes, validações, onboarding e futura CI não podem atualizar o lock
   incidentalmente.
5. Mudanças de dependências exigem uma atualização deliberada e planejada do
   `uv.lock`.
6. Toda atualização deliberada deve registrar a versão completa do uv, o índice
   utilizado e o cutoff ou política temporal equivalente.
7. O diff completo do lock deve ser revisado como artefato de segurança e
   supply chain.
8. A atualização deve validar integridade do TOML, ambiente limpo, Ruff, Pytest,
   importação, endpoints, Request ID, logging, snapshot e a matriz Python
   aplicável.
9. Mudanças no lock devem usar commit específico e não podem ser misturadas
   silenciosamente com mudanças funcionais.
10. `pylock.toml` não é artefato oficial do Hermes AI OS nesta Sprint.

## Consequências positivas

- versões diretas e transitivas ficam fixadas em um artefato auditável;
- onboarding e reconstrução de ambientes tornam-se mais previsíveis;
- a paridade comprovada entre Windows e Linux passa a ter uma baseline oficial;
- mudanças de dependências passam a produzir diffs explícitos e revisáveis;
- futuras validações e CI poderão consumir o lock de forma fail-closed.

## Consequências e limitações

- atualizações de dependências passam a exigir um processo deliberado;
- a disponibilidade futura dos artefatos no índice não é garantida somente pelo
  lockfile;
- a prova Linux ocorreu em Docker Desktop/WSL2, não em host físico Linux
  administrado separadamente;
- CI ainda não foi implementada nem validada;
- interoperabilidade de terceiros do `pylock.toml` não foi comprovada;
- a adoção local do lock não equivale a publicação remota;
- `origin/main` continua sendo apenas a referência remota local conhecida até
  futura operação de rede autorizada.

## Política de atualização

Uma atualização futura do `uv.lock` deve ocorrer em mudança planejada e seguir,
no mínimo, este fluxo:

1. alterar deliberadamente a declaração aplicável no `pyproject.toml`;
2. registrar a versão completa e o SHA-256 do uv;
3. registrar o índice explícito e o cutoff ou política temporal equivalente;
4. gerar ou atualizar o lock sem misturar mudança funcional não relacionada;
5. revisar integralmente o diff do lock;
6. validar o TOML e uma instalação em ambiente limpo;
7. executar Ruff, Pytest, importação, endpoints, Request ID e logging;
8. executar o snapshot e a matriz Python aplicável;
9. atualizar a documentação viva;
10. criar commit específico para a mudança de dependências e lock.

Comandos de consumo devem usar modo bloqueado, como `uv sync --locked`, quando
aplicável. Comandos de validação não devem regenerar ou modificar o lock.

## Relação com decisões anteriores

Esta decisão complementa o ADR-0001. O `pyproject.toml` continua sendo a fonte
declarativa; o `uv.lock` fixa a resolução reproduzível correspondente. Nenhum
ADR anterior é substituído.
