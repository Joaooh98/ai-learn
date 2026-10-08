# AI Gateway Practical Project

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

Esta pasta concentra os prompts e artefatos do projeto prático da trilha **AI Gateways**.

## Prompts

| # | Arquivo | Origem |
|---|---------|--------|
| 01 | [calling-openai-with-sdk.md](calling-openai-with-sdk.md) | Aula 02 — Chamando OpenAI com SDK |

## Execução do artefato presente

Execute os comandos nesta pasta. Copie `.env.example` para `.env`, preencha a chave do provider e configure `OPENAI_MODEL` com um identificador de modelo disponível para sua conta.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Depois de preencher o `.env`, execute:

```bash
python main.py "Explique AI Gateway em uma aplicação de suporte"
```

O prompt é um registro da aula, e o código presente pode ter defaults diferentes. Confira [main.py](main.py), [requirements.txt](requirements.txt) e [.env.example](.env.example). As dependências não estão fixadas; anote as versões usadas ao comparar resultados.

## Limites do exemplo

O `main.py` usa `gpt-4-mini` quando `OPENAI_MODEL` não está definido, enquanto o prompt histórico pede outro default. Defina o modelo no ambiente; o repositório não comprova a existência desse alias. O código faz chamada direta e trata erros de forma genérica. Timeout e retries são herdados do SDK, sem política explícita da aplicação.
