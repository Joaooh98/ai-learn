# 04 — Fluxos de Chamada

[Arquitetura](../README.md) · [Anterior: AI Gateways](../03-ai-gateway/README.md) · [Próximo: Cache](../05-cache/README.md)

Este módulo decide como entregar trabalho de IA ao usuário: resposta completa na request, texto progressivo ou job acompanhado por estado. A escolha envolve contrato, prazo, utilidade de uma resposta parcial e capacidade de recuperar o trabalho após falha.

## Roteiro de estudo

| Aula | Assunto | Duração | Foco |
|---|---|---|---|
| 01 | [O problema de execução em aplicações com IA](01-execution-problem-in-ai-applications/README.md) | `04:44` | Identificar prazo e experiência necessários |
| 02 | [Quando uma chamada síncrona ainda faz sentido](02-when-a-synchronous-call-still-makes-sense/README.md) | `04:17` | Reservar resposta completa para tarefas adequadas |
| 03 | [Streaming e latência percebida](03-streaming-and-perceived-latency/README.md) | `05:31` | Separar progresso e tempo total |
| 04 | [Quando transformar IA em processamento assíncrono](04-when-to-turn-ai-into-async-processing/README.md) | `03:52` | Projetar estado e recuperação |
| 05 | [Trabalhando de forma síncrona na prática](05-working-synchronously-in-practice/README.md) | `04:51` | Ler o baseline FastAPI |
| 06 | [Exemplificando com streaming](06-streaming-example/README.md) | `05:29` | Interpretar entrega incremental e falha parcial |
| 07 | [Trabalhando de forma assíncrona](07-working-asynchronously/README.md) | `06:18` | Observar o contrato de job e seus limites |

## Três dimensões que não devem ser confundidas

| Dimensão | Pergunta | Exemplos |
|---|---|---|
| Concorrência no processo | A execução bloqueia o event loop ou aguarda I/O? | Client síncrono em thread pool; client assíncrono com `await` |
| Entrega HTTP | Quando o cliente recebe o resultado? | Resposta completa; corpo progressivo; ID para consultar depois |
| Durabilidade do trabalho | A tarefa sobrevive a restart e pode ser retomada? | Memória local; estado persistido e fila/worker com recuperação |

Uma rota `async def` que faz `await` e só então retorna JSON ainda entrega resultado completo na request original. Uma rota `def` pode atender esse mesmo contrato em thread pool. FastAPI executa operações `def` nesse pool; funções utilitárias chamadas diretamente não são automaticamente convertidas em não bloqueantes. [Documentação oficial de concorrência](https://fastapi.tiangolo.com/async/).

Nos exemplos, os clients são síncronos e as rotas são `def`. A execução evita chamar o SDK bloqueante diretamente no event loop, mas continua ocupando recursos durante a espera. O pool compartilhado tem capacidade limitada; também é usado por tarefas síncronas em background. [Thread pool do Starlette](https://starlette.dev/threadpool/).

## Comparação dos fluxos

| Aspecto | Resposta completa | Streaming | Job |
|---|---|---|---|
| Primeira entrega útil | Resultado final | Primeiro conteúdo aproveitável | ID e status; resultado depois |
| Conexão original | Aberta até terminar | Aberta durante o fluxo | Encerrada após aceitar/criar tarefa |
| Resultado parcial | Geralmente não publicado | Publicado com estado incompleto | Pode ser salvo/publicado como progresso |
| Falha depois da entrega | Cliente pode ter perdido o retorno | Precisa de sinal de falha no corpo | Precisa registrar falha/retomar em estado persistido |
| Uso típico | Classificação curta | Explicação textual progressiva | Análise longa ou com várias etapas |
| Custo de operação | Prazo e concorrência | Prazo, buffers, conexão e cancelamento | Fila, persistência, workers, retry e retenção |

Streaming muda quando o conteúdo aparece, sem diminuir automaticamente tokens ou trabalho do modelo. Job muda onde o trabalho continua e como o cliente acompanha. Nenhum dos dois elimina limites de concorrência, custo ou necessidade de validar a saída.

## Contratos implementados nos exemplos

| Projeto | Rotas | Comportamento efetivo |
|---|---|---|
| [Síncrono](05-working-synchronously-in-practice/sync-ticket-analysis/README.md) | `POST /tickets/analyze` | Aguarda OpenAI, parseia JSON, valida Pydantic e responde |
| [Streaming](06-streaming-example/streaming-ticket-explanation/README.md) | Análise + `POST /tickets/explain` | Texto simples incremental, sem framing SSE |
| [Jobs](07-working-asynchronously/async-ticket-analysis/README.md) | Análise + explicação + `POST /tickets/full-analysis` + `GET /jobs/{job_id}` | HTTP 200 na criação; `BackgroundTasks`; dicionário no processo |

Todos os demos usam `127.0.0.1:8000`; execute um por vez na própria pasta. Os READMEs incluem ambiente, comandos e requisições. O modelo padrão é `gpt-4.1-mini`, substituível por `OPENAI_MODEL`; valide o suporte aos parâmetros se alterar o modelo.

## Streaming e contrato do consumidor

`StreamingResponse` transmite o que o gerador entrega e usa o media type definido. O exemplo escolhe `text/plain; charset=utf-8`. Essa entrega não se transforma em SSE apenas porque o client enviou `Accept: text/event-stream`. [Resposta incremental do Starlette](https://starlette.dev/responses/).

Para o demo, o consumidor deve ler o corpo incrementalmente, decodificar UTF-8 sem quebrar caracteres e concatenar os fragmentos. Fronteiras de rede não equivalem a fronteiras de tokens. O protocolo SSE, sua diferença para texto simples e o limite do `EventSource` estão detalhados na [aula 03](03-streaming-and-perceived-latency/README.md).

Mantenha estados de interface como `iniciando`, `recebendo`, `concluído`, `interrompido` e `falhou`. O exemplo não publica um evento de conclusão/falha; ele acrescenta um marcador de erro ao texto. HTTP 200 e encerramento do corpo não bastam para distinguir todas as causas de interrupção.

Meça tempo até o primeiro conteúdo visível, intervalo entre conteúdos e tempo total. Verifique buffering em client, proxy e ingress; `curl -N` desabilita o buffer do curl, sem controlar as outras camadas. `time_starttransfer` mede início da resposta HTTP e não necessariamente o primeiro texto útil.

## Do job didático ao job durável

No FastAPI, `BackgroundTasks` dispara trabalho após a resposta no mesmo processo da aplicação. É uma facilidade de execução, não uma fila persistida. [Referência oficial](https://fastapi.tiangolo.com/tutorial/background-tasks/).

No demo, `job_id` identifica um item em um dicionário. Restart perde estado; múltiplos processos não o compartilham. A primeira consulta pode encontrar um estado posterior a `pending`. Não há garantia de execução uma vez, retomada, cancelamento ou deduplicação.

Uma evolução precisa definir:

1. Como registrar a tarefa e garantir sua publicação sem criar jobs órfãos.
2. Como consumir, confirmar e eventualmente repetir trabalho depois de falhas.
3. Como persistir resultado, erro, tentativas, prazo e progresso.
4. Como impedir efeitos externos duplicados e consultas indevidas entre usuários.
5. Como limitar concorrência e controlar acúmulo, retenção e expiração.

Trocar o dicionário por banco ou Redis resolve apenas parte do armazenamento. A fila, os workers e a política de recuperação continuam sendo decisões adicionais. A [aula 04](04-when-to-turn-ai-into-async-processing/README.md) relaciona essas decisões com idempotência e coordenação da publicação.

## Limites verificados no código

- **Entrada:** `min_length=1` rejeita string vazia, mas admite espaços; não há máximo de tamanho.
- **Saída:** `category` e `priority` são `str`; seus exemplos nas descrições não impõem enums. O schema não proíbe campos extras explicitamente. [Modelos e validação Pydantic](https://pydantic.dev/docs/validation/latest/concepts/models/).
- **JSON:** os clients de análise usam `json_object`, sem enviar JSON Schema. Parse/validação de formato não comprovam classificação correta. [Saídas estruturadas oficiais](https://developers.openai.com/api/docs/guides/structured-outputs).
- **Erros:** análise mapeia parse, schema e falhas do provider para 500; não há tradução específica de quota, credencial ou timeout.
- **Resiliência:** timeout e retries não são configurados nos clients. Eles herdam a versão instalada; a [política do módulo de gateway](../03-ai-gateway/README.md#resiliência-com-orçamento-ponta-a-ponta) explica o impacto.
- **Streaming:** prefetch não converte todo erro inicial em 500; exceções capturadas no gerador tornam-se texto. Não há fechamento explícito do stream upstream nem protocolo de cancelamento/retomada.
- **Jobs:** sem persistência, retenção, autorização por dono, deduplicação ou retry do job. Os oito caracteres do UUID não são acompanhados de verificação de colisão.
- **Reprodução:** dependências não fixadas e Uvicorn com `reload=True`; são artefatos de estudo, sem validação de implantação de produção.

## Exercício de revisão

Com a mesma mensagem de ticket, desenhe os três contratos. Para cada um, indique o prazo permitido, a evidência de conclusão, o comportamento ao fechar a aba e a recuperação depois de reiniciar o servidor. Depois repita com JSON inválido, indisponibilidade do provider e timeout no client. O ponto é prever o estado observável, não presumir que trocar a sintaxe da função melhora a garantia.

Na integração com [05 — Cache](../05-cache/README.md), trate separadamente resultado final reaproveitável e estado de job. Um job em `processing` não é uma resposta pronta; cache também não substitui persistência de trabalho aceito.

## Fontes e critério de revisão

Revisão documental e leitura dos artefatos em **1 de outubro de 2026**. Referências primárias acompanham os assuntos. Durações e registros das aulas foram preservados. As ressalvas descrevem limites observáveis do código; as evoluções propostas não são funcionalidades já implementadas.
