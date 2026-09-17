# Aula 07 — Fingerprint de prompt e contexto

> Curso: **Cache** · Duração: `04:44`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

O cache exato da aula 06 usa a entrada bruta como chave, o que é frágil: parâmetros extras,
ordem diferente de campos ou pequenas variações de formatação quebram o hit mesmo quando a
pergunta é, na prática, a mesma. Esta aula introduz o conceito de **fingerprint**: uma chave de
cache derivada de forma controlada do prompt e do contexto relevante, normalizando o que não deve
afetar o resultado.

## Conceito

```text
prompt + contexto + parâmetros relevantes -> normalização -> hash -> fingerprint (chave de cache)
```

Pontos que costumam entrar na normalização antes de gerar o fingerprint:

- Texto do prompt (normalizado: espaços, caixa, pontuação irrelevante).
- Parâmetros que mudam o resultado (modelo, temperatura, system prompt).
- Contexto adicional relevante (ex.: dados injetados no prompt), quando ele afeta a resposta.

## Ideia-chave

Fingerprint continua sendo cache **exato** — só que exato sobre uma versão normalizada da entrada,
não sobre o texto bruto. Isso aumenta a taxa de hit sem introduzir o risco de falso positivo que
o cache semântico (aulas 09 em diante) vai trazer.
