# Aula 06 — Exemplificando com streaming

[Índice do módulo](../README.md)

> Curso: **Fluxos de Chamada** · Duração: `05:29`

Esta aula evolui a API síncrona da aula anterior adicionando um endpoint de streaming para explicação textual. A ideia é comparar dois fluxos no mesmo backend: JSON completo para máquina e texto progressivo para experiência humana.

## Resumo

A aplicação passa a ter dois caminhos:

```text
Fluxo 1: /tickets/analyze -> espera a IA terminar -> devolve JSON
Fluxo 2: /tickets/explain -> IA gera chunks -> devolve texto em partes
```

O endpoint de streaming não tenta devolver JSON. Ele usa um prompt próprio para texto corrido, em português, com frases curtas e progressivas.

## Prompt de explicação

```text
Você é um assistente de suporte. Explique, em texto corrido e em português,
o que o cliente está relatando e qual a recomendação inicial de tratamento.
Escreva de forma progressiva, em algumas frases curtas. Não use JSON.
```

## Implementação vista na aula

No cliente de IA:

- `stream=True` faz o SDK devolver um iterável de chunks.
- Cada `chunk.choices[0].delta.content` é repassado com `yield`.
- Se houver erro no meio do stream, a aplicação não consegue mais trocar o status HTTP; por isso envia uma mensagem simples no próprio texto.

Na rota FastAPI:

- `POST /tickets/explain` retorna `StreamingResponse`.
- A rota tenta puxar o primeiro chunk antes de começar a resposta. Uma exceção que escape do gerador nesse ponto vira HTTP 500; erros capturados dentro do gerador podem ser entregues como texto com HTTP 200.
- Depois do primeiro byte enviado, o restante é entregue com `yield from chunks`.

## Teste com curl

O print usa `curl -N` para não bufferizar a resposta:

```bash
curl -N -w "\nTempo total: %{time_total}s\n" \
  -X POST http://127.0.0.1:8000/tickets/explain \
  -H "Content-Type: application/json" \
  -d '{"message": "Fui cobrado duas vezes e preciso de ajuda com meu pagamento."}'
```

## Projeto prático

O projeto reproduzível está em [streaming-ticket-explanation](./streaming-ticket-explanation/README.md).

## Ideia-chave

Neste exemplo, streaming entrega explicação textual progressiva. Dados estruturados também podem ser transmitidos em partes, desde que o consumidor tenha um protocolo de eventos e valide o resultado final antes de agir.

## Complemento — Comportamento observado no código

A resposta é um fluxo de texto simples, sem SSE ou eventos `done/error`. O consumidor junta os fragmentos do corpo. Não existe correspondência garantida entre cada `yield` e cada chunk recebido pelo navegador, porque os buffers do transporte podem agrupar conteúdo.

O prefetch chama `next(chunks)` antes de criar a resposta. Falhas na criação da chamada ao provider podem escapar e virar HTTP 500. Já o bloco `try/except` dentro de `explain_ticket()` captura erros durante a iteração, inclusive antes do primeiro texto, e os transforma em uma mensagem textual. Nesse caso a rota pode enviar HTTP 200 com essa mensagem; o status não prova conclusão bem-sucedida.

Depois de iniciada a resposta, um erro precisa de um sinal no contrato do corpo. Em uma evolução, eventos explícitos de conclusão e falha são mais confiáveis do que acrescentar um marcador indistinguível do conteúdo do modelo.

O demo não fecha explicitamente o stream upstream nem implementa cancelamento da geração quando o client desconecta. Encerrar leitura local não assegura interrupção remota. Esses pontos devem ser verificados ao evoluir o client e o servidor.
