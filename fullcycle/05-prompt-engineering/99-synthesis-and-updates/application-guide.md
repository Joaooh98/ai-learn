# Da técnica de prompt ao comportamento verificável

[Índice da revisão](README.md) · Fontes consultadas em **19/11/2026**.

## 1. Escolha a técnica pela falha que precisa resolver

| Dificuldade observada | Intervenção inicial | Evidência para comparar |
|---|---|---|
| Saída inconsistente | Schema e validação | Taxa de respostas válidas e campos ausentes |
| Critério de decisão ambíguo | Exemplos positivos e negativos | FP/FN nas classes afetadas |
| Pedido incompleto | Esclarecimento dos campos realmente necessários | Quantidade de interações e sucesso da tarefa |
| Etapas com contratos diferentes | Workflow com validação entre etapas | Erros por etapa e custo total |
| Resposta desatualizada | Recuperação de fonte verificável | Evidência recuperada e fidelidade às fontes |
| Ação exige autorização | Controle no serviço/ferramenta | Testes de acesso permitido e negado |

Isso é uma proposta de aplicação ao conteúdo local, não um ranking universal de técnicas.
Role prompting ajuda a estabelecer perspectiva, mas o modelo não recebe uma qualificação
real por assumir uma persona. Few-shot é aprendizado em contexto; não altera os pesos.

## 2. CoT, ToT, SoT e ReAct precisam de uma implementação coerente

Os scripts do capítulo 1 demonstram instruções associadas a essas técnicas. Pedir que a
resposta tenha ramos não implementa, por si só, um algoritmo de busca em árvore. Pedir um
esqueleto não prova execução paralela. Imprimir `Action` e `Observation` não demonstra que
uma ferramenta real foi executada. Para cada exemplo, diferencie formato solicitado,
controle exercido pelo código e ação externa efetivamente realizada.

Modelos de raciocínio podem funcionar melhor com objetivo e restrições diretos, sem pedir
exposição de passos internos. Use verificações externas e justificativas curtas da resposta,
conforme as [boas práticas oficiais para raciocínio](https://developers.openai.com/api/docs/guides/reasoning-best-practices).

Na aplicação, registre decisões, evidências e resultados de ferramentas. Eles permitem
verificar o trabalho sem depender de uma narrativa gerada sobre como o modelo chegou à saída.

## 3. Contexto útil tem origem e orçamento

`6-prompt-enriquecido/1-ITER_RETGEN.py` cria rascunho, identifica lacunas e pede ao próprio LLM
informações para preenchê-las. A leitura do arquivo não mostra consulta a um retriever ou
fonte externa: `query_chain` é outra chamada ao mesmo modelo. Logo, preencher marcadores
`[MISSING: ...]` mede progresso textual, não comprova aquisição de fatos.

Para estudar retrieval iterativo de fato, proponha este fluxo: gerar consulta, recuperar fonte,
registrar documento/página, revisar a resposta e verificar se a nova evidência resolve a lacuna.
Pare quando atingir o orçamento de consultas/tempo ou quando a evidência deixar de melhorar.
Nunca force o preenchimento de um fato que continua desconhecido.

`2-query-enrichment.py` demonstra coleta de seis campos de um PR. Em uma aplicação real,
alguns deles podem estar no repositório ou na sessão. Pergunte somente o que não estiver
disponível e o que possa alterar a execução. Dados recuperados continuam sujeitos a validação
e controle de acesso.

## 4. Workflow previsível e agente com autonomia têm custos diferentes

Se as etapas são conhecidas, expresse a sequência no código e valide as transições. Reserve
a escolha dinâmica de ferramentas para problemas em que essa flexibilidade melhora resultados.
A [distinção de workflows e agentes da Anthropic](https://www.anthropic.com/research/building-effective-agents)
é útil para interpretar os exercícios, embora o próprio artigo registre que ferramentas
mudaram desde sua publicação original.

Um code reviewer que apenas lê um diff precisa de permissões diferentes de um agente que
cria branches ou publica PRs. Nas ferramentas, controle os recursos acessíveis, valide
argumentos e defina o tratamento de erro. A instrução textual não substitui esses controles.

## 5. Versione o experimento inteiro

Um identificador legível como `reviewer-v2` ajuda a navegar, mas pode apontar para conteúdo
mutável. Registre a revisão imutável do prompt, o hash do dataset, o commit do código,
o modelo de geração e o evaluator, inclusive prompt/modelo do juiz. Promova uma configuração
avaliada e mantenha possibilidade de retorno à anterior.

A documentação atual concentra a gestão programática no
[SDK do LangSmith](https://docs.langchain.com/langsmith/manage-prompts-programmatically).
Os capítulos locais usam combinações de LangChain `0.3.x` e `1.0.0a5`: são ambientes
históricos distintos. Consulte o [guia de migração v1](https://docs.langchain.com/oss/python/migrate/langchain-v1)
antes de modernizar imports e dependências; não misture um trecho da documentação atual
com um ambiente antigo presumindo compatibilidade. Esta revisão não atualizou pacotes.

## 6. Schema, validade semântica e qualidade são verificações separadas

Uma resposta pode ser JSON válido e apontar uma linha inexistente. Outra pode identificar
um bug real com severidade discutível. Meça pelo menos três níveis: formato, correspondência
com a referência e utilidade da conclusão. Use enumerações e campos obrigatórios onde houver
contrato, e valide invariantes de negócio em código. A API atual de
[structured output do LangChain](https://docs.langchain.com/oss/python/langchain/structured-output)
distingue estratégias do provider e de tool calling; suporte depende da integração.

No helper pairwise local, texto inválido pode virar empate ou até vitória por conter as letras
A/B. Ao evoluir o exercício, guarde `winner`, versão da rubrica e status de parsing. Faça uma
amostra de revisão humana antes de confiar na preferência agregada.

## 7. Plataforma é uma decisão operacional

As notas antigas não devem ser lidas como comparação comercial atual. Existe
[documentação de LangSmith self-hosted](https://docs.langchain.com/langsmith/self-hosted);
portanto “cloud only” não é uma propriedade geral do produto. O
[Langfuse documenta avaliação online e offline](https://langfuse.com/docs/evaluation/overview).
Disponibilidade de funcionalidades, licença e contratação devem ser conferidas para a edição
e versão pretendidas. Não há base aqui para declarar um vencedor universal ou preço garantido.

Para escolher, faça uma prova pequena: mesmo dataset, mesmo gerador e mesma política de
retenção. Verifique exportação, proteção de conteúdo sensível, controle de acesso, integração
com o pipeline e custo de operação. Evite duplicar conteúdo de produção em duas plataformas
sem uma razão explícita.

## Exercício de consolidação

1. Separe exemplos de desenvolvimento, validação e teste para um code reviewer.
2. Defina se o acerto exige tipo, severidade e localização; registre a política de denominador zero.
3. Compare baseline, few-shot e uma variante de contexto com o mesmo orçamento.
4. Conte falhas de formato separadamente de respostas válidas sem findings.
5. Compare por severidade e dificuldade; inspecione cada regressão crítica.
6. Registre custos, latência, versões e erros; escreva uma decisão de promoção ou rejeição.

Não há metas numéricas universais neste exercício. Escolha limites conforme o custo dos
falsos alertas, das falhas não detectadas e da operação pretendida.
