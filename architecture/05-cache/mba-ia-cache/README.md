# Analisador de tickets — cache exato e semântico

Exemplo didático com FastAPI, LangChain, OpenAI e PostgreSQL/pgvector. Classifica tickets em
`billing`, `technical_support`, `account`, `cancellation` ou `other` e devolve confiança e motivo.
O objetivo é observar a cascata de cache e seus limites. Veja a [trilha das aulas](../README.md).

## Comportamento implementado

1. Constrói fingerprint com `prompt_version`, `rules_version`, `model_capability` e texto
   normalizado; gera SHA-256 da serialização JSON com chaves ordenadas.
2. Consulta `CACHE`, um dicionário local. Hit retorna `source: exact_cache` e evita embedding,
   PostgreSQL e modelo de chat.
3. No miss exato, gera embedding e busca até cinco candidatos no pgvector, filtrados pelas três
   versões/capacidade. A ordenação usa distância de cosseno `<=>`.
4. Aceita o primeiro candidato se `similarity >= semantic_cache_threshold` e se
   `response_json` puder ser convertido em `TicketAnalysis`. Retorna `source: semantic_cache`.
   Esse caminho **não preenche o cache exato**.
5. No miss semântico, chama a chain, incrementa `ai_call_count`, grava no dicionário exato e tenta
   persistir a análise no PostgreSQL. Reaproveita o embedding já gerado e retorna `source: ai_model`.

`similarity = 1 - distance` representa cosseno neste SQL. Não é probabilidade de acerto. A API
aceita thresholds em `0 < t <= 1`, uma restrição do demo; cosseno, em geral, pode variar de -1 a 1.

| Campo da resposta | O que informa |
|---|---|
| `source` | Origem efetiva da análise |
| `cache.hit` | Hit **exato**; continua falso em hit semântico |
| `semantic_cache` | Tentativa, decisão, threshold e melhor candidato |
| `semantic_cache_write` | Tentativa de escrita após chamada ao chat e seu resultado |
| `ai_call_number` | Contador local de análises de chat concluídas; não contabiliza embeddings ou retries do SDK |
| `elapsed_ms` | Tempo medido dentro do handler; não inclui toda a latência HTTP |

Se a saída do melhor candidato não validar, segue para o modelo; não tenta o segundo candidato.
Validar estrutura também não prova que categoria, confiança e justificativa estão corretas.

## Organização

| Arquivo | Responsabilidade |
|---|---|
| [main.py](main.py) | Endpoints, fingerprint, decisão de cache e chain |
| [db.py](db.py) | Conexão, schema, inserção e busca SQL |
| [models.py](models.py) | Contratos Pydantic de entrada/saída |
| [config.py](config.py) | Ambiente, configuração local e fábricas de modelos |
| [log_helpers.py](log_helpers.py) | Formatação dos logs |
| [test.http](test.http) | Sequência manual de requisições |

LangChain fornece prompt, modelo de chat, saída estruturada e `OpenAIEmbeddings`. A persistência
e a busca usam `psycopg` e SQL próprio; não há vector store LangChain nem classe pronta de cache
semântico. O demo de prompt caching visto nos prints da aula 23 não está implementado aqui.

## Preparar e executar

Execute estes comandos **nesta pasta**, com Python 3.10 ou superior e Docker Compose disponíveis:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de iniciar a aplicação. O exemplo usa
`gpt-4.1-mini`, `text-embedding-3-small` e dimensão padrão 1536. Chamadas ao chat e ao modelo de
embedding podem gerar cobrança; um hit semântico ainda usa embedding.

O servidor atende em `http://localhost:8000`; o contrato interativo fica em
`http://localhost:8000/docs`. O banco usa `pgvector/pgvector:pg16`, com dados no volume
`ai_cache_postgres_data`.

Se a porta 5432 estiver ocupada, ajuste `POSTGRES_HOST_PORT` no `.env` e a porta em
`DATABASE_URL` para o mesmo valor. Esse cliente roda no host; o mapeamento alternativo não muda
a porta interna 5432 do contêiner.

No startup, tenta criar extensão `vector`, tabela `ai_response_cache` e índice B-tree de
fingerprint. A exceção é registrada, mas **não impede a aplicação de iniciar**. Use
`GET /db/status` e confira `connected`, `pgvector_enabled` e `table` antes dos testes.

Para parar o banco mantendo dados: `docker compose down`. Reiniciar o processo da aplicação
limpa dicionário, contador e configuração runtime, mas mantém os itens do PostgreSQL.
`docker compose down -v` também apaga os dados do volume; use apenas se quiser descartar o
banco didático.

## Endpoints

| Método e rota | Uso |
|---|---|
| `GET /config` | Ler configuração do processo |
| `PUT /config` | Atualizar rótulos de versão/capacidade e threshold |
| `GET /db/status` | Diagnóstico de conexão/extensão/tabela |
| `POST /tickets/analyze` | Cascata completa |
| `POST /embeddings/generate` | Gerar vetores e mostrar dimensão/preview |
| `POST /semantic-cache/items` | Inserir item manual com embedding |
| `POST /semantic-cache/search` | Buscar candidatos sem decidir reutilização |
| `POST /semantic-cache/evaluate` | Comparar o primeiro candidato com threshold |

`/config` altera rótulos usados na chave/filtro. **Não troca o prompt, regras implementadas ou
modelo físico**: chain e embeddings são criados no carregamento do módulo. Para mudar
`OPENAI_MODEL`, altere ambiente e reinicie. O versionamento só funciona se o desenvolvedor
atualizar o rótulo quando mudar a implementação correspondente.

A inserção manual recebe JSON livre em `response_json`; uma estrutura incompatível pode ser
persistida e só rejeitada ao tentar servir um hit no endpoint de tickets.

Exemplos de entrada:

```json
{"message": "Quero cancelar meu plano"}
```

```json
{
  "input_text": "Como cancelo minha assinatura?",
  "response_json": {
    "category": "cancellation",
    "confidence": 0.92,
    "reason": "Solicitação de cancelamento de assinatura."
  }
}
```

Para busca, envie `{"input_text": "Preciso cancelar meu plano", "limit": 5}`. Para avaliação,
adicione `"threshold": 0.9`. `limit` deve ser ao menos 1 e é limitado a 10. Avaliação isolada
gera embedding e consulta o banco; não chama o chat nem grava. O endpoint principal já integra
a mesma decisão ao fluxo completo.

## Exercício manual e resultados esperados

Use [test.http](test.http) ou o contrato em `/docs`. Para um experimento isolado sem apagar dados,
use novos rótulos de prompt/regras em `PUT /config`, exclusivos dessa sessão de estudo. Isso
separa os candidatos antigos e as chaves exatas; não cria novos prompts.

| Passo | Requisição | Observação esperada |
|---|---|---|
| 1 | `Quero cancelar meu plano` em escopo sem itens | `ai_model`, seguido de tentativa de gravação |
| 2 | Mesma mensagem no mesmo processo/escopo | `exact_cache` |
| 3 | `Preciso cancelar meu plano` | Candidato semântico; hit depende da similaridade e threshold reais |
| 4 | `Meu aplicativo está travando ao abrir` | Observe rejeição/aceite; não presuma a decisão sem medir |
| 5 | Mudar `rules_version` | Entradas antigas ficam fora da chave/filtro |
| 6 | Reiniciar sem alterar ambiente/versões | Exato fica vazio; dados persistidos podem produzir hit semântico |

`docker compose up -d` não esvazia um volume existente. Os comentários de `test.http` apresentam
um cenário ideal e resultados semânticos esperados, não garantias. Conte embeddings e chat
separadamente ao avaliar custo.

## Limitações confirmadas no código

- Sem TTL, expiração, limite de memória, limpeza física, isolamento por tenant ou autenticação.
  `created_at` é armazenado, mas a busca não filtra idade.
- Sem filtro de modelo/versão do embedding. Dimensão igual não torna dois espaços vetoriais
  compatíveis. Trocar embedding exige separar/migrar os itens e recalibrar o threshold.
- `OPENAI_EMBEDDING_DIMENSIONS` configura tabela/metadados, mas não é passado a
  `OpenAIEmbeddings`. Alterar só esse número pode causar incompatibilidade na gravação.
  `CREATE TABLE IF NOT EXISTS` também não migra a dimensão de uma tabela existente.
- O índice criado é B-tree de metadados, não HNSW/IVFFlat. A busca vetorial não tem índice ANN
  configurado; pgvector faz busca exata por padrão. [Referência pgvector](https://github.com/pgvector/pgvector).
- Falhas de embedding/leitura não têm fallback implementado e podem interromper um miss exato.
  Falha de gravação é capturada: devolve a análise com `saved: false`.
- Estado global é local por processo. Múltiplos workers divergem em cache/contador/config;
  requisições concorrentes podem gerar chamadas e itens duplicados. Não há single-flight.
- O handler de tickets aceita string vazia; não aplica a validação de conteúdo usada nos endpoints
  de embedding/busca. Confiança é `float`, sem restrição Pydantic de 0 a 1.
- Toda resposta concluída pelo chat é candidata à persistência, sem auditoria de qualidade ou
  política de dados. Similaridade e schema não garantem justificativa correta para outro ticket.
- Dependências têm poucos limites de versão e imagem Docker usa tag móvel. Registre versões
  resolvidas ao reproduzir; as aulas mostram snapshots de um ambiente específico.
- A configuração global pode mudar durante uma requisição. O exemplo não garante snapshot
  atômico de configuração para fingerprint, threshold e geração.

Esses limites são oportunidades de evolução do exercício. Para desenhar a política completa,
use os critérios e métricas no [guia do módulo](../README.md).
