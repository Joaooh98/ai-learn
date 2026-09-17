# Aula 20 — Camadas de cache em aplicações com IA

> Curso: **Cache** · Duração: `05:55`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Com cache exato, cache semântico e suas variações já implementados (aulas 01 a 19), esta aula dá
um passo atrás e organiza tudo em um panorama: uma aplicação com IA pode ter várias camadas de
cache atuando em pontos diferentes do fluxo, não apenas uma.

## Camadas típicas

```text
Aplicação -> cache exato (fingerprint)        -> hit: retorna sem chamar o modelo
          -> cache semântico (embedding)       -> hit: retorna sem chamar o modelo
          -> chamada ao modelo
          -> cache do provider (prompt caching) -> reduz custo/latência mesmo quando o modelo é chamado
```

- **Cache exato**: mais barato de manter, mais restrito (só pega repetição literal/normalizada).
- **Cache semântico**: mais caro de manter (embedding + busca vetorial), mais abrangente (pega
  repetição de significado).
- **Cache do provider**: opera dentro da própria chamada ao modelo, mesmo quando as camadas
  anteriores não resolveram (tema das aulas 21 a 23).

## Ideia-chave

As camadas não são mutuamente exclusivas — o objetivo é que cada requisição passe pela camada mais
barata primeiro, e só chegue às camadas mais caras (chamar o modelo, sem cache algum do provider)
quando realmente necessário.
