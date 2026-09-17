# Aula 03 — TTL, resposta stale e invalidação

> Curso: **Cache** · Duração: `03:47`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Guardar uma resposta no cache resolve o problema de repetir trabalho, mas cria um novo problema:
por quanto tempo essa resposta continua válida? A aula cobre os três conceitos que lidam com isso.

## Conceitos

- **TTL (time to live)**: tempo definido para uma entrada do cache continuar válida antes de
  expirar automaticamente.
- **Resposta stale**: dado desatualizado que ainda está sendo servido do cache, seja porque o TTL
  é longo demais, seja porque a fonte mudou antes do TTL expirar.
- **Invalidação**: remover ou forçar a atualização de uma entrada do cache antes do TTL natural,
  normalmente porque algo relevante mudou (novo contexto, nova versão do prompt, dado de origem
  alterado).

## Ideia-chave

TTL curto reduz o risco de resposta stale, mas aumenta miss e custo. TTL longo reduz custo, mas
aumenta o risco de servir informação desatualizada. Definir TTL é sempre um trade-off entre
custo/latência e frescor da resposta — não existe um valor universalmente correto.
