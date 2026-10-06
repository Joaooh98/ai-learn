# Projeto prático — Streaming Ticket Explanation

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

API FastAPI com dois fluxos para comparar a experiência:

- `POST /tickets/analyze`: chamada síncrona que devolve JSON completo.
- `POST /tickets/explain`: chamada com streaming que devolve texto em partes.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Preencha `OPENAI_API_KEY` no `.env` antes de rodar.

## Teste do streaming

```bash
curl -N -w "\nTempo total: %{time_total}s\n" \
  -X POST http://127.0.0.1:8000/tickets/explain \
  -H "Content-Type: application/json" \
  -d '{"message": "Fui cobrado duas vezes e preciso de ajuda com meu pagamento."}'
```

Use `-N` para o curl mostrar os chunks sem esperar bufferizar a resposta completa.

## Contrato e verificação local

Rode cada projeto na própria pasta; todos expõem `127.0.0.1:8000`, então use um de cada vez. Depois de iniciar, os contratos estão em `http://127.0.0.1:8000/docs` e os exemplos de requisições em [requests.http](requests.http).

O modelo padrão do código é `gpt-4.1-mini`, substituível por `OPENAI_MODEL`. Se mudar o modelo, confira suporte a Chat Completions e ao JSON mode usado na análise. As dependências não estão fixadas; registre versões para reproduzir um resultado.

`POST /tickets/analyze` responde somente depois da análise completa. `message=""` gera 422; entrada contendo apenas espaços ainda passa em `min_length=1`. `category` e `priority` são strings, sem validação de enum. Erros do provider ou de parse/schema são tratados genericamente com 500. Veja os [limites verificados no código](../../README.md#limites-verificados-no-código).

## Consumindo o fluxo de texto

`POST /tickets/explain` retorna `text/plain; charset=utf-8`. Use `curl -N` ou `fetch` com leitura incremental do corpo; não use `EventSource` como se esse POST fosse um endpoint SSE. Os fragmentos devem ser concatenados e decodificados incrementalmente.

O texto `[erro ao gerar o restante da resposta]` sinaliza falha capturada durante a iteração. Ele pode aparecer em uma resposta com HTTP 200, inclusive sem conteúdo útil anterior. O código não oferece eventos explícitos de término, retomada ou cancelamento upstream. Veja [streaming e SSE](../../03-streaming-and-perceived-latency/README.md).
