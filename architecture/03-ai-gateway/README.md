# 03 — AI Gateways

[Arquitetura](../README.md) · [Anterior: acoplamento e saúde da aplicação](../02-coupling-and-application-health/README.md) · [Próximo: fluxos de chamada](../04-call-flows/README.md)

Este módulo acompanha a evolução de uma chamada direta por SDK até uma interface HTTP compartilhada com nomes lógicos e fallback técnico. O objetivo é reconhecer o que a abstração simplifica e quais garantias ainda precisam ser definidas, implementadas e medidas.

## Roteiro de estudo

| Aula | Assunto | Duração | Resultado de estudo |
|---|---|---|---|
| 01 | [Introdução - Integrações com IA](01-introduction-ai-integrations/README.md) | `03:05` | Identificar decisões duplicadas |
| 02 | [Chamando OpenAI com SDK](02-calling-openai-with-sdk/README.md) | `04:20` | Ler o baseline com SDK nativo |
| 03 | [Adicionando Anthropic como opção](03-adding-anthropic-as-option/README.md) | `04:28` | Distinguir seleção de provider e fallback |
| 04 | [Entendendo AI Gateway](04-understanding-ai-gateway/README.md) | `03:29` | Definir a fronteira do gateway |
| 05 | [Compatibilidade - a primeira capacidade de uma AI Gateway](05-compatibility-first-ai-gateway-capability/README.md) | `03:38` | Separar normalização e equivalência |
| 06 | [LiteLLM como primeira implementação da compatibilidade](06-litellm-first-compatibility-implementation/README.md) | `03:13` | Escolher SDK ou serviço HTTP |
| 07 | [LiteLLM na prática](07-litellm-in-practice/README.md) | `04:59` | Usar uma chamada normalizada |
| 08 | [LiteLLM como Proxy](08-litellm-as-proxy/README.md) | `03:08` | Entender a responsabilidade do proxy |
| 09 | [LiteLLM Proxy - Fluxo da requisição](09-litellm-proxy-request-flow/README.md) | `03:27` | Traçar identidade, limite e destino |
| 10 | [LiteLLM Proxy e Router](10-litellm-proxy-and-router/README.md) | `03:44` | Resolver grupos e deployments |
| 11 | [Expondo capacidades, não modelos físicos](11-exposing-capabilities-not-physical-models/README.md) | `03:28` | Definir contrato por capacidade |
| 12 | [Governança mínima - acesso, custo e limites](12-minimal-governance-access-cost-limits/README.md) | `03:41` | Separar quotas, orçamento e concorrência |
| 13 | [Resiliência - timeout, retry e fallback](13-resilience-timeout-retry-fallback/README.md) | `04:29` | Planejar resiliência com prazo total |
| 14 | [LiteLLM Proxy na prática](14-litellm-proxy-in-practice/README.md) | `07:16` | Montar proxy e client local |
| 15 | [LiteLLM Proxy na prática - parte 2](15-litellm-proxy-in-practice-part-2/README.md) | `03:11` | Executar a integração HTTP |
| 16 | [Adicionando e alternando modelos no Proxy](16-adding-and-switching-models-in-proxy/README.md) | `06:12` | Selecionar nomes lógicos por ambiente |
| 17 | [Fallback técnico](17-technical-fallback/README.md) | `06:32` | Verificar fallback técnico |
| 18 | [Fallback com modelo fraco](18-fallback-with-weak-model/README.md) | `05:38` | Validar contrato depois do fallback |

Leia 01–07 para compatibilidade, 08–13 para responsabilidade operacional e 14–18 para a prática com proxy. Os prompts foram preservados como registros históricos; notas de revisão distinguem o pedido original do código efetivamente presente.

## O que os exemplos implementam

| Exemplo | Implementado | Limite material |
|---|---|---|
| [SDK direto](02-calling-openai-with-sdk/sdk-simple-example/README.md) | OpenAI, prompt e resposta textual | Default do código difere do prompt; não há política explícita de timeout/retry |
| [Dois providers](03-adding-anthropic-as-option/provider-selection-example/README.md) | Seleção por `AI_PROVIDER`, SDKs nativos | Sem fallback; modelos históricos devem ser substituídos por ambiente |
| [LiteLLM SDK](07-litellm-in-practice/provider-selection-example/README.md) | Uma chamada `completion()` | Mantém credenciais e seleção locais; prefixo e provider podem divergir |
| [Proxy inicial](14-litellm-proxy-in-practice/minimal-proxy-client/README.md) / [continuação](15-litellm-proxy-in-practice-part-2/minimal-proxy-client/README.md) | Client HTTP e alias `developer-assistant` | Já executável nas duas pastas; master key compartilhada |
| [Múltiplas capacidades](16-adding-and-switching-models-in-proxy/multi-capability-proxy/README.md) | Dois grupos, um deployment por grupo | Seleção explícita, sem balanceamento entre grupos ou fallback |
| [Fallback técnico](17-technical-fallback/proxy-technical-fallback/README.md) | Alias principal e backup, regra de fallback | Não prova equivalência semântica; retries/timeouts não fixados |
| [Validação de fallback](18-fallback-with-weak-model/weak-model-fallback-validation/README.md) | Parse JSON e categoria permitida | Schema parcial, sem formato estruturado enviado ao provider |

Os Compose dos proxies usam o mesmo nome de container e a porta `4000`: execute um de cada vez. O Python roda no host e usa `localhost:4000`. Em um container cliente, a URL precisa identificar o serviço de proxy na rede utilizada.

As dependências e a imagem `main-stable` não estão fixadas. Registre versões, digest da imagem e configuração ao reproduzir um experimento. O material não inclui evidência de execução paga ou testes reais com todos os providers na revisão documental.

## Compatibilidade e contrato por capacidade

Um alias é a chave de roteamento; um contrato é a definição do comportamento aceito. Para `support-ticket-classifier`, publique entrada, categorias permitidas, campos obrigatórios, limite de contexto, prazo, versão do prompt, regra de falha e critério de qualidade. Depois verifique primário e backup com o mesmo conjunto representativo.

LiteLLM normaliza APIs, mas os parâmetros suportados variam. Por padrão, parâmetros OpenAI não suportados produzem erro; `drop_params` pode removê-los. Não habilite remoção indiscriminada quando o parâmetro faz parte do contrato. [Parâmetros de entrada oficiais](https://docs.litellm.ai/docs/completion/input).

Quando a saída for estruturada, diferencie JSON sintático, aderência ao schema e correção do domínio. A aplicação da aula 18 valida só parte do primeiro/segundo níveis. Nenhuma validação de schema prova que a categoria escolhida representa corretamente o ticket.

Uma troca de modelo pede avaliação de qualidade, custo por resultado aceito e latência p95. Se mudar formato ou semântica, versione a capacidade. Na mudança de embeddings, reavalie compatibilidade do índice: dimensões iguais não tornam dois espaços vetoriais equivalentes.

## Resiliência com orçamento ponta a ponta

Escolha um prazo total por capacidade. Dentro dele cabem tentativas, backoff, fallback e entrega da resposta. Diferencie timeout de conexão, espera de leitura e deadline global; seus efeitos dependem do client e do transporte. LiteLLM também expõe configurações específicas de timeout no proxy. [Referência oficial de timeouts](https://docs.litellm.ai/docs/proxy/timeout).

Os exemplos `OpenAI()` não configuram retry ou timeout. A documentação do SDK consultada registra duas novas tentativas automáticas para certas falhas e timeout padrão de dez minutos; confirme a versão instalada. Esses defaults não equivalem ao prazo de produto. [SDK oficial OpenAI: retries e timeouts](https://github.com/openai/openai-python#retries).

**Exemplo aritmético, não configuração do repositório:** três tentativas do client × três tentativas no gateway × dois destinos podem produzir até 18 tentativas upstream quando as camadas repetem o fluxo completo. Conte tentativas reais, falhas e gasto; estabeleça uma camada responsável e um orçamento compartilhado.

O router realiza retries dentro de um grupo e fallback para outro grupo conforme a política. Uma resposta HTTP válida, porém inútil para o negócio, exige avaliação adicional; failover técnico não faz essa avaliação automaticamente. [Fluxo oficial da requisição](https://docs.litellm.ai/docs/proxy/architecture).

A política também deve dizer quando desistir: resposta de erro, execução posterior, resultado parcial ou cache ainda válido. Timeout local não comprova cancelamento remoto. Para ações externas, defina idempotência e reconciliação antes de repetir. Após publicação de texto em streaming, reiniciar em outro provider requer um contrato que indique substituição ou reinício.

## Governança do laboratório e da operação

`LITELLM_MASTER_KEY` é uma credencial administrativa; os demos a usam para simplificar a autenticação. A operação compartilhada deve identificar consumidores e limitar seus acessos. O fluxo de virtual keys documentado pelo LiteLLM usa PostgreSQL e uma chave administrativa para criar credenciais com escopo. Os Compose desta trilha não montam essa infraestrutura. [Virtual keys oficiais](https://docs.litellm.ai/docs/proxy/virtual_keys).

A separação `OPENAI_API_KEY` no proxy e chave interna no client reduz o acoplamento da chamada. O `.env` compartilhado do laboratório não prova isolamento dos arquivos ou das permissões. Distribua somente os segredos necessários a cada serviço na implantação real.

Registre capacidade solicitada, deployment efetivo, request ID, tentativas, resultado da validação, uso, latência e custo. Evite registrar prompts e respostas integralmente por padrão quando isso não for necessário. O print do alias solicitado não serve como prova de fallback.

Fallbacks, cache e rotas alternativas precisam respeitar o mesmo escopo de acesso e contrato. A master key dos exemplos também pode chamar o alias de backup diretamente; a documentação não o trata como inacessível.

## Conexões com os próximos módulos

- [04 — Fluxos de Chamada](../04-call-flows/README.md): escolher resposta completa, streaming ou job não depende apenas do gateway.
- [05 — Cache](../05-cache/README.md): resultado armazenado precisa acompanhar escopo, versão da capacidade, prompt, dados e política de validade.

**Perguntas para consolidar:** o que acontece se o gateway responde 200 com categoria errada? Como provar qual deployment respondeu? Quanto tempo e gasto uma falha pode consumir? Qual resultado em cache continua válido após trocar o modelo?

## Fontes e critério de revisão

Revisão documental e inspeção dos artefatos em **1 de outubro de 2026**. As referências oficiais ficam junto dos assuntos que sustentam. Modelos, endpoints e configurações mudam; confirme a versão efetivamente usada. As capturas e durações são registros da aula, não evidência de disponibilidade atual de recursos.

O histórico de aposentadoria dos modelos Anthropic está nos READMEs dos exemplos das aulas 03 e 07. Os nomes solicitados em prompts e os defaults divergentes do código foram preservados e identificados; a atualização de execução usa variáveis de ambiente.
