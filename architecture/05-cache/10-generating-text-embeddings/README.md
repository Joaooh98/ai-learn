# Aula 10 — Gerando embeddings de textos

> Curso: **Cache** · Duração: `06:20`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Depois de apresentar o conceito de embedding (aula 09), esta aula coloca em prática a geração de
embeddings de texto usando um modelo real, via API/SDK do provider escolhido.

## O que a aula deve cobrir

- Chamada a um modelo de embedding, enviando um texto e recebendo o vetor correspondente.
- Formato e dimensão do vetor retornado.
- Geração de embeddings para múltiplos textos, como base para comparação nas próximas aulas.

## Ideia-chave

Gerar o embedding é o primeiro passo prático do cache semântico: sem um vetor confiável
representando cada pergunta, não há como comparar semanticamente uma pergunta nova com as que já
foram cacheadas — tema da aula seguinte.

--- obs: projeto de exemplo esta aqui: architecture/05-cache/mba-ia-cache se for o caso crie uma copia somente para esse modulo sem ter todo o contexto de todas as aulas 