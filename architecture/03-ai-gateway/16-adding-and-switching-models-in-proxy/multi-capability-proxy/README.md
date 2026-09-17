# Multi Capability Proxy

> Origem: aula 16 — Adicionando e alternando modelos no Proxy.

Este projeto registra a evolução do exemplo das aulas 14 e 15: a aplicação passa a escolher uma capacidade interna via `AI_GATEWAY_MODEL`, enquanto o LiteLLM Proxy decide qual provider/modelo real usar.

## Capacidades

- `developer-assistant`: capacidade principal com OpenAI.
- `architecture-advisor`: capacidade alternativa com Anthropic.

## Como executar

```bash
cp .env.example .env
docker compose up
```

Em outro terminal:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Para alternar a capacidade, altere `AI_GATEWAY_MODEL` no `.env`:

```env
AI_GATEWAY_MODEL=architecture-advisor
```

## Ideia da aula

A aplicação não alterna entre SDKs, providers ou modelos físicos. Ela alterna entre nomes internos publicados pelo gateway.
