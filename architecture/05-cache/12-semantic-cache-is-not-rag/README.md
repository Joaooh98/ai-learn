# Aula 12 — Cache semântico não é RAG

> Curso: **Cache** · Duração: `04:20`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Embeddings, similaridade e um banco vetorial são peças usadas tanto em cache semântico quanto em
RAG (Retrieval-Augmented Generation), o que gera confusão comum entre os dois conceitos. Esta aula
existe para marcar a diferença antes de a implementação prática começar (aulas 13 em diante).

## A diferença

- **RAG**: busca documentos/trechos relevantes em uma base de conhecimento para **alimentar o
  prompt** antes de chamar o modelo. O objetivo é dar mais contexto para o modelo gerar uma
  resposta melhor ou mais atualizada. O modelo é sempre chamado.
- **Cache semântico**: busca se uma pergunta **parecida** já foi respondida antes, para
  **reaproveitar a resposta** e evitar chamar o modelo de novo. O objetivo é economizar tempo e
  custo, não enriquecer o prompt.

```text
RAG:            pergunta -> busca contexto -> monta prompt com contexto -> chama modelo
Cache semântico: pergunta -> busca resposta parecida -> hit: retorna sem chamar modelo
                                                       -> miss: chama modelo normalmente
```

## Ideia-chave

Os dois usam a mesma infraestrutura (embeddings + busca por similaridade), mas resolvem problemas
diferentes: RAG melhora a qualidade/atualidade da resposta; cache semântico evita reprocessar uma
pergunta equivalente. Um sistema pode ter os dois ao mesmo tempo, em pontos diferentes do fluxo.
