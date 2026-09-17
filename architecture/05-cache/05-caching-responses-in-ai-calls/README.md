# Aula 05 — Cache de resposta em chamadas de IA

> Curso: **Cache** · Duração: `03:57`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo, a partir do analisador sem cache construído na aula anterior
([`04-analyzer-without-cache`](../04-analyzer-without-cache/README.md)). Quando os prints forem
adicionados, este README pode ser ajustado para refletir o fluxo exato da aula.

## Resumo

Com a linha de base sem cache pronta, a aula introduz a ideia central que guia o restante do
módulo: cachear diretamente a **resposta** de uma chamada de IA, associando-a à entrada que a
gerou (o prompt e seus parâmetros), para reaproveitá-la em chamadas futuras equivalentes.

## Conceito

```text
entrada (prompt + parâmetros) -> chave de cache -> resposta do modelo
```

Da próxima vez que a mesma entrada aparecer, a aplicação consulta o cache pela chave antes de
chamar o modelo novamente.

## Ideia-chave

Cachear resposta de IA é, na essência, o mesmo padrão hit/miss/cache-aside da aula 02 — a
diferença é a natureza da "fonte": em vez de uma consulta a banco, é uma chamada cara e variável a
um modelo. As próximas duas aulas (06 e 07) tornam esse conceito concreto: como montar a chave de
cache e como implementar isso na prática.
