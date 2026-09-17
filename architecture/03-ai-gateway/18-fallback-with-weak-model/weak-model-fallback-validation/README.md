# Weak Model Fallback Validation

> Origem: aula 18 — Fallback com modelo fraco.

Este projeto registra o limite do fallback tecnico: mesmo quando o proxy consegue uma resposta de backup, a aplicacao ainda precisa validar se a resposta cumpre o contrato esperado.

## Caso de uso

Classificacao de ticket de suporte.

Entrada padrao:

```text
Fui cobrado duas vezes na minha assinatura e quero resolver isso.
```

Saida esperada:

```json
{"category":"billing","reason":"Cobranca duplicada na assinatura"}
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

## Cenarios

Para simular o fallback, a aula aponta `PRIMARY_MODEL` para um modelo inexistente. O proxy entao aciona `support-ticket-classifier-backup`.

O ponto didatico: o fallback pode retornar HTTP 200, mas ainda quebrar o contrato se vier com markdown, texto extra ou JSON invalido.
