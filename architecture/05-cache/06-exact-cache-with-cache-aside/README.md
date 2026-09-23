# Aula 06 — Cache exato com cache-aside

> Curso: **Cache** · Duração: `04:56`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Esta aula implementa, na prática, o padrão cache-aside (aula 02) aplicado ao analisador construído
na aula 04, criando um **cache exato**: a resposta só é reaproveitada quando a entrada é
exatamente igual à que gerou a resposta cacheada anteriormente.

## O que a aula deve cobrir

- Definição de uma chave de cache a partir da entrada (ex.: hash do prompt + parâmetros).
- Consulta ao cache antes de chamar o modelo (hit/miss).
- Gravação da resposta no cache em caso de miss.
- Limite do cache exato: qualquer variação no texto de entrada (mesmo mudanças mínimas, como
  espaços ou reformulações) gera uma chave diferente e, portanto, um miss — problema que motiva o
  fingerprint (aulas 07 e 08) e, mais adiante, o cache semântico.

## Ideia-chave

Cache exato é simples de implementar e de raciocinar sobre, mas só funciona quando a mesma
pergunta é feita literalmente da mesma forma. Ele resolve repetição idêntica, não repetição
semelhante.

---- obs: projeto de exemplo esta aqui: architecture/05-cache/mba-ia-cache se for o caso crie uma copia somente para esse modulo sem ter todo o contexto de todas as aulas 