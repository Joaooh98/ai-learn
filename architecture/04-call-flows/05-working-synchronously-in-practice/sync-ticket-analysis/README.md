# Projeto prático — Sync Ticket Analysis

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

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

## Contrato e verificação local

Rode cada projeto na própria pasta; todos expõem `127.0.0.1:8000`, então use um de cada vez. Depois de iniciar, os contratos estão em `http://127.0.0.1:8000/docs` e os exemplos de requisições em [requests.http](requests.http).

O modelo padrão do código é `gpt-4.1-mini`, substituível por `OPENAI_MODEL`. Se mudar o modelo, confira suporte a Chat Completions e ao JSON mode usado na análise. As dependências não estão fixadas; registre versões para reproduzir um resultado.

`POST /tickets/analyze` responde somente depois da análise completa. `message=""` gera 422; entrada contendo apenas espaços ainda passa em `min_length=1`. `category` e `priority` são strings, sem validação de enum. Erros do provider ou de parse/schema são tratados genericamente com 500. Veja os [limites verificados no código](../../README.md#limites-verificados-no-código).
