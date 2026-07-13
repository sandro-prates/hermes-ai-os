# Hermes AI OS — Technology Decision Baseline

## 1. Identificação

- Projeto: Hermes AI OS.
- Milestone: M0 — Foundation.
- Sprint: SPRINT-05 — Technology Decision Baseline.
- Item formal: DT-007 — Pesquisa tecnológica.
- Data da revisão: 13/07/2026.
- Natureza: pesquisa e recomendações; nenhuma decisão arquitetural é aceita por este
  documento.

## 2. Objetivo e limites

Esta pesquisa reduz a incerteza necessária para planejar M1 e M2 sem adicionar
dependências, lockfile, workflow de CI, infraestrutura ou código de produto.

Temas decisórios desta baseline:

1. gerenciamento e lock de dependências;
2. matriz oficial de versões do Python;
3. quality gate e CI.

Persistência, migrations, filas, workers, agentes, modelos, cloud, memória, dashboard
e integrações são apenas preparados em matriz compacta. As classificações deste
documento significam:

- **adotar:** recomendação madura para aprovação humana posterior;
- **prototipar:** exige prova isolada antes de decisão;
- **adiar:** decisão não necessária no horizonte imediato;
- **rejeitar:** inadequada aos requisitos atuais;
- **pendente:** evidência insuficiente ou dependência ainda aberta.

Nenhuma classificação equivale a adoção, implementação ou ADR aceito.

## 3. Princípios e critérios

### 3.1 Princípios obrigatórios

- **Local First:** desenvolvimento e operação básica devem funcionar sem serviço
  cloud obrigatório.
- **Cloud Ready:** decisões locais não devem impedir implantação remota posterior.
- **Open Core:** o núcleo deve permanecer auditável e independente de oferta
  comercial proprietária.
- **Modularidade:** persistência, modelos, filas e integrações devem possuir fronteiras
  substituíveis.
- **Reprodutibilidade:** dependências, Python e quality gates devem produzir evidência
  repetível.
- **Custo progressivo:** complexidade operacional só entra quando um requisito a
  justificar.
- **Portabilidade:** Windows é ambiente de primeira classe; Linux deve ser coberto no
  gate automatizado antes de implantação.
- **Neutralidade de provedor:** nenhuma interface de modelo deve exigir um único
  provedor remoto.

### 3.2 Critérios de comparação

| Critério | Pergunta objetiva |
|---|---|
| Reprodutibilidade | A mesma entrada produz resolução e ambiente verificáveis? |
| Portabilidade | Windows, Linux e Python suportados são representados? |
| Fonte canônica | A relação com `pyproject.toml` é explícita e verificável? |
| Segurança | Há hashes, permissões mínimas e atualização controlada? |
| Manutenção | O processo de atualização é pequeno, documentável e auditável? |
| Lock-in | O artefato pode ser exportado ou consumido por outro ecossistema? |
| Custo | Exige serviço, runner ou operação permanente? |
| Maturidade | A capacidade é estável ou ainda experimental/pré-release? |

## 4. Decisão 1 — gerenciamento e lock de dependências

### 4.1 Estado atual

`pyproject.toml` é a fonte declarativa do projeto e contém intervalos de versões, mas
não registra uma resolução completa. Instalações realizadas em momentos diferentes
podem selecionar versões transitivas diferentes.

### 4.2 Alternativas avaliadas

| Alternativa | Evidência | Vantagens | Limitações | Classificação |
|---|---|---|---|---|
| `uv.lock` gerenciado por uv | A documentação do uv define lockfile universal/cross-platform, verificação com `uv lock --check`, sincronização exata e exportação para `requirements.txt` ou `pylock.toml`. | Um artefato para marcadores de SO/Python; integra projeto e ambiente; atualização explícita; boa aderência a Windows e Linux. | Formato nativo específico do uv; introduz ferramenta nova; precisa comprovar compatibilidade com extras atuais e Python 3.12–3.14. | **prototipar** |
| `pylock.toml` por `pip lock` | PEP 751 padroniza `pylock.toml`; pip 26.1.2 oferece `pip lock`. | Formato padronizado e independente de ferramenta; permanece próximo do fluxo pip atual. | O comando é explicitamente experimental e o arquivo gerado só é garantido para a versão do Python e plataforma correntes. | **adiar** como fonte única agora |
| Constraints/requirements com hashes | pip suporta constraints e `--require-hashes`. | Ferramentas já conhecidas; controle explícito por ambiente. | Exige disciplina e possivelmente múltiplos artefatos por plataforma/Python; duplica parte da declaração do `pyproject.toml`; não resolve sozinho a matriz universal. | **adiar** como fallback |

### 4.3 Recomendação

**Prototipar uv em Sprint própria, sem adoção automática.** A prova deve:

1. gerar um `uv.lock` a partir do `pyproject.toml` sem alterar dependências;
2. validar Python 3.12, 3.13 e 3.14 em Windows e Linux;
3. comprovar `uv lock --check` e sincronização com extras de desenvolvimento;
4. documentar atualização controlada e rollback via Git;
5. avaliar exportação para `pylock.toml` como saída interoperável;
6. medir o diff e confirmar que `pyproject.toml` continua sendo a declaração humana.

Gate de adoção: aprovação humana após a prova. Até lá, não existe ferramenta de lock
oficial no Hermes AI OS.

## 5. Decisão 2 — matriz oficial de Python

### 5.1 Evidência oficial em 13/07/2026

O projeto declara `requires-python = ">=3.12,<3.15"`. A página de versões do Python,
atualizada em 27/05/2026, registra:

| Versão | Estado upstream | Fim de suporte previsto | Relação com o projeto |
|---|---|---|---|
| 3.12 | security | 2028-10 | suportada pelo intervalo; sem novos binários regulares upstream |
| 3.13 | bugfix | 2029-10 | suportada e candidata à matriz principal |
| 3.14 | bugfix | 2030-10 | suportada e runtime local verificado nesta baseline |
| 3.15 | prerelease | 2031-10 | excluída pelo limite `<3.15`; apenas observação futura |

### 5.2 Política recomendada

- **adotar após aprovação humana:** Python 3.12, 3.13 e 3.14 como matriz formal.
- Executar o gate completo nas três versões em Linux.
- Executar ao menos Python 3.14 em Windows por ser o ambiente operacional atual; a
  expansão Windows 3.12/3.13 depende de custo de runner e evidência de valor.
- Fixar explicitamente `python-version` no CI; não depender do Python implícito do
  runner.
- Tratar 3.12 como compatibilidade de segurança/legado, não como runtime preferencial
  para novos ambientes.
- Não ampliar para 3.15 enquanto estiver pré-release e fora de `requires-python`.
- Revisar a matriz a cada release anual do Python ou quando uma dependência direta
  retirar suporte.

### 5.3 Gate para mudança

Qualquer alteração de `requires-python` deve verificar wheels das dependências diretas,
suíte completa, importação, endpoints, Request ID e lock. Esta pesquisa não altera o
intervalo atual.

## 6. Decisão 3 — quality gate e CI

### 6.1 Alternativas

| Alternativa | Vantagens | Limitações | Classificação |
|---|---|---|---|
| GitHub Actions com `actions/setup-python` | Integrado ao remoto atual; matriz de Python e SO; permissões `contents: read`; cache opcional; documentação oficial para projetos Python. | Depende da decisão de lock para instalações reproduzíveis; consumo de minutos; ações precisam ser fixadas e revisadas. | **prototipar após lock** |
| Gate somente local documentado | Nenhum serviço externo; já funciona no PowerShell. | Não impede regressão remota nem comprova Linux/matriz Python automaticamente. | **manter como fallback**, não como estado final |

### 6.2 Gate mínimo recomendado

Quando autorizado, o workflow candidato deve ser somente leitura sobre o repositório,
com permissões mínimas e estes passos:

1. checkout;
2. setup explícito da versão do Python;
3. instalação reproduzível a partir da estratégia de lock aprovada;
4. `python tools/project_snapshot.py --check`;
5. `python -m ruff check .`;
6. `python -m pytest`;
7. importação de `app.main`;
8. nenhum formatter com `--fix`, commit automático ou publicação.

Matriz inicial candidata:

- Ubuntu: Python 3.12, 3.13 e 3.14;
- Windows: Python 3.14;
- expansão posterior condicionada a tempo, custo e falhas específicas.

O `setup-python` recomenda versão explícita e oferece cache, mas cache não substitui
lock. Ruff pode rodar pela instalação de desenvolvimento já fixada; usar uma action
separada com versão `latest` criaria uma segunda fonte de versão e não é recomendado
para o primeiro gate.

### 6.3 Recomendação

**Prototipar GitHub Actions somente após decidir o lock.** A aceitação do workflow,
permissões, versões das actions e política de proteção de branch exige aprovação
humana separada.

## 7. Dependências entre decisões

```text
política Python
      ↓
prova de lock multiplataforma
      ↓
quality gate reproduzível
      ↓
infraestrutura e produto
```

CI antes do lock automatizaria uma instalação variável. Lock antes da matriz poderia
omitir plataformas relevantes. Por isso, a matriz Python é a política de entrada, a
prova de lock é o próximo incremento e CI vem depois.

## 8. Matriz preparatória dos temas adiados

| Tema | Requisitos principais | Dependências | Riscos | Alternativas de referência | Milestone provável | Motivo do adiamento |
|---|---|---|---|---|---|---|
| Persistência e migrations | Local simples, transações, evolução de schema, caminho cloud | lock e modelo de domínio mínimo | divergência SQLite/PostgreSQL; migrations prematuras | SQLite + Alembic; PostgreSQL + Alembic | M1 | não há modelo de domínio nem requisito de concorrência |
| Filas e workers | idempotência, retry, observabilidade, execução local | persistência, contratos de jobs, broker | entrega duplicada, operação de broker, shutdown | Celery; Dramatiq | M2 | nenhum job assíncrono de produto existe |
| Runtime/framework de agentes | estado explícito, ferramentas, cancelamento, testes | abstração de modelos e persistência | lock-in de framework, churn de APIs, semântica oculta | núcleo próprio fino; LangGraph ou Pydantic AI em protótipo comparativo | M2 | requisitos de agentes ainda não foram implementados |
| Abstração de modelos | local/remoto, streaming, ferramentas, erros e custo | contrato do runtime e segurança de credenciais | menor denominador comum, diferenças entre provedores | protocolo interno + adaptadores; LiteLLM/Ollama como referências | M2 | nenhum provedor faz parte do produto atual |
| Cloud e distribuição | imagem reproduzível, configuração externa, health e rollback | lock, CI, persistência | custo operacional e complexidade precoce | Docker/Compose; plataforma gerenciada antes de Kubernetes | M1/M2 | Local First ainda não exige orquestrador |
| Memória | escopo, retenção, isolamento, busca e exclusão | persistência e runtime de agentes | vazamento de dados, custo, irreversibilidade | PostgreSQL/pgvector; Qdrant | M3 | não existe agente nem política de dados |
| Dashboard | contrato de API, autenticação, eventos e acessibilidade | backend de produto estável | acoplamento visual prematuro | UI web separada; Streamlit apenas para protótipo interno | M4 | API atual expõe somente raiz e health |
| Integrações | autenticação, idempotência, rate limit, auditoria | modelo de extensão e segurança | segredos, contratos externos, lock-in | webhooks/OpenAPI; SDK de plugins próprio | M5 | nenhum caso de integração foi priorizado |

As alternativas acima são referências para pesquisa futura, não escolhas.

## 9. Segurança, custo e operação

- Lockfiles e workflows devem ser revisados como código.
- Actions deverão usar permissões mínimas; autenticação e publicação ficam fora do
  quality gate inicial.
- Credenciais nunca entram em `.env.example`, logs, cache ou artefatos.
- Atualizações de dependências devem ser explícitas, pequenas e validadas em matriz.
- Serviços persistentes, brokers e clusters não são justificados no M0.
- Local First não significa ausência de segurança: isolamento de dados, exclusão e
  backup precisam anteceder memória e persistência de usuário.
- Open Core exige que formatos e interfaces essenciais não dependam de serviço
  proprietário obrigatório.

## 10. Recomendações consolidadas

| Assunto | Recomendação | Estado após esta pesquisa |
|---|---|---|
| Python | matriz 3.12–3.14, com Linux completo e Windows 3.14 inicial | pendente de aprovação humana |
| Lock | prova isolada de `uv.lock`, incluindo exportação `pylock.toml` | prototipar |
| `pip lock` | acompanhar estabilização; não usar como fonte única agora | adiar |
| CI | GitHub Actions após lock, sem correção ou publicação automática | prototipar depois do lock |
| Infraestrutura/produto | manter matriz preparatória e pesquisar quando houver requisito | adiar |
| ADRs | criar somente após decisão humana sobre política concreta | nenhum criado |

## 11. Sequência recomendada

### SPRINT-06 candidata — Dependency Reproducibility Proof

- Validar formalmente a matriz Python 3.12–3.14.
- Prototipar uv sem mudar dependências.
- Comparar `uv.lock` e exportação `pylock.toml`.
- Validar Windows e Linux em ambientes descartáveis.
- Submeter a adoção e eventual ADR à aprovação humana.

### SPRINT-07 candidata — Automated Quality Gate

- Depende da decisão de lock da SPRINT-06.
- Prototipar GitHub Actions com permissões mínimas.
- Executar snapshot check, Ruff, Pytest e importação na matriz aprovada.
- Não publicar artefatos nem alterar arquivos automaticamente.

Essas Sprints são candidatas; não estão planejadas ou ativadas por esta pesquisa.

## 12. Conclusão da DT-007

A pesquisa fornece critérios, alternativas, riscos, recomendações e adiamentos
verificáveis. Sua conclusão significa apenas que a investigação foi preenchida,
revisada e commitada. Não significa adoção de uv, `pylock.toml`, GitHub Actions,
Python adicional, banco, fila, framework, provedor ou ADR.

## 13. Fontes primárias

Todas as fontes foram consultadas em 13/07/2026.

| Fonte | Mantenedor | Versão/data disponível | URL |
|---|---|---|---|
| Locking and syncing — uv | Astral | documentação contínua; uv 0.11.21 publicado em 11/06/2026 | https://docs.astral.sh/uv/concepts/projects/sync/ |
| Structure and files — uv | Astral | documentação consultada em 13/07/2026 | https://docs.astral.sh/uv/concepts/projects/layout/ |
| uv releases | Astral | 0.11.21, 11/06/2026 | https://github.com/astral-sh/uv/releases |
| `pip lock` | Python Packaging Authority | pip 26.1.2; capacidade marcada experimental | https://pip.pypa.io/en/stable/cli/pip_lock/ |
| PEP 751 — lockfile `pylock.toml` | Python Software Foundation | Final; resolução em 31/03/2025 | https://peps.python.org/pep-0751/ |
| Status of Python versions | Python Software Foundation | página atualizada em 27/05/2026 | https://devguide.python.org/versions/ |
| Building and testing Python | GitHub | documentação contínua | https://docs.github.com/en/actions/tutorials/build-and-test-code/python |
| `actions/setup-python` | GitHub | v6.2.0, 22/01/2026 | https://github.com/actions/setup-python |
| Integrations — Ruff | Astral | exemplos com Ruff 0.15.21; documentação contínua | https://docs.astral.sh/ruff/integrations/ |
| About SQLite / Transactions | SQLite Project | documentação contínua consultada em 13/07/2026 | https://www.sqlite.org/about.html |
| PostgreSQL current documentation | PostgreSQL Global Development Group | PostgreSQL 18 current na consulta | https://www.postgresql.org/docs/current/ |
| Alembic documentation | SQLAlchemy | 1.18.5 na consulta | https://alembic.sqlalchemy.org/en/latest/ |
| Celery workers/tasks | Celery Project | 5.6.2 na documentação latest | https://docs.celeryq.dev/en/latest/userguide/workers.html |
| Dramatiq User Guide | Dramatiq maintainers | 2.2.0 na consulta | https://dramatiq.io/guide.html |
| LangGraph overview | LangChain | documentação contínua | https://docs.langchain.com/oss/python/langgraph/overview |
| Pydantic AI overview/releases | Pydantic | v1.104.0 e v2.0.0b4 em 28/05/2026 | https://github.com/pydantic/pydantic-ai/releases |
| LiteLLM documentation | BerriAI | documentação contínua; releases recentes incluem RCs | https://docs.litellm.ai/ |
| Docker overview | Docker | documentação contínua | https://docs.docker.com/get-started/docker-overview/ |
| Kubernetes concepts | Kubernetes Authors / CNCF | documentação contínua | https://kubernetes.io/docs/concepts/ |
