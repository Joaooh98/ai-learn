# Minimal Proxy Client

> Origem: aula 15 — LiteLLM Proxy na pratica, parte 2.

Esta pasta registra a versao completa do exemplo pratico: uma aplicacao Python chama o LiteLLM Proxy local usando o SDK da OpenAI como client compativel.

## Arquitetura

```text
Aplicacao Python -> LiteLLM Proxy -> OpenAI
```

## Prompt extraido da aula

Prompt de sistema:

```text
Voce e um arquiteto de software explicando IA para desenvolvedores.
Responda de forma didatica, pratica e objetiva. O tema e AI Gateway.
Explique o conceito conectando com problemas reais de aplicacoes que chamam modelos de IA em producao. Responda com 2 paragrafos.
```

Pergunta padrao:

```text
O que e uma AI Gateway e por que ela e importante em aplicacoes com IA?
```

## Como executar

Crie um `.env` a partir de `.env.example` e preencha as chaves:

```bash
cp .env.example .env
```

Suba o proxy:

```bash
docker compose up
```

Em outro terminal, execute a aplicacao:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Tambem e possivel enviar uma pergunta pela linha de comando:

```bash
python main.py "Explique AI Gateway usando um exemplo de suporte ao cliente"
```

## Resultado esperado

A aplicacao deve imprimir o modelo logico `developer-assistant`, a pergunta usada e uma resposta em dois paragrafos. O modelo real fica escondido atras do proxy.
