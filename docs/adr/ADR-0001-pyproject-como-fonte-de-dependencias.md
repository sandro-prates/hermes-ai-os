# ADR-0001 — `pyproject.toml` como fonte principal do projeto Python

- **Status:** Accepted
- **Data:** 2026-07-12
- **Escopo:** Backend Python
- **Implementação:** Concluída e commitada em `a1d0d21`

## Contexto

O ambiente virtual já possuía dependências instaladas, mas o repositório não continha `requirements.txt` nem `pyproject.toml`.

Sem uma declaração versionada de dependências, o ambiente não era reproduzível.

O Hermes AI OS pretende funcionar localmente, em containers, nuvem e instalações comerciais. Esses cenários exigem uma fonte explícita de metadados, compatibilidade Python, dependências e ferramentas de qualidade.

## Decisão

Adotar `pyproject.toml` como fonte principal para:

- metadados do projeto;
- versão mínima e máxima suportada do Python;
- dependências diretas;
- dependências opcionais de desenvolvimento;
- configuração do pytest;
- configuração do Ruff;
- configuração futura de build e distribuição.

Não usar `pip freeze` como definição principal de dependências, porque ele mistura dependências diretas e transitivas.

## Consequências positivas

- Ambiente reproduzível.
- Melhor preparação para distribuição.
- Configuração centralizada.
- Base adequada para Open Core, plugins e empacotamento.
- Menor acoplamento às versões transitivas atuais do ambiente virtual.

## Consequências negativas

- As dependências declaradas precisam ser mantidas manualmente.
- Será necessário adotar posteriormente uma estratégia de lock para builds totalmente reproduzíveis.
- Compatibilidade entre Python 3.12, 3.13 e 3.14 ainda precisa ser testada.

## Estado verificado

O arquivo `pyproject.toml` está rastreado e commitado em `a1d0d21`. Ele é carregado
pelo pytest após a remoção de um UTF-8 BOM e também define os metadados, dependências
e configurações do Ruff.
