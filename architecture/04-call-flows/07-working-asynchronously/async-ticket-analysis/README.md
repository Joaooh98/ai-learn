# Projeto prático — Async Ticket Analysis

API FastAPI com três fluxos de chamada:

- `POST /tickets/analyze`: síncrono, espera a IA e devolve JSON.
- `POST /tickets/explain`: streaming, devolve texto em partes.
- `POST /tickets/full-analysis`: cria job e responde imediatamente.
- `GET /jobs/{job_id}`: consulta status e resultado do job.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de rodar.

## Fluxo assíncrono

```text
POST /tickets/full-analysis -> {"job_id": "...", "status": "pending"}
BackgroundTasks -> processing -> OpenAI -> completed ou failed
GET /jobs/{job_id} -> status atual e resultado
```

O arquivo `requests.http` usa `# @name createJob` para reaproveitar o `job_id` automaticamente na consulta.

## Nota de produção

O arquivo `app/jobs.py` usa memória local para fins didáticos. Em produção, substitua por banco, Redis, fila real ou worker dedicado.
