# Minimal Proxy Client

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

> Origem: aula 14 — LiteLLM Proxy na pratica.

Este projeto registra a primeira metade da pratica: preparar uma aplicacao Python minima para chamar o LiteLLM Proxy local em vez de chamar a OpenAI diretamente.

## Arquitetura

```text
Aplicacao Python -> LiteLLM Proxy -> OpenAI
```

## O que esta aula cobre

- estrutura de pastas;
- `docker-compose.yml` para subir o proxy;
- `litellm/config.yaml` com o modelo interno `developer-assistant`;
- `.env.example` separando chave real do provider e chave local do proxy;
- prompt usado pela aplicacao.

## Prompt da aula

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

## Fluxo esperado

1. A aplicacao usa o nome interno `developer-assistant`.
2. O client aponta para `http://localhost:4000`.
3. O proxy autentica a chamada usando `LITELLM_MASTER_KEY`.
4. O proxy resolve `developer-assistant` para o modelo real configurado.
5. O provider responde.
6. A resposta volta para a aplicacao em formato compativel com OpenAI.

## Observacao

A aula 14 registra a montagem inicial, e a aula 15 registra sua continuação. O `app/main.py` presente nesta pasta já contém uma chamada executável completa ao proxy.

## Como executar o código presente

Nesta pasta, prepare `.env` com as chaves e suba o proxy:

```bash
cp .env.example .env
docker compose up
```

Depois de preencher o `.env` e com o proxy disponível, abra outro terminal nesta pasta:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
python app/main.py "Explique AI Gateway com um exemplo de suporte"
```

O client roda no host e chama `localhost:4000`. A chave administrativa é usada somente para simplificar o laboratório. Veja os [limites dos exemplos](../../README.md#o-que-os-exemplos-implementam) e a [continuação da prática](../../15-litellm-proxy-in-practice-part-2/README.md).
