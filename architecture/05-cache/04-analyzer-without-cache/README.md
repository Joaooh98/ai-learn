# Aula 04 — Analisador sem cache

> Curso: **Cache** · Duração: `07:11`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Depois da parte conceitual (aulas 01 a 03), o módulo inicia a prática construindo um analisador —
um endpoint ou serviço que chama um modelo de IA para processar uma entrada — **sem nenhum
cache**. Essa versão serve como linha de base: é contra ela que as próximas aulas vão medir o
ganho de cada camada de cache adicionada (exato, semântico, prompt caching do provider).

## O que a aula deve cobrir

- Implementação de um caso de uso simples que chama um modelo a cada requisição.
- Observação de latência e custo repetidos mesmo quando a mesma pergunta (ou uma pergunta muito
  parecida) é feita mais de uma vez.
- Ausência proposital de qualquer camada de cache, para deixar o problema visível antes de
  resolvê-lo.

## Ideia-chave

Construir o analisador sem cache primeiro é o que torna o ganho das próximas aulas mensurável:
sem uma baseline clara, fica difícil justificar a complexidade que cache-aside, fingerprint e
cache semântico vão adicionar ao sistema.


---- obs: projeto de exemplo esta aqui: architecture/05-cache/mba-ia-cache se for o caso crie uma copia somente para esse modulo sem ter todo o contexto de todas as aulas 