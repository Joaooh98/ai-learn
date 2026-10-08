# Snapshot prático — aula 18

Estado isolado do projeto ao final da aula **Miss semântico e gravação automática no
pgvector**. Esta pasta não possui prints próprios; o snapshot foi reconstruído a partir do
[projeto consolidado](../../mba-ia-cache/README.md) e do delta inequívoco descrito pelo título
da aula em relação ao [snapshot 17](../../17-integrating-semantic-cache-into-tickets-endpoint/mba-ia-cache/README.md).

## Alteração introduzida nesta aula

Até a aula 17, um miss semântico chamava o modelo e preenchia somente o dicionário de cache
exato. Agora, após uma inferência bem-sucedida, o fluxo também insere a análise no pgvector:

```text
miss exato
   → gera embedding e busca candidatos
   → miss semântico
   → chama a IA
   → salva no cache exato
   → reutiliza o mesmo embedding no INSERT do cache semântico
```

Não há uma segunda geração de embedding para a escrita. O vetor já calculado em
`search_candidates()` chega a `save_ai_result_to_semantic_cache()`.

`TicketResponse` passa a incluir `semantic_cache_write`:

| Campo | Significado |
| --- | --- |
| `attempted` | O fluxo tentou persistir uma resposta nova |
| `saved` | O `INSERT` terminou com sucesso |
| `reason` | Motivo do estado apresentado |
| `item_id` | UUID criado no pgvector, quando salvo |
| `embedding_dimension` | Dimensão do vetor reaproveitado |

Hits exatos e semânticos retornam `attempted: false`, pois já existe uma resposta reutilizável.
Se o chat funcionar e a escrita falhar, a análise ainda é devolvida e o cache exato permanece
preenchido; nesse caso, `saved` será `false`.

## Preparação para executar depois

Na pasta deste snapshot:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes da execução. O arquivo real está ignorado pelo Git.
O servidor atende em `http://localhost:8000`, com o contrato em `/docs`.

O [roteiro HTTP](test.http) cria um escopo de versões específico da aula, provoca o primeiro
miss e depois consulta a paráfrase. Execute os blocos na ordem. O hit semântico depende do
score produzido pelo modelo de embeddings; consulte `/semantic-cache/search` para interpretar
o valor real antes de alterar o threshold.

## Arquivos principais

| Arquivo | Papel |
| --- | --- |
| [main.py](main.py) | Cascata e gravação automática após o miss |
| [models.py](models.py) | Inclui `SemanticCacheWriteInfo` no contrato de resposta |
| [db.py](db.py) | `INSERT` e busca no PostgreSQL/pgvector |
| [config.py](config.py) | Modelos, versões e threshold |
| [docker-compose.yml](docker-compose.yml) | Banco isolado para a aula 18 |
| [test.http](test.http) | Sequência manual que demonstra o novo comportamento |

## Limites deste estado

- A memória e o PostgreSQL não formam uma transação única.
- UUIDs novos e ausência de unicidade permitem duplicatas em misses concorrentes.
- Não há TTL, limpeza, autenticação, isolamento por tenant ou mecanismo single-flight.
- A captura de erro cobre o `INSERT`; falhas na geração do embedding, na leitura ou no chat
  continuam encerrando a requisição.

Este snapshot preserva a implementação da etapa e não antecipa a reescrita citada na aula 19.
