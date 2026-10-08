# Weak Model Fallback Validation

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

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

## Preparação e reprodução

Execute um único projeto de proxy por vez: os exemplos usam o mesmo nome de container `litellm-proxy` e a porta `4000`. Preencha as chaves no `.env` antes de subir o serviço. `docker compose up` permanece no primeiro terminal; rode o client em outro.

A tag `main-stable` e as dependências Python não fixadas podem mudar. Registre a imagem/versão e as dependências efetivamente instaladas ao reproduzir a aula. Não há lockfile ou teste de integração com provider neste material.

Se alterar variáveis que o Compose injeta no container, execute `docker compose up --force-recreate` para aplicar os novos valores. Editar o `.env` não muda o ambiente de um processo já iniciado.

A master key do laboratório permite acesso administrativo e não representa isolamento por aplicação. Para os detalhes de chaves, timeout, retries e escopo implementado, veja o [índice do módulo](../../README.md).

## Validação e cenário de falha

Apontar `PRIMARY_MODEL` para um modelo inexistente produz um erro de configuração, não uma reprodução fiel de todo incidente de rede ou provider. Observe o erro e o destino final; a classificação do erro e a política de fallback dependem da versão executada.

`contrato_quebrado()` não exige `reason`, não limita campos extras e pode falhar com `TypeError` para categoria em lista/objeto. “VALIDA” significa passar nessas verificações parciais, não validar todo o schema nem comprovar acerto semântico. O client usa somente prompt para pedir JSON, sem `response_format`.

O comportamento exibido do backup é um resultado histórico. Um modelo menos capaz pode obedecer ao formato em outras entradas; um modelo mais capaz também pode produzir uma resposta inadequada.
