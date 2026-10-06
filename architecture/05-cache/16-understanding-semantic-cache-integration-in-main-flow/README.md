# Aula 16 — Entendendo a integração do cache semântico no fluxo principal

> Curso: **Cache** · Duração: `04:02`

## Material e foco da aula

Os quatro prints posicionam a camada semântica depois do cache exato e antes do modelo.
[02.png](02.png) mostra o endpoint; [04.png](04.png) resume a cadeia de prioridade.
Não há fluxo de RAG, ingestão de documentos ou chunking nesta integração.

## Cascata observada

```text
requisição → fingerprint → cache exato em memória
  hit exato → retorna análise; sem embedding, banco ou chat
  miss exato → gera embedding → busca candidatos no pgvector → avalia melhor
    hit semântico → retorna análise armazenada; sem chat
    miss semântico → chama chat → grava resultado elegível → retorna
```

A ordem tenta primeiro a operação de menor custo. Gerar embedding em toda requisição,
inclusive no hit exato, adicionaria trabalho desnecessário.

## Complemento de estudo: custo das camadas

Se `h_e` é a taxa de hit exato e `h_s` a taxa semântica **condicionada ao miss exato**:

```text
fração de chamadas de chat evitadas = h_e + (1 - h_e) × h_s
fração que gera embedding          = 1 - h_e
fração que chama chat              = (1 - h_e) × (1 - h_s)
```

As contas assumem requisições elegíveis, disponibilidade das camadas e decisões de qualidade
já aprovadas. Não calculam sozinhas dinheiro economizado: inclua custo de embedding, consulta,
armazenamento e escrita. Para latência, meça distribuições por caminho; toda consulta semântica
também acrescenta tempo ao miss.

A disponibilidade muda com a ordem: hit exato não depende do banco, mas o miss exato do projeto
depende de embedding e leitura SQL antes de chegar ao chat.

## Diagrama e implementação têm limites diferentes

[03.png](03.png) sugere armazenar em cache exato tanto o resultado novo quanto o hit semântico.
O [código consolidado](../mba-ia-cache/main.py) grava `CACHE[key]` somente após inferência:
**hit semântico não promove a entrada para o cache exato**. Repetir essa consulta pode continuar
gerando embedding e acessando o banco. Documentar essa diferença ajuda a interpretar os testes.

Também não há fallback implementado para falha de geração de embedding ou leitura SQL.
A captura de erro na gravação semântica não cobre essas operações anteriores.

## Validade continua obrigatória

Um candidato acima do limiar não é automaticamente “seguro”. Contexto, escopo e contrato
precisam ser compatíveis. Cache-aside permite essa política explícita, mas não fornece
consistência automática. [Referência: Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).

## Exercício

Com 40% de hit exato e 50% de hit semântico entre os misses exatos, qual fração das requisições
ainda chama o modelo de chat? Qual fração continua precisando de embedding?
