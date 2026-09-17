# Proxy Technical Fallback

> Origem: aula 17 — Fallback tecnico.

Este projeto registra o fallback configurado no LiteLLM Proxy. A aplicacao chama apenas `developer-assistant`; se essa capacidade falhar, o proxy tenta `developer-assistant-backup`.

## Fluxo

```text
Aplicacao -> developer-assistant -> falha -> developer-assistant-backup
```

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

## Observacao

Fallback tecnico aumenta disponibilidade, mas nao garante resposta equivalente. O backup pode ter outro estilo, outra qualidade e outro comportamento.
