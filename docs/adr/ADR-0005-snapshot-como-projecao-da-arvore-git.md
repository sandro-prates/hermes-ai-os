# ADR-0005 — Snapshot como projeção determinística da árvore Git

- **Status:** Accepted
- **Data:** 2026-07-12
- **Escopo:** Continuidade técnica e tooling
- **Implementação:** Implementada, validada e oficialmente adotada

## Contexto

O primeiro formato do snapshot registrava hash, data e mensagem do HEAD e incluía
todos os caminhos retornados pela árvore Git. Uma simulação isolada comprovou uma
autorreferência: depois que `docs/PROJECT_SNAPSHOT.md` era commitado sozinho, o HEAD
mudava e o próprio arquivo passava a integrar a árvore descrita. Por isso, o conteúdo
esperado mudava imediatamente e `--check` falhava.

Metadados de commit também mudam em commits vazios, mesmo quando nenhum conteúdo do
projeto é alterado. Eles não são adequados para identificar o estado canônico que o
snapshot pretende representar.

## Decisão

Definir o snapshot canônico como uma projeção da árvore rastreada do Git em HEAD.

A projeção deve:

- ser obtida com `git ls-tree`;
- conter somente entradas rastreadas;
- excluir explicitamente `docs/PROJECT_SNAPSHOT.md`;
- excluir diretórios e arquivos gerados definidos pela ferramenta;
- ordenar entradas pelo caminho relativo;
- ser independente de branch, upstream, hash, data e mensagem de commit;
- não incorporar o estado transitório da working tree.

Cada entrada é normalizada como:

```text
<modo> <tipo> <object-id>\t<caminho>\n
```

O fingerprint da projeção é o SHA-256 da concatenação UTF-8 dessas entradas
normalizadas e ordenadas.

O estado da working tree continua sendo verificado antes da operação e exibido no
console. A geração normal é recusada quando existem alterações relevantes fora do
arquivo de saída; `--audit-working-tree` é a exceção explícita para auditoria.

O relatório oficial é `docs/PROJECT_SNAPSHOT.md`. Sua atualização integra o fluxo de
continuidade em commit exclusivo, e sua validade é comprovada sem escrita por:

```text
python tools/project_snapshot.py --check
```

## Consequências positivas

- Um commit contendo somente o snapshot não invalida o próprio snapshot.
- Commits vazios e mudanças apenas em metadados não alteram o fingerprint.
- Clones da mesma árvore projetada produzem bytes idênticos.
- Arquivos ignorados, locais e sensíveis não entram na projeção.
- Alterações em qualquer outro blob rastreado invalidam `--check`.

## Consequências negativas

- O snapshot não identifica um commit específico.
- Dois commits com a mesma árvore projetada possuem o mesmo fingerprint.
- O próprio snapshot não é protegido pelo fingerprint; adulterações são detectadas
  pela comparação integral feita por `--check`.
- Submódulos, se adotados, exigirão manter o tratamento do tipo `commit` na projeção.

## Limitações

- A inspeção de endpoints é estática e pode não reconhecer registro dinâmico de rotas.
- Resultados operacionais de Ruff, Pytest e importação são mostrados no console; o
  conteúdo canônico usa os resultados documentados na árvore commitada.
- A validade do relatório depende da execução de `--check` contra a árvore commitada;
  Git permanece responsável por comprovar commit e publicação.
