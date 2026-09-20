# Aula 07 — Trabalhando de forma assíncrona

> Curso: **Fluxos de Chamada** · Duração: `06:18`

Esta aula adiciona o terceiro fluxo do módulo: processamento assíncrono por job. A request cria um trabalho, recebe um `job_id` imediatamente e a IA roda depois, fora da resposta original.

## Resumo

O fluxo implementado é:

```text
POST /tickets/full-analysis -> cria job pending -> responde job_id
BackgroundTasks -> processing -> chama IA -> completed/failed
GET /jobs/{job_id} -> consulta status e resultado
```

Nos prints, o projeto continua com os endpoints anteriores:

- `POST /tickets/analyze`: síncrono, devolve JSON estruturado.
- `POST /tickets/explain`: streaming, devolve texto progressivo.
- `POST /tickets/full-analysis`: assíncrono, cria job.
- `GET /jobs/{job_id}`: consulta status/resultado.

## Job store didático

A aula usa um dicionário Python em memória para armazenar jobs:

```text
job_id -> {"job_id", "status", "result?", "error?"}
```

Estados possíveis:

```text
pending -> processing -> completed
pending -> processing -> failed
```

Isso é suficiente para aprender o fluxo, mas não é produção: ao reiniciar o processo os jobs somem, e múltiplos workers não compartilham esse dicionário. Em produção, isso viraria banco, Redis, fila real, Celery/RQ ou serviço equivalente.

## Resultado esperado

Ao criar o job:

```json
{
  "job_id": "job_4c009606",
  "status": "pending"
}
```

Depois de consultar:

```json
{
  "job_id": "job_4c009606",
  "status": "completed",
  "result": {
    "category": "billing",
    "priority": "high",
    "summary": "Cobrança duplicada no pagamento",
    "recommended_action": "Verificar as transações recentes do cliente e iniciar o processo de estorno para a cobrança duplicada."
  }
}
```

## Projeto prático

O projeto reproduzível está em [async-ticket-analysis](./async-ticket-analysis/README.md).

## Ideia-chave

Assíncrono muda o contrato da funcionalidade. O cliente não recebe o resultado da IA na primeira resposta; ele recebe um identificador e passa a acompanhar estado.
