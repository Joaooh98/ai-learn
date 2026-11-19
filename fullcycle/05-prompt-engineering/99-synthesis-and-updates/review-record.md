# Evidências da revisão de Prompt Engineering

Data: **19/11/2026**. Escopo: documentação de estudo, sem execução remota de modelos,
publicação de prompts ou alteração das dependências e scripts didáticos.

## Material visual lido integralmente

| Imagem | Observação | Nota enriquecida |
|---|---|---|
| `precision/img/precision.png` | 20 logs, 10 bugs reais, TP=8 e FP=5 | `precision/precision.md` |
| `recall/img/image.png` | 7 acertos e 3 perdas | `recall/recall.md` |
| `f1/img/image.png` | Fórmula e exemplo P=0,61/R=0,7 | `f1/f1.md` |
| `pairwise-vsevaluation/img/image-1.png` | Preferência entre respostas e summary evaluator | `pairwise-vsevaluation/pairwise-evaluator-vs-evaluation.md` |
| `pairwise-vsevaluation/img/image-2.png` | Continuação do mesmo quadro | Mesma nota |
| `pratic/three-types-prompts/img/one.png` | Dataset com expected_findings e metadados | `pratic/three-types-prompts/three-types-prompts.md` |
| `pratic/calc-metrics/img/image.png` | Placar de precision, recall e F1 | `pratic/calc-metrics/calc-metrics-2.md` |

Os caminhos da tabela são relativos a
`../mba-ia-prompt-engineering/my-summary/comparative-evaluation/`.
As outras quatro notas desse conjunto também receberam complemento contextual.

## Código usado para conferir as explicações

- `7-evaluation/2-precision/metrics.py`: acumulação de TP/FP/FN e matching `(type, severity)`.
- `7-evaluation/shared/parsers.py`: fallback para `{}` quando o parsing falha.
- `7-evaluation/3-pairwise/pairwise_helpers.py`: escolha por presença de letras.
- `7-evaluation/3-pairwise/run.py`: obtenção dos prompts e comparação de experimentos.
- `6-prompt-enriquecido/1-ITER_RETGEN.py`: preenchimento iterativo por LLM sem retriever externo.
- `6-prompt-enriquecido/2-query-enrichment.py`: esclarecimento de campos do PR.

Os caminhos acima partem de `../mba-ia-prompt-engineering/`.
Essa inspeção não equivale a auditoria de todos os scripts do curso.

## Limites e próximos aprofundamentos

Os prints sustentam os resultados exibidos, sem provar disponibilidade atual do modelo,
replicabilidade do run ou adequação para produção. Os links oficiais sustentam os complementos
atuais; recomendações de desenho foram identificadas como aplicação ao caso local.

A revisão principal cobre integralmente as dez notas e sete imagens do conjunto comparativo.
Os capítulos de tipos de prompts, agentes e registry receberam orientação na síntese, mas
seus arquivos executáveis e instruções de agentes não foram reescritos nem integralmente auditados.
