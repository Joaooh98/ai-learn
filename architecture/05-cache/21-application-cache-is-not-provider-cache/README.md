# Aula 21 — Cache da aplicação não é cache do provider

> Curso: **Cache** · Duração: `06:11`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Depois de mapear as camadas de cache (aula 20), esta aula separa claramente dois níveis que
costumam ser confundidos: o cache que a própria aplicação implementa (exato ou semântico) e o
cache que o provider de IA oferece nativamente dentro da chamada ao modelo (prompt caching).

## A diferença

- **Cache da aplicação**: decide se chama o modelo ou não. Vive fora da chamada — antes dela. É o
  que foi construído nas aulas 01 a 20 (fingerprint, pgvector, embeddings, threshold).
- **Cache do provider (prompt caching)**: o modelo é sempre chamado, mas o provider reaproveita
  internamente partes já processadas do prompt (ex.: um system prompt longo e repetido), reduzindo
  custo e latência **dentro** da própria chamada.

```text
Cache da aplicação:  decide SE chama o modelo
Cache do provider:   otimiza COMO o modelo processa a chamada, quando ela acontece
```

## Ideia-chave

Os dois níveis resolvem problemas diferentes e não competem entre si: uma aplicação bem otimizada
usa cache próprio para evitar chamadas desnecessárias, e ainda se beneficia do prompt caching do
provider nas chamadas que de fato precisam acontecer. As próximas duas aulas aprofundam o prompt
caching dos providers.
