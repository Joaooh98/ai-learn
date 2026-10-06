# Aula 15 — Threshold e falso positivo no cache semântico

> Curso: **Cache** · Duração: `07:04`

## Material e foco da aula

Os doze prints implementam `POST /semantic-cache/evaluate` e comparam cortes de decisão.
[03.png](03.png) mostra a avaliação do melhor candidato. Nos [prints 10](10.png) e
[12](12.png), “Quero cancelar minha reunião de amanhã” é rejeitado com limiar 0,90 e aceito
com 0,60, apesar de o candidato tratar de plano/assinatura. O score exibido é cerca de 0,66.

## O risco demonstrado

```text
candidato: "Quero cancelar meu plano" → análise de cancelamento de assinatura
consulta:  "Quero cancelar minha reunião de amanhã" → outra entidade/intenção
```

Termos próximos podem levar a reutilização indevida. Reduzir o corte aumenta aceitação, mas
não transforma essas intenções em equivalentes. O score observado nos prints não é uma
constante reproduzível para qualquer modelo ou conjunto de entradas.

Em [main.py](../mba-ia-cache/main.py), `evaluate_best_match()` rejeita lista vazia e compara
apenas o primeiro candidato com `similarity >= threshold`. O endpoint de avaliação valida
`0 < threshold <= 1` e usa o corte enviado; o endpoint de tickets usa o corte de `runtime_config`.
Avaliar com outro limiar não altera automaticamente a configuração do classificador.

## Complemento de estudo: calibrar com exemplos rotulados

Monte pares do domínio e rotule se **a resposta armazenada completa** serviria para a consulta:

- Paráfrases válidas, incluindo variação de idioma ou estilo quando suportadas.
- Mesmo assunto, mas entidade, valor, prazo ou produto diferente.
- Negações e mudanças de intenção.
- Mesmo texto com outro cliente, outra permissão ou outra versão de regra.
- Casos em que a categoria coincide, mas o motivo cacheado fica errado.

Separe dados de calibração e validação. Varie o threshold no conjunto de calibração e confira
o resultado em entradas não usadas na escolha. Refaça a avaliação ao trocar modelo de embedding,
normalização, contrato ou composição da base.

| Decisão | Resposta era reutilizável | Resposta não era reutilizável |
| --- | --- | --- |
| Aceitar | Hit correto | Falso positivo: resposta indevida |
| Rejeitar | Falso negativo: economia perdida | Rejeição correta |

Métricas úteis: precisão dos hits (`hits corretos / hits aceitos`), recall das oportunidades
(`hits corretos / casos reutilizáveis`), custo evitado e latência. Declare também o denominador
de “taxa de falso positivo”: entre negativos e entre hits aceitos são medidas distintas.

## Além do threshold

Exija escopo e validade; compare atributos críticos; considere rejeitar casos ambíguos e
revisar amostras de hits. Nenhum limiar sozinho garante ausência de falso positivo.
Similaridade não é probabilidade de acerto. A métrica do projeto é cosseno, como documentado
nos [operadores do pgvector](https://github.com/pgvector/pgvector#querying).

## Pergunta de revisão

Para triagem de tickets, o custo de uma inferência extra é maior ou menor que encaminhar um
pedido ao time errado com justificativa incorreta? Como isso orienta a escolha do corte?
