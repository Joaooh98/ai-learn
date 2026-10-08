# Minimal Proxy Client

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

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

## Preparação e reprodução

Execute um único projeto de proxy por vez: os exemplos usam o mesmo nome de container `litellm-proxy` e a porta `4000`. Preencha as chaves no `.env` antes de subir o serviço. `docker compose up` permanece no primeiro terminal; rode o client em outro.

A tag `main-stable` e as dependências Python não fixadas podem mudar. Registre a imagem/versão e as dependências efetivamente instaladas ao reproduzir a aula. Não há lockfile ou teste de integração com provider neste material.

Se alterar variáveis que o Compose injeta no container, execute `docker compose up --force-recreate` para aplicar os novos valores. Editar o `.env` não muda o ambiente de um processo já iniciado.

A master key do laboratório permite acesso administrativo e não representa isolamento por aplicação. Para os detalhes de chaves, timeout, retries e escopo implementado, veja o [índice do módulo](../../README.md).
