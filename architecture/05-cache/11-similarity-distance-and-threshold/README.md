# Aula 11 — Similaridade, distância e threshold

> Curso: **Cache** · Duração: `05:27`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Com embeddings sendo gerados (aula 10), a aula explica como comparar dois vetores para decidir se
os textos que eles representam são "parecidos o suficiente" — a peça que falta antes de implementar
o cache semântico de fato.

## Conceitos

- **Similaridade/distância**: medidas como similaridade de cosseno ou distância euclidiana, usadas
  para comparar dois vetores de embedding e obter um número que indica o quão próximos eles estão.
- **Threshold**: valor de corte que decide, a partir da similaridade/distância calculada, se dois
  textos devem ser tratados como "a mesma pergunta" para fins de cache.

## Fluxo conceitual

```text
embedding(pergunta nova) vs embedding(pergunta cacheada) -> similaridade/distância
  acima do threshold -> tratar como a mesma pergunta (hit semântico)
  abaixo do threshold -> tratar como pergunta diferente (miss semântico)
```

## Ideia-chave

O threshold é o parâmetro mais sensível do cache semântico: threshold muito permissivo gera falsos
positivos (respostas erradas por excesso de confiança na similaridade); threshold muito restritivo
reduz o cache semântico a pouco mais que um cache exato. A aula 15 volta a esse tema aplicado à
prática.
