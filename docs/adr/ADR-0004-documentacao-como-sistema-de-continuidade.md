# ADR-0004 — Documentação viva como sistema formal de continuidade

- **Status:** Accepted
- **Data:** 2026-07-12
- **Escopo:** Todo o projeto
- **Implementação:** Em andamento

## Contexto

O Hermes AI OS será desenvolvido ao longo de múltiplas Sprints, conversas e possivelmente por diferentes assistentes de IA.

Depender exclusivamente do histórico de uma conversa cria riscos:

- perda de contexto;
- decisões contraditórias;
- status incorretos;
- repetição de trabalho;
- mudanças sem rastreabilidade;
- dificuldade para retomar o projeto.

## Decisão

Adotar os seguintes documentos como sistema formal de continuidade:

- `docs/00_PROJECT_MASTER.md`: visão, princípios e entrada principal;
- `docs/01_PROJECT_STATE.yaml`: estado operacional verificável;
- `docs/02_BACKLOG.md`: trabalho concluído, atual, pendente e dívida técnica;
- `docs/03_CHANGELOG.md`: histórico de mudanças;
- `docs/adr/`: decisões arquiteturais.

O estado deve ser validado contra:

- Git;
- código;
- testes;
- análise estática;
- execução manual quando aplicável.

## Ordem de retomada

Uma nova conversa ou assistente deve:

1. ler `00_PROJECT_MASTER.md`;
2. ler `01_PROJECT_STATE.yaml`;
3. ler `02_BACKLOG.md`;
4. ler `03_CHANGELOG.md`;
5. ler os ADRs aceitos;
6. executar `git status --short --branch`;
7. validar divergências antes de implementar.

## Consequências positivas

- Continuidade entre conversas.
- Menor dependência de memória informal.
- Melhor governança.
- Maior rastreabilidade para colaboradores e clientes Enterprise.
- Base para automação futura de status e releases.

## Consequências negativas

- Custo contínuo de manutenção.
- Documentação pode ficar desatualizada se a Definition of Done não for seguida.
- Dados derivados do Git podem envelhecer rapidamente.
- Exige disciplina antes de commits e encerramento de Sprints.

## Regra de consistência

Quando houver divergência:

1. código e Git determinam o que existe;
2. testes determinam o que foi validado;
3. documentação deve ser corrigida;
4. nenhum status deve ser inventado para preencher lacunas.