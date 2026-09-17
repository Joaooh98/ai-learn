# Aula 15 — Threshold e falso positivo no cache semântico

> Curso: **Cache** · Duração: `07:04`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Com a busca por similaridade funcionando (aula 14), esta aula aprofunda o risco central do cache
semântico: o falso positivo — quando o sistema trata duas perguntas como equivalentes (porque a
similaridade ficou acima do threshold) mas elas, na verdade, esperam respostas diferentes.

## O risco do falso positivo

```text
Pergunta A: "Como cancelo meu pedido?"
Pergunta B: "Como cancelo minha assinatura?"
```

Essas perguntas podem gerar embeddings próximos (mesmo campo semântico: "cancelar algo"), mas a
resposta correta é diferente para cada uma. Um threshold mal calibrado pode fazer o cache retornar
a resposta errada com alta confiança.

## Como mitigar

- Calibrar o threshold com casos reais, não apenas teoricamente.
- Considerar contexto adicional além do texto puro (ex.: categoria, entidade envolvida) na
  composição do embedding ou na validação do hit.
- Monitorar hits semânticos incorretos como uma métrica de qualidade do cache, não só a taxa de
  hit.

## Ideia-chave

Cache semântico troca a rigidez do cache exato por um risco novo: acertar demais, na direção
errada. Escolher o threshold é balancear economia de chamadas (menos miss) contra risco de
resposta incorreta (menos falso positivo).
