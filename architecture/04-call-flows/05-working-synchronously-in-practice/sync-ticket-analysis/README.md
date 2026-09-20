# Projeto prático — Sync Ticket Analysis

API FastAPI que demonstra uma chamada síncrona para IA. A request só termina depois que a OpenAI devolve a resposta completa em JSON.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de rodar.

## Endpoints

- `POST /tickets/analyze`: classifica um ticket e devolve `category`, `priority` e `summary`.

## Fluxo

```text
request -> FastAPI -> OpenAI -> JSON completo -> validação Pydantic -> response
```

Use `requests.http` para testar pelo REST Client do VS Code.
