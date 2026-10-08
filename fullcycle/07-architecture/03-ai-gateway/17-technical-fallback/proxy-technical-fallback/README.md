# Proxy Technical Fallback

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

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

## Preparação e reprodução

Execute um único projeto de proxy por vez: os exemplos usam o mesmo nome de container `litellm-proxy` e a porta `4000`. Preencha as chaves no `.env` antes de subir o serviço. `docker compose up` permanece no primeiro terminal; rode o client em outro.

A tag `main-stable` e as dependências Python não fixadas podem mudar. Registre a imagem/versão e as dependências efetivamente instaladas ao reproduzir a aula. Não há lockfile ou teste de integração com provider neste material.

Se alterar variáveis que o Compose injeta no container, execute `docker compose up --force-recreate` para aplicar os novos valores. Editar o `.env` não muda o ambiente de um processo já iniciado.

A master key do laboratório permite acesso administrativo e não representa isolamento por aplicação. Para os detalhes de chaves, timeout, retries e escopo implementado, veja o [índice do módulo](../../README.md).

## Evidência de fallback

A linha `Modelo: developer-assistant` mostra o alias solicitado, não o destino final. Confira a falha do primário e o deployment do backup nos logs do proxy. O YAML não fixa retries nem timeout. O backup está publicado como outro modelo lógico, e a master key também pode chamá-lo diretamente.

A regra `litellm_settings.fallbacks` aparece em exemplos oficiais; o quickstart atual mostra `router_settings.fallbacks`. Confira o comportamento da versão usada antes de atribuir um problema ao local da configuração. [Referência de failover](https://docs.litellm.ai/docs/proxy/reliability).
