# Projeto prático — Streaming Ticket Explanation

API FastAPI com dois fluxos para comparar a experiência:

- `POST /tickets/analyze`: chamada síncrona que devolve JSON completo.
- `POST /tickets/explain`: chamada com streaming que devolve texto em partes.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de rodar.

## Teste do streaming

```bash
curl -N -w "\nTempo total: %{time_total}s\n" \
  -X POST http://127.0.0.1:8000/tickets/explain \
  -H "Content-Type: application/json" \
  -d '{"message": "Fui cobrado duas vezes e preciso de ajuda com meu pagamento."}'
```

Use `-N` para o curl mostrar os chunks sem esperar bufferizar a resposta completa.
