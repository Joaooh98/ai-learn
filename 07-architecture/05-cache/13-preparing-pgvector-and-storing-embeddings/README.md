# Aula 13 — Preparando pgvector e salvando embeddings

> Curso: **Cache** · Duração: `08:12`

## Material e foco da aula

Os 27 prints mostram PostgreSQL com pgvector, inicialização da tabela e inserção de entradas.
[17.png](17.png) registra o schema e o índice; [22.png](22.png) mostra Docker Compose;
[27.png](27.png) mostra a entrada criada pelo endpoint.

## Estrutura observada

O [Docker Compose](../mba-ia-cache/docker-compose.yml) usa a imagem `pgvector/pgvector:pg16`.
`init_db()` de [db.py](../mba-ia-cache/db.py) habilita a extensão SQL **`vector`**, cria a
tabela `ai_response_cache` e o índice de fingerprint.

| Campo | Papel |
| --- | --- |
| `id` | UUID da entrada |
| `prompt_version`, `rules_version`, `model_capability` | Compatibilidade do contrato declarado |
| `input_text`, `normalized_text` | Entrada original e representação usada no embedding |
| `response_json` | Resposta armazenada como JSONB |
| `embedding` | Vetor com a dimensão configurada |
| `created_at` | Data de criação, sem política de expiração associada |

Trecho representativo da inicialização, com dimensão padrão:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
-- Na tabela ai_response_cache:
-- response_json JSONB NOT NULL
-- embedding VECTOR(1536)
```

A extensão e o tipo estão descritos no [pgvector](https://github.com/pgvector/pgvector#getting-started).
O nome do projeto é pgvector; o comando SQL habilita `vector`.

## Inserção manual

`POST /semantic-cache/items` recebe `input_text` e `response_json`, constrói o fingerprint,
gera embedding completo e persiste a entrada. Exemplo:

```json
{
  "input_text": "Como cancelo minha assinatura?",
  "response_json": {
    "category": "cancellation",
    "confidence": 0.92,
    "reason": "O usuário solicita cancelamento da assinatura."
  }
}
```

Esse endpoint aceita um dicionário genérico: não valida antecipadamente toda a resposta como
`TicketAnalysis`. O fluxo de análise valida o candidato antes de servi-lo.

## Complemento de estudo: preparar persistência

O índice criado é **B-tree sobre metadados**, não HNSW ou IVFFlat. A existência do índice não
significa que a busca vetorial aproximada está habilitada. O SQL atual realiza busca vetorial
sem índice aproximado.

`CREATE TABLE IF NOT EXISTS` não migra schema existente. Mudar a dimensão configurada não
altera uma coluna criada anteriormente; a geração também precisa usar dimensão compatível.
O modelo de embedding não é armazenado como coluna, e versões de modelos não são filtradas
diretamente. Esses pontos exigem plano de migração se o modelo mudar.

Há persistência em volume, mas não TTL, deduplicação, política de retenção ou isolamento por
cliente. Guarde escopo em campos estruturados e aplique autorização nas leituras. PostgreSQL
também oferece políticas por linha para cenários de isolamento. [Referência: Row Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

## Exercício

Explique por que trocar a variável de dimensão e reiniciar a API não migra os embeddings
existentes. Quais informações seriam necessárias para manter dois modelos sem misturar vetores?
