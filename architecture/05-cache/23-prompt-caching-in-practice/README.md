# Aula 23 — Prompt Caching na prática

> Curso: **Cache** · Duração: `07:06`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Fechando o módulo "Cache", esta aula coloca em prática o prompt caching nativo de um provider
(apresentado conceitualmente na aula 22): estruturar uma chamada para que a parte fixa e repetida
do prompt seja reaproveitada pelo provider entre requisições.

## O que a aula deve cobrir

- Organização do prompt separando o conteúdo fixo e repetido (ex.: instruções, system prompt) do
  conteúdo variável (a pergunta/entrada de cada chamada).
- Ativação/observação do prompt caching na chamada ao modelo escolhido.
- Comparação de custo e/ou latência entre chamadas com e sem reaproveitamento do prefixo cacheado.

## Ideia-chave

Esta aula fecha o módulo mostrando que cache em aplicações com IA acontece em várias camadas
complementares: cache exato e semântico controlados pela aplicação (aulas 01 a 19), e prompt
caching controlado pelo provider (aulas 21 a 23) — cada um reduzindo custo e latência em um ponto
diferente do fluxo.
