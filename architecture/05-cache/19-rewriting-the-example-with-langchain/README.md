# Aula 19 — Refazendo exemplo utilizando LangChain

> Curso: **Cache** · Duração: `12:16`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Depois de implementar o cache semântico "na mão" (geração de embedding, gravação e busca no
pgvector, decisão de threshold — aulas 09 a 18), esta aula refaz o mesmo exemplo usando LangChain,
mostrando como o framework abstrai boa parte dessas peças (geração de embeddings, integração com
vector store, busca por similaridade).

## O que a aula deve cobrir

- Configuração do componente de embeddings do LangChain.
- Configuração do vector store do LangChain apontando para o mesmo pgvector usado nas aulas
  anteriores.
- Reimplementação da busca por similaridade e do fluxo de hit/miss semântico usando as abstrações
  do framework.
- Comparação entre a implementação manual e a versão com LangChain: o que se ganha em produtividade
  e o que se perde em controle explícito sobre cada etapa.

## Ideia-chave

Ter implementado o fluxo manualmente antes (aulas 09 a 18) é o que torna esta aula útil: dá para
entender exatamente o que o LangChain está abstraindo, em vez de tratar o framework como uma caixa
preta.
