# Projeto prático — Async Ticket Analysis

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

API FastAPI com três fluxos de chamada:

- `POST /tickets/analyze`: síncrono, espera a IA e devolve JSON.
- `POST /tickets/explain`: streaming, devolve texto em partes.
- `POST /tickets/full-analysis`: cria job e responde imediatamente.
- `GET /jobs/{job_id}`: consulta status e resultado do job.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de rodar.

## Fluxo assíncrono

```text
POST /tickets/full-analysis -> {"job_id": "...", "status": "pending"}
BackgroundTasks -> processing -> OpenAI -> completed ou failed
GET /jobs/{job_id} -> status atual e resultado
```

O arquivo `requests.http` usa `# @name createJob` para reaproveitar o `job_id` automaticamente na consulta.

## Nota de produção

O arquivo `app/jobs.py` usa memória local para fins didáticos. Uma evolução de produção precisa de armazenamento de estado compartilhado e de um mecanismo de fila/worker com políticas de recuperação. Trocar somente o dicionário por banco ou Redis não torna `BackgroundTasks` durável.

## Contrato e verificação local

Rode cada projeto na própria pasta; todos expõem `127.0.0.1:8000`, então use um de cada vez. Depois de iniciar, os contratos estão em `http://127.0.0.1:8000/docs` e os exemplos de requisições em [requests.http](requests.http).

O modelo padrão do código é `gpt-4.1-mini`, substituível por `OPENAI_MODEL`. Se mudar o modelo, confira suporte a Chat Completions e ao JSON mode usado na análise. As dependências não estão fixadas; registre versões para reproduzir um resultado.

`POST /tickets/analyze` responde somente depois da análise completa. `message=""` gera 422; entrada contendo apenas espaços ainda passa em `min_length=1`. `category` e `priority` são strings, sem validação de enum. Erros do provider ou de parse/schema são tratados genericamente com 500. Veja os [limites verificados no código](../../README.md#limites-verificados-no-código).

## Consumindo o fluxo de texto

`POST /tickets/explain` retorna `text/plain; charset=utf-8`. Use `curl -N` ou `fetch` com leitura incremental do corpo; não use `EventSource` como se esse POST fosse um endpoint SSE. Os fragmentos devem ser concatenados e decodificados incrementalmente.

O texto `[erro ao gerar o restante da resposta]` sinaliza falha capturada durante a iteração. Ele pode aparecer em uma resposta com HTTP 200, inclusive sem conteúdo útil anterior. O código não oferece eventos explícitos de término, retomada ou cancelamento upstream. Veja [streaming e SSE](../../03-streaming-and-perceived-latency/README.md).

## O que esperar do job didático

A criação responde HTTP 200 com `job_id` e `status=pending`. A tarefa é executada via `BackgroundTasks` no mesmo processo; a primeira consulta já pode mostrar outro estado. Um ID desconhecido retorna 404.

Restart, recarga automática do Uvicorn e encerramento do processo podem perder os jobs. Não existem autenticação por dono do job, retenção, deduplicação, retry do job ou garantia de retomada. O REST Client é necessário para a variável `{{createJob.response.body.$.job_id}}`; em outro client, copie o ID retornado e use-o na URL.

**Verificação de entendimento:** explique o que acontece se o processo encerrar depois de retornar `job_id` e antes de concluir a IA. Compare essa resposta com o contrato de uma fila durável descrito na [aula 04](../../04-when-to-turn-ai-into-async-processing/README.md).
