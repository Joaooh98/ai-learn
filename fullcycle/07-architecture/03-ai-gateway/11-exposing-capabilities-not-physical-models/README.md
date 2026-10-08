# Aula 11 — Expondo capacidades, não modelos físicos

[Índice do módulo](../README.md)

> Curso: **AI Gateways** · Duração: `03:28`

## Resumo

A aula reforça a ideia de que a aplicação não deveria depender de modelos físicos. Em vez de pedir `gpt-*`, `claude-*` ou `gemini-*`, ela deveria pedir capacidades como classificação, resposta ao usuário, extração de documento ou análise profunda.

O gateway vira a camada que traduz intenção de uso em provider/modelo real.

## 1. Gateway como camada de abstração

![Gateway entre app e providers](./01.png)

O gateway fica entre a aplicação e os providers de IA. Ele não elimina a existência do modelo físico, mas impede que esse detalhe vaze para o contrato da aplicação.

Responsabilidades:

- roteamento;
- transformação de request/response;
- autenticação e chaves;
- políticas;
- observabilidade;
- cache, retry e circuit breaker.

Um erro comum é criar o gateway sem mudar o nível de abstração. Se a aplicação continua pedindo diretamente modelos físicos, o gateway agrega menos valor.

## 2. Aplicação pede capacidade

![Capacidades internas](./02.png)

Exemplos de capacidades internas:

- `classificador simples`;
- `resposta suporte`;
- `extracao de documento`;
- `analise profunda`;
- `embedding padrao`.

O mapeamento interno decide se essa capacidade será atendida por OpenAI, Anthropic, Google ou outro provider.

## 3. Bons nomes

![Nomes úteis](./03.png)

Nomes bons comunicam intenção de uso. Nomes ruins comunicam detalhe técnico ou ordem arbitrária.

Bons exemplos:

- `classificacao`;
- `resposta ao usuario`;
- `analise pesada`.

Evitar:

- `modelo 1`;
- `modelo 2`;
- `modelo rapido`.

O nome deveria permanecer estável mesmo quando o provider muda.

## 4. Evolução do desenho

![Provider-centric vs capability-centric](./04.png)

No desenho orientado a provider, a aplicação acopla diretamente com a tecnologia externa. No desenho orientado a capacidade, a aplicação fala com o gateway e o gateway decide o provider físico.

Perguntas úteis para modelar capacidades:

- quem usa?
- qual time, produto ou cenário?
- qual custo esperado?
- quais limites de rate, contexto e quota?

## Ideia-chave

AI Gateway saudável expõe intenção de uso, não marca/modelo. Isso protege o produto contra mudanças de custo, provider, disponibilidade e estratégia técnica.

## Complemento — Versionar capacidades quando o comportamento muda

Uma capacidade deve ter contrato observável: entrada permitida, saída, limites, nível mínimo de qualidade e tratamento de falha. Se a mudança de modelo altera esse contrato, considere publicar uma nova versão ou fazer rollout gradual com avaliações, mesmo que o nome HTTP possa permanecer igual.

Nomes de tarefas como `support-ticket-classifier` ajudam a comunicar intenção. Nomes de níveis como `chat-rapido` também podem ser úteis quando o contrato publicado descreve custo, latência e qualidade desse nível. O problema é usar um rótulo sem critérios verificáveis.

Embeddings precisam de cuidado adicional: trocar o modelo pode alterar o espaço vetorial, mesmo com a mesma dimensão. A mudança exige planejar versionamento e reindexação dos documentos; a interface normalizada não garante comparabilidade entre vetores de modelos distintos.

**Conexão com cache:** a chave precisa acompanhar versão da capacidade, prompt e implementação quando esses fatores afetam a resposta. Veja [05 — Cache](../../05-cache/README.md).
