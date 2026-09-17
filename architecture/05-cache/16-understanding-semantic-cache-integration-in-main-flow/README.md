# Aula 16 — Entendendo a integração do cache semântico no fluxo principal

> Curso: **Cache** · Duração: `04:02`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Antes de integrar o cache semântico a um endpoint real (aula 17), esta aula posiciona
conceitualmente onde essa camada entra no fluxo principal da aplicação — para deixar claro o que
acontece antes e depois da chamada ao modelo.

## Fluxo conceitual

```text
Requisição -> gera embedding da entrada
           -> busca no pgvector por resposta parecida (aulas 14 e 15)
                hit semântico  -> retorna resposta cacheada, sem chamar o modelo
                miss semântico -> chama o modelo -> grava pergunta + resposta + embedding
           -> resposta ao cliente
```

## Ideia-chave

O cache semântico entra como um passo adicional **antes** da chamada ao modelo, não depois. Ele
intercepta a requisição, decide se responde do cache ou deixa o fluxo seguir normalmente — decisão
que precisa ser rápida o suficiente para não anular o ganho de latência que o cache deveria trazer.
