# Aula 11 — Similaridade, distância e threshold

> Curso: **Cache** · Duração: `05:27`

## Material e foco da aula

Os cinco prints distinguem proximidade vetorial, score e corte de decisão.
[02.png](02.png) contrasta distância e similaridade; [04.png](04.png) coloca a decisão na
aplicação. As escalas e os thresholds dos desenhos são exemplos didáticos.

## Direção da comparação

| Medida | Interpretação | Regra típica de aceitação |
| --- | --- | --- |
| Similaridade de cosseno | Maior valor: direções mais próximas | `similaridade >= limiar` |
| Distância de cosseno | Menor valor: direções mais próximas | `distância <= limite` |
| Distância euclidiana (L2) | Menor valor: vetores mais próximos | `distância <= limite` |

Não aplique “acima do threshold = hit” a toda métrica. A direção depende do significado do score.

Para vetores não nulos `u` e `v`:

```text
similaridade_cosseno(u,v) = (u · v) / (||u|| × ||v||)
distância_cosseno(u,v)    = 1 - similaridade_cosseno(u,v)
```

A similaridade de cosseno pode variar de -1 a 1; a distância correspondente, de 0 a 2.
Nem toda API expõe essa escala diretamente. Produto interno e L2 também não compartilham
um threshold universal com o cosseno.

## O que o projeto usa

Em [db.py](../mba-ia-cache/db.py), `<=>` calcula distância de cosseno e
`1 - (embedding <=> query)` calcula a similaridade. A consulta ordena por distância crescente.
Esses operadores estão documentados no [pgvector](https://github.com/pgvector/pgvector#querying).

`evaluate_best_match()` em [main.py](../mba-ia-cache/main.py) aceita o primeiro candidato se
`best_match.similarity >= threshold`. Assim, com limiar ilustrativo de 0,90:

```text
distância = 0,08 → similaridade = 0,92 → candidato aceito pelo score
distância = 0,15 → similaridade = 0,85 → candidato rejeitado
```

## Complemento de estudo: o score não é probabilidade

Similaridade de 0,92 não significa 92% de chance de a resposta estar correta. Ela descreve a
relação geométrica dos vetores. Correção depende também de contexto, escopo, contrato, frescor
e qualidade da resposta armazenada.

Vetores normalizados podem produzir ordenações relacionadas para cosseno, produto interno e
L2, mas valores de corte ainda exigem a transformação correspondente. Trocar métrica ou modelo
sem recalibrar muda a política de aceitação.

O código restringe o threshold a `0 < threshold <= 1`; essa é uma escolha do exemplo, não
a definição completa da escala do cosseno.

## Exercício

Para limiar de similaridade 0,90, qual é o limite equivalente de distância de cosseno?
Por que o mesmo número não pode ser usado diretamente como limite de distância L2?

---

> Complemento revisado em 19/11/2026. Exemplos propostos não são medições da aula.

## Aprofundamento: calibrar pela consequência da reutilização

Os cinco prints vão de vetores à decisão da aplicação. Os cortes 0,70, 0,90 e 0,82 que
aparecem nos desenhos pertencem a exemplos diferentes; não constituem uma tabela de thresholds
intercambiáveis. O HNSW desenhado também não demonstra que esse índice esteja criado no projeto.

### Dataset de pares proposto

Monte pares com rótulo `pode_reutilizar`: paráfrases realmente equivalentes, negações, mudança
de plano, versão de política e tenant. Calibre o limiar no conjunto de validação e confira
em um conjunto separado quantas reutilizações eram erradas. Inclua pares semanticamente
próximos que precisam de respostas diferentes, como cancelar um plano e cancelar uma reunião.

Aplique o escopo de acesso e a validade antes de aceitar qualquer candidato. Para respostas
com efeitos externos, reusar texto não deve reexecutar a ação anterior. Se o resultado
contiver informação individual, proximidade semântica não permite compartilhá-lo com outro usuário.

Reporte taxa de hits aceitos, erro entre os hits, custo total do lookup e validade da resposta.
Uma política de cache que evita muitas gerações mas aumenta respostas incorretas pode piorar
custo por resultado útil. Dimensão, modelo de embedding, métrica e versão dos dados devem
acompanhar cada calibração.
