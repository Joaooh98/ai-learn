# Aula 09 — O que é um modelo de embedding

> Curso: **Cache** · Duração: `05:25`

## Material e foco da aula

Os seis prints passam do cache exato ao semântico e apresentam o vetor como representação de
texto. [02.png](02.png) diferencia embedding de chat; [03.png](03.png) compara proximidade de
significado; [04.png](04.png) lembra que a decisão de reutilizar depende de limiar e contexto.

## Conceito

```text
texto → modelo de embedding → vetor numérico
"Como cancelo minha assinatura?" → [0.12, -0.03, 0.88, ...]
```

Os números acima são ilustrativos. Cada dimensão integra uma representação aprendida; não
é adequado interpretar uma posição isolada como “cancelamento” ou “cobrança”.

Um modelo de embedding produz representação, enquanto o modelo de chat produz a análise.
Textos relacionados podem ficar próximos no espaço vetorial, mas essa proximidade é uma
**aproximação** da relação entre textos, não uma prova de igualdade ou de resposta intercambiável.
[Referência: guia oficial de embeddings](https://developers.openai.com/api/docs/guides/embeddings).

## Complemento de estudo: representação e equivalência

No projeto, mensagens são normalizadas e enviadas a `OpenAIEmbeddings`, com
`text-embedding-3-small` como padrão. A análise de tickets usa outro modelo. Veja
[config.py](../mba-ia-cache/config.py) e [main.py](../mba-ia-cache/main.py).

| Par de entradas | O que precisa ser verificado |
| --- | --- |
| “Quero cancelar meu plano” / “Preciso encerrar minha assinatura” | Mesmo produto e política; análise completa reutilizável |
| “Quero cancelar” / “Não quero cancelar” | Negação muda a intenção |
| “Cobrança de R$ 10” / “Cobrança de R$ 100” | Valor pode afetar motivo e ação |
| Mesma pergunta de dois clientes | Escopo e dados podem exigir respostas diferentes |

Embeddings podem aproximar textos do mesmo tema, mesmo quando números, negações, entidades
ou condições exigem outra resposta. Não descarte esses detalhes na preparação da entrada.

## Compatibilidade dos vetores

Compare vetores do mesmo espaço: modelo, revisão, dimensão e preparação compatíveis.
Dois modelos podem produzir vetores do mesmo tamanho com coordenadas sem relação entre si.
Trocar o modelo exige uma estratégia de reindexação e separação de versões, além de recalibrar
o threshold.

Dimensão maior não assegura melhor cache. Avalie recuperação e falsos hits com o conjunto de
tickets do domínio. A dimensão também afeta armazenamento e trabalho de busca.

## Pergunta de revisão

Por que duas mensagens sobre cancelamento podem ter embedding próximo e, ainda assim,
não permitir reutilizar a mesma análise?
