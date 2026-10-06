# Aula 14 — Buscando respostas parecidas com pgvector

> Curso: **Cache** · Duração: `08:00`

## Material e foco da aula

Os doze prints mostram `POST /semantic-cache/search`, a consulta SQL e a lista de candidatos.
[05.png](05.png) inicia a função de busca; [08.png](08.png) mostra filtros e ordenação;
[10.png](10.png) e [12.png](12.png) registram o retorno de candidatos.

## Fluxo observado

```text
input_text → fingerprint → embed_query → filtro de compatibilidade
           → ORDER BY distância crescente → LIMIT → candidatos e scores
```

Em [db.py](../mba-ia-cache/db.py), o trecho central da consulta é:

```sql
SELECT
  c.id,
  c.response_json,
  c.embedding <=> q.value AS distance,
  1 - (c.embedding <=> q.value) AS similarity
FROM ai_response_cache c
CROSS JOIN query_embedding q
WHERE c.prompt_version = %s
  AND c.rules_version = %s
  AND c.model_capability = %s
ORDER BY c.embedding <=> q.value
LIMIT %s;
```

O fragmento depende da CTE `query_embedding` definida no código. O vetor e os filtros são
passados como parâmetros, sem concatenar o texto do usuário no SQL.

O operador `<=>` é distância de cosseno. Os resultados têm a menor distância primeiro;
`similarity = 1 - distance` inverte a direção para um score de similaridade.
[Referência: consulta no pgvector](https://github.com/pgvector/pgvector#querying).

## Busca não é decisão de hit

Exemplo de requisição:

```json
{"input_text": "Preciso cancelar meu plano", "limit": 5}
```

`/semantic-cache/search` devolve candidatos e seus metadados, sem aceitar automaticamente
uma resposta. O vizinho mais próximo é apenas o melhor **entre os disponíveis**, e pode ser
inadequado. A aceitação pelo threshold aparece na aula 15.

Em [main.py](../mba-ia-cache/main.py), `run_semantic_search()` rejeita `limit < 1`, limita
o valor a dez e rejeita texto vazio após normalização. Os filtros de versão são iguais à
configuração atual; não incluem igualdade de `normalized_text`, pois a busca admite paráfrases.

## Complemento de estudo: relevância, escopo e escala

A consulta do exemplo usa busca exata de vizinhos, sem índice vetorial aproximado. Para grandes
volumes, HNSW ou IVFFlat são opções de estudo que mudam o equilíbrio entre latência e recall;
não são uma etapa já implementada. [Referência: indexação no pgvector](https://github.com/pgvector/pgvector#indexing).

Filtre tenant, autorização, versões e validade conforme o domínio. Aproximação vetorial não
substitui esses critérios. O conjunto de candidatos precisa ser elegível antes da resposta
ser utilizada.

## Exercício

Uma tabela tem somente perguntas sobre cobrança. Qual candidato a busca pode retornar para
“Quero cancelar uma reunião”? Por que `LIMIT 1` não prova que a resposta seja reutilizável?
