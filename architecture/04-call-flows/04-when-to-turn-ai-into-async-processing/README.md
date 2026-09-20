# Aula 04 — Quando transformar IA em processamento assíncrono

> Curso: **Fluxos de Chamada** · Duração: `03:52`

Esta aula separa dois conceitos que às vezes são confundidos: streaming e processamento assíncrono. Streaming ainda mantém uma request aberta; processamento assíncrono tira o trabalho pesado da request original.

## Resumo

Streaming é útil quando o usuário se beneficia de receber partes da resposta. Processamento assíncrono é indicado quando o trabalho é longo, pesado, frágil ou composto por várias etapas.

```text
Streaming: request aberta -> resposta em partes
Assíncrono: request cria job -> processamento roda depois -> usuário consulta status
```

## O que não cabe na mesma request

O material usa uma tarefa pesada de suporte como exemplo:

```text
ler tickets -> classificar -> resumir -> identificar prioridade -> consolidar resultado
```

Esse fluxo chama IA, tem múltiplas etapas e pode demorar. Se rodar dentro de uma única request HTTP, surgem riscos:

- timeout;
- falha no meio;
- aba fechada pelo usuário;
- cliques repetidos;
- recursos presos durante toda a execução.

## Arquitetura com job

Fluxo recomendado:

```text
1. usuário envia POST
2. API cria job com status pending
3. API retorna job_id imediatamente
4. worker pega o job
5. worker chama IA e processa
6. resultado/status é salvo
7. usuário acompanha por GET /jobs/{id}, WebSocket, SSE ou notificação
```

Estados principais do job:

```text
pending -> processing -> completed
pending -> processing -> failed
```

Cada job deve ter um ID único e pode carregar logs, mensagens intermediárias e resultado parcial, dependendo da necessidade do produto.

## Decisão arquitetural

A pergunta central da aula é:

```text
Precisa terminar na requisição original?
```

Se sim, execute na request direta e responda ao usuário de forma síncrona. Se não, a tarefa é boa candidata a job.

## O que muda com assíncrono

Processamento assíncrono muda o desenho da funcionalidade, não apenas onde o código roda:

- **Camada**: sai da camada de request e entra na camada de processamento.
- **Fluxo**: passa a ter etapas desacopladas, fila/worker e estado explícito.
- **Observabilidade**: precisa de logs, métricas, traces e dashboard ponta a ponta.
- **Retry**: precisa de políticas de retry, backoff e DLQ para falhas transientes.

## Ideia-chave

Quando a IA não precisa terminar dentro da request original, transformar a operação em job deixa a aplicação mais resiliente, mais observável e menos vulnerável a timeouts.
