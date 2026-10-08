# Aula 18 — Miss semântico e gravação automática no pgvector

> Curso: **Cache** · Duração: `04:26`

## Resultado da aula

O miss semântico passa a alimentar o próprio cache: depois que a IA produz uma análise, o
endpoint mantém o cache exato e insere a resposta no pgvector. Uma mensagem parecida futura
pode então ser resolvida sem nova chamada ao chat.

O [snapshot prático](mba-ia-cache/README.md) representa esse estado isoladamente.

## Proveniência da reconstrução

Esta aula não possui PNGs próprios. O código foi isolado com base em duas evidências locais:

1. o estágio anterior, registrado nos 21 prints e no
   [snapshot da aula 17](../17-integrating-semantic-cache-into-tickets-endpoint/mba-ia-cache/README.md),
   termina sem escrita automática;
2. o [projeto consolidado](../mba-ia-cache/README.md) contém a função de gravação após miss e
   reutiliza o embedding gerado na busca.

Assim, o snapshot 18 conserva toda a aula 17 e acrescenta somente o delta nominal e verificável:
`SemanticCacheWriteInfo`, `save_ai_result_to_semantic_cache()` e sua chamada depois da IA.

## Fluxo completo

```text
exact hit ───────────────────────────────> retorna sem escrever

exact miss → embedding → semantic hit ──> retorna sem escrever
                        │
                        └─ semantic miss → IA → exact CACHE
                                                │
                                                └─ INSERT no pgvector
                                                   com o mesmo embedding
```

Gerar o embedding uma segunda vez aumentaria custo e latência e poderia introduzir uma pequena
variação desnecessária. O vetor consultado e o vetor persistido pertencem à mesma entrada
normalizada e ao mesmo request.

## Resposta observável

| Situação | `source` | `semantic_cache_write.attempted` | `saved` |
| --- | --- | --- | --- |
| Hit exato | `exact_cache` | `false` | `false` |
| Hit semântico | `semantic_cache` | `false` | `false` |
| Miss e `INSERT` bem-sucedido | `ai_model` | `true` | `true` |
| Miss e falha no `INSERT` | `ai_model` | `true` | `false` |

A falha de escrita é tratada depois que o resultado da IA já foi obtido. Por isso a API pode
responder com a análise e `saved: false`; uma repetição imediata ainda pode virar hit exato no
mesmo processo.

## Prática preparada

Siga a preparação do [README do snapshot](mba-ia-cache/README.md) e execute o
[roteiro HTTP](mba-ia-cache/test.http) na ordem. Ele separa o experimento por versões, provoca
a gravação automática e permite examinar o candidato criado por busca e avaliação.

Não é preciso executar agora: ambiente, dependências, `.env.example`, banco e requisições estão
organizados para a retomada após as aulas.

## Exercício

Se a resposta retorna `saved: false`, por que uma repetição idêntica pode ser hit exato antes
de reiniciar a API, mas deixa de encontrar esse resultado após o restart?
