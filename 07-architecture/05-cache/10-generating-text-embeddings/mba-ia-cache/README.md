# Snapshot prático — aula 10

Estado isolado do projeto ao final da aula **Gerando embeddings de textos**, reconstruído a
partir dos 23 prints da aula. Ele conserva o cache exato das aulas anteriores e acrescenta
somente a configuração de `OpenAIEmbeddings` e `POST /embeddings/generate`.

## O que existe neste estágio

- Classificação de tickets com saída estruturada.
- Cache exato em memória, baseado em fingerprint versionado e SHA-256.
- `GET /config` e `PUT /config` para os rótulos usados no fingerprint.
- Geração em lote com `embed_documents`, normalização, dimensão e prévia de cinco valores.

Ainda não existem PostgreSQL, pgvector, persistência nem busca semântica neste snapshot.

## Preparação para executar depois

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Antes da execução, preencha `OPENAI_API_KEY` no `.env`. As requisições de
[test.http](test.http) chamam modelos externos e só devem ser disparadas quando você quiser
realizar o exercício. O servidor ficará em `http://localhost:8000`.

## Arquivos centrais

- [main.py](main.py): cache exato, classificador e endpoint de embeddings.
- [config.py](config.py): modelos e configuração por ambiente.
- [models.py](models.py): contratos Pydantic.
- [test.http](test.http): sequência manual mostrada na aula.
