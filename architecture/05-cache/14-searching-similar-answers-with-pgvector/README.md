# Aula 14 — Buscando respostas parecidas com pgvector

> Curso: **Cache** · Duração: `08:00`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Com os embeddings sendo salvos no pgvector (aula 13), esta aula implementa a busca: dado o
embedding de uma pergunta nova, encontrar a entrada mais parecida já armazenada, usando os
operadores de distância/similaridade do pgvector.

## O que a aula deve cobrir

- Consulta ao pgvector ordenando os resultados por distância/similaridade em relação ao vetor da
  pergunta nova (busca do vizinho mais próximo).
- Recuperação da resposta associada à entrada mais parecida encontrada.
- Ligação com o conceito de threshold (aula 11) para decidir se o resultado encontrado é
  parecido o suficiente para ser tratado como hit.

## Ideia-chave

Esta aula fecha o ciclo básico de busca do cache semântico: gerar embedding da entrada, buscar o
vizinho mais próximo no pgvector e comparar a distância com o threshold. A aula 15 aprofunda os
riscos dessa decisão de threshold na prática.
