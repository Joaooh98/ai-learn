# Aula 09 — O que é um modelo de embedding

> Curso: **Cache** · Duração: `05:25`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Para ir além do cache exato (que só reconhece entradas idênticas), o módulo precisa de uma forma
de medir o **significado** de um texto, não apenas seu conteúdo literal. Esta aula introduz o
conceito de modelo de embedding: um modelo que transforma um texto em um vetor numérico que
representa sua semântica.

## Conceito

```text
texto -> modelo de embedding -> vetor numérico (ex.: [0.12, -0.03, 0.88, ...])
```

Textos com significado parecido tendem a gerar vetores próximos nesse espaço numérico; textos com
significados diferentes tendem a gerar vetores distantes. É essa propriedade — proximidade de
vetor como aproximação de proximidade de significado — que viabiliza o cache semântico.

## Ideia-chave

Um modelo de embedding não gera texto, gera **representação**. É essa representação numérica que
as próximas aulas usam para comparar perguntas diferentes na forma, mas parecidas no significado —
a base do cache semântico.
