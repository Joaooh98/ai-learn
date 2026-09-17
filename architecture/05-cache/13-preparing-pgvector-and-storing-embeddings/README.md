# Aula 13 — Preparando pgvector e salvando embeddings

> Curso: **Cache** · Duração: `08:12`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Com o conceito de cache semântico esclarecido (aula 12), a aula inicia a implementação prática
configurando o pgvector (extensão do PostgreSQL para armazenar e consultar vetores) e salvando os
embeddings gerados a partir das perguntas processadas.

## O que a aula deve cobrir

- Habilitação da extensão `pgvector` no PostgreSQL.
- Criação de uma tabela para armazenar pergunta, resposta e o vetor de embedding correspondente.
- Gravação dos embeddings gerados (aula 10) nessa tabela.

## Ideia-chave

Esta aula monta a infraestrutura de armazenamento necessária para o cache semântico funcionar: sem
um lugar para guardar e consultar vetores de forma eficiente, a comparação de similaridade da aula
11 não escala além de comparar tudo em memória. A próxima aula usa essa base para buscar respostas
parecidas.
