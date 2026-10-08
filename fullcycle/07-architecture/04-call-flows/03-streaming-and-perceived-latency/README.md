# Aula 03 — Streaming e latência percebida

[Índice do módulo](../README.md)

> Curso: **Fluxos de Chamada** · Duração: `05:31`

Esta aula mostra que streaming não necessariamente diminui o tempo total de processamento, mas muda radicalmente a percepção do usuário porque reduz o tempo até o primeiro retorno visível.

## Resumo

No fluxo síncrono, o usuário envia uma pergunta e espera até a IA concluir tudo. No streaming, a aplicação começa a renderizar pequenos pedaços da resposta enquanto o modelo ainda está gerando o restante.

```text
Síncrono:  pergunta -> IA processa -> resposta completa
Streaming: pergunta -> IA processa -> chunk 1 -> chunk 2 -> ... -> resposta final
```

Mesmo que a resposta completa demore 18 segundos, se o primeiro texto aparece em 1,5 segundo o usuário percebe progresso e passa a confiar mais no fluxo.

## Exemplo da aula

O caso apresentado é uma explicação textual para um ticket:

```http
POST /tickets/explain
Accept: text/event-stream
```

A IA produz texto progressivo e o frontend renderiza conforme os chunks chegam:

```text
chunk 1 + chunk 2 + chunk 3 + ... + chunk n
```

Esse padrão é ideal para explicações, resumos, recomendações e conversas, porque o conteúdo já tem valor parcial.

## Quando streaming serve

Streaming funciona bem quando a resposta pode ser consumida gradualmente:

- explicações;
- conversas;
- raciocínios narrativos;
- resumos longos;
- recomendações textuais.

Nesses casos, ver o caminho da resposta sendo construído melhora a experiência.

## Quando o resultado precisa estar completo

Streaming não dispensa esperar o fechamento e validar resultados usados como decisão final:

- JSON final;
- validações;
- decisões estruturadas;
- dados usados diretamente por outro sistema.

Um JSON parcial pode parecer válido visualmente, mas ainda estar incompleto. Se o frontend interpreta pedaços como decisão final, a aplicação pode agir com dados errados.

## Falhas no meio do stream

Depois que a resposta começou, uma falha não se comporta como erro HTTP comum. A conexão pode cair, o servidor pode falhar ou o provider pode interromper a geração. A interface precisa mostrar estado, permitir retry e evitar ações automáticas com conteúdo incompleto.

## Streaming ou job assíncrono?

Pergunta principal:

```text
O usuário ganha alguma coisa vendo a resposta aos poucos?
```

Se sim, streaming. Se não, entregue a resposta completa quando estiver pronta ou transforme em job assíncrono.

## Ideia-chave

Streaming é uma ferramenta de experiência, não uma solução universal de performance. Ele é excelente quando o valor aparece antes da resposta completa.

## Complemento — Streaming, SSE e contrato de eventos

O cabeçalho `Accept: text/event-stream` mostrado acima ilustra SSE conceitualmente. O [demo da aula 06](../06-streaming-example/streaming-ticket-explanation/README.md) entrega `text/plain; charset=utf-8`, sem eventos SSE. Enviar esse `Accept` não converte o corpo em SSE.

SSE requer `Content-Type: text/event-stream` e mensagens com campos como `event`, `data` e, quando usado, `id`, separadas por uma linha vazia. O navegador recebe eventos enquadrados nesse protocolo. O `EventSource` nativo abre uma URL via GET; o POST JSON do exemplo é melhor consumido com `fetch` e leitura incremental do corpo, ou exige outro contrato de endpoint. [Especificação oficial de SSE](https://html.spec.whatwg.org/multipage/server-sent-events.html).

Chunks de rede não são necessariamente tokens nem frases completas. O consumidor precisa decodificar UTF-8 incrementalmente e preservar fragmentos quando interpreta eventos ou JSON. Para dados estruturados, pode exibir progresso e juntar o documento; a ação de negócio espera conclusão e validação.

Streaming não reduz por si só quantidade de tokens, chamadas ou trabalho do modelo. Ainda mantém conexão aberta e requer tratamento de cancelamento, buffer no caminho, pausa entre chunks e falhas parciais. Meça tempo até o primeiro texto e tempo total separadamente.
