# Snapshot prático — aula 17

Estado isolado do projeto ao final da aula **Integrando cache semântico no endpoint de
tickets**, reconstruído a partir dos 21 prints da pasta da aula. Ele existe para permitir que
a prática seja executada mais tarde sem depender do projeto consolidado do módulo.

## O que este estado implementa

O endpoint `POST /tickets/analyze` executa esta cascata:

1. cria o fingerprint versionado e tenta o cache exato em memória;
2. no miss exato, gera o embedding, consulta candidatos no pgvector e avalia o melhor pelo
   `semantic_cache_threshold`;
3. em um candidato aceito com `response_json` válido, retorna `source: semantic_cache`;
4. no miss semântico, chama a chain, incrementa `ai_call_number` e salva a análise somente no
   cache exato.

O último limite é essencial para estudar a evolução: este snapshot **ainda não grava** no
pgvector uma resposta recém-gerada pela IA. A gravação automática entra na aula 18. Para
preparar candidatos semânticos aqui, use `POST /semantic-cache/items`.

| Arquivo | Papel |
| --- | --- |
| [main.py](main.py) | Endpoints, chain e cascata exata/semântica |
| [models.py](models.py) | Contratos Pydantic, inclusive `SemanticCacheInfo` |
| [db.py](db.py) | Schema, inserção manual e busca por distância de cosseno |
| [config.py](config.py) | Variáveis de ambiente e configuração alterável em runtime |
| [docker-compose.yml](docker-compose.yml) | PostgreSQL com pgvector |
| [test.http](test.http) | Roteiro manual focado na integração da aula 17 |

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

Antes de iniciar, preencha `OPENAI_API_KEY` no `.env`. O arquivo real fica ignorado pelo Git.
O servidor atende em `http://localhost:8000` e a documentação interativa em `/docs`.

Execute [test.http](test.http) de cima para baixo. Similaridade depende dos embeddings e dos
itens já presentes no volume; por isso um comentário com “pode retornar” descreve uma decisão
que deve ser observada, não um valor garantido.

Para reiniciar o exercício sem remover dados, pare e suba a API. Isso limpa o cache exato e o
contador, mas preserva o pgvector. Para apagar também a base didática desta aula, use
`docker compose down -v` conscientemente.

## Contrato que diferencia este snapshot

`TicketResponse` possui `cache` e `semantic_cache`, como aparece nos prints, e não possui
`semantic_cache_write`. Depois de uma resposta `source: ai_model`, uma repetição idêntica pode
ser `exact_cache`; uma paráfrase ainda depende de um item que tenha sido inserido manualmente.
