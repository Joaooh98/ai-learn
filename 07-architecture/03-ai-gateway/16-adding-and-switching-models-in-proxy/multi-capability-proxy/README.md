# Multi Capability Proxy

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

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

## Preparação e reprodução

Execute um único projeto de proxy por vez: os exemplos usam o mesmo nome de container `litellm-proxy` e a porta `4000`. Preencha as chaves no `.env` antes de subir o serviço. `docker compose up` permanece no primeiro terminal; rode o client em outro.

A tag `main-stable` e as dependências Python não fixadas podem mudar. Registre a imagem/versão e as dependências efetivamente instaladas ao reproduzir a aula. Não há lockfile ou teste de integração com provider neste material.

Se alterar variáveis que o Compose injeta no container, execute `docker compose up --force-recreate` para aplicar os novos valores. Editar o `.env` não muda o ambiente de um processo já iniciado.

A master key do laboratório permite acesso administrativo e não representa isolamento por aplicação. Para os detalhes de chaves, timeout, retries e escopo implementado, veja o [índice do módulo](../../README.md).
