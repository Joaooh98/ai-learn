# Aula 17 — Integrando cache semântico no endpoint de tickets

> Curso: **Cache** · Duração: `10:12`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Esta aula aplica o fluxo descrito na aula 16 em um caso de uso concreto: um endpoint de tickets
(provavelmente o mesmo analisador construído nas aulas 04 a 08, agora tratando tickets de suporte
ou similar), adicionando a camada de cache semântico completa.

## O que a aula deve cobrir

- Geração de embedding para o conteúdo do ticket recebido.
- Consulta ao pgvector por tickets/perguntas semanticamente parecidas já processados.
- Decisão de hit/miss semântico com base no threshold definido (aulas 11 e 15).
- Retorno da resposta cacheada em caso de hit, ou chamada ao modelo em caso de miss.

## Ideia-chave

Esta é a primeira integração ponta a ponta do cache semântico em um caso de uso realista, unindo
tudo que foi construído nas aulas 09 a 16: embedding, pgvector, busca por similaridade e
threshold.
