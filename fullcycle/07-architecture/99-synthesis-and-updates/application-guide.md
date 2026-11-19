# Aplicação atual: contratos, qualidade e controles

[Índice da revisão](README.md) · Referências consultadas em **19/11/2026**.
As recomendações abaixo são complementos de engenharia ao material, com escopo indicado;
não são resultados de benchmarks ou certificação de produtos.

## 1. Acoplamento: use medidas para investigar uma mudança

`Ca`, `Ce`, `I`, `A` e `D` resumem um grafo e uma convenção de contagem. Antes de comparar
runs, fixe unidade, arquivos incluídos, tratamento de tipos e versão do analisador. Preserve
comportamento e teste uma mudança representativa do domínio. Um gráfico melhor após mover
pastas pode refletir apenas uma mudança de medição.

Use métricas junto de ciclos, dependências que atravessam fronteiras e esforço real de
alteração. A hipótese útil é concreta: “esta regra exige carregar infraestrutura para ser
testada” ou “trocar o provider altera o caso de uso”. A refatoração precisa demonstrar que
reduziu esse problema, sem acumular interfaces decorativas.

## 2. Gateway: defina a capacidade e avalie a rota alternativa

Um alias deve representar um contrato: entradas aceitas, saída, prazo, qualidade mínima e
modo de falha. Primário e backup precisam ser avaliados com exemplos comparáveis. Uma
resposta tecnicamente válida pode continuar sendo inadequada para a tarefa.

Configure tentativas e deadline considerando todas as camadas. A mecânica de
[fallback do LiteLLM](https://docs.litellm.ai/docs/proxy/reliability) não transforma um modelo
alternativo em equivalente de negócio. Registre também o deployment efetivo e custo por
resultado aceito. Respostas parcialmente publicadas precisam de uma regra própria de
reinício, sem juntar silenciosamente gerações de dois providers.

## 3. Fluxo: complete o trabalho, não apenas a conexão

Streaming melhora entrega progressiva quando os fragmentos têm valor. Jobs duráveis resolvem
continuidade após desconexão/restart. As escolhas podem coexistir: um job persiste o trabalho
e envia progresso por um canal incremental.

O [SSE do padrão HTML](https://html.spec.whatwg.org/multipage/server-sent-events.html) define
formato e reconexão; a aplicação decide retenção e replay. Um evento final deve distinguir
conclusão, falha e cancelamento. Para ações com efeito, status e reconciliação importam mais
que simplesmente repetir uma requisição interrompida.

## 4. Cache: reutilização exige equivalência e validade

Registre origem e versão da resposta, escopo de acesso, validade dos dados, contrato e
qualidade mínima para escrita. Um hit também precisa respeitar esses critérios. Relevância
geométrica é somente um sinal para selecionar candidatos.

Ao calibrar, inclua paráfrases equivalentes e casos perigosamente parecidos: negação, mudança
de plano, versão, autorização e estado de uma ação. Meça erro entre as reutilizações e custo
líquido, além da taxa de hits. Trocar o modelo de embeddings pede reavaliação do índice e
do limiar, mesmo quando as dimensões coincidem.

## 5. RAG: busque evidência autorizada e avalie o pipeline por partes

Verifique ingestão, recuperação, seleção e geração separadamente. O dado precisa ser
pertinente à pergunta e permitido ao usuário. Filtros fixos de demonstração não substituem
identidade e escopo derivados de autenticação na aplicação real.

A [documentação do pgvector](https://github.com/pgvector/pgvector#filtering) descreve o impacto
de filtros em índices aproximados e alternativas de configuração. Experimente busca exata,
vetorial e seleção de candidatos de forma controlada. Reranking não recupera uma evidência
que não chegou à sua entrada. Para termos literais, avalie uma estratégia complementar
sem presumir que toda consulta precisa de uma arquitetura mais complexa.

## 6. Observabilidade: observe com limites de dados e de custo

Defina atributos operacionais com propósito. Pergunta, hash, request ID ou tenant com muitos
valores não devem entrar indiscriminadamente como labels de métricas. Use correlação em
traces/logs e agregação para métricas, com escopo de acesso e retenção claros.

Head sampling probabilístico não garante guardar todo erro posterior. Decisões por resultado
precisam de outra estratégia, infraestrutura e orçamento. Confira também o que exporters e
instrumentações capturam automaticamente. As referências de
[privacidade](https://opentelemetry.io/docs/security/handling-sensitive-data/) e
[sampling](https://opentelemetry.io/docs/concepts/sampling/) ajudam a comparar o desenho com
a implementação, sem atribuir ao padrão uma política que o código não configurou.

## 7. Evaluation: o juiz também precisa de teste

Separe falha de contrato, ausência de evidência e preferência semântica. Calibre a rubrica
com casos conhecidos e mantenha casos fora do ajuste. Não compare scores produzidos por
juízes ou escalas diferentes como se estivessem na mesma régua.

Fixe dataset, modelo, prompt, política e evaluator. Uma resposta que vence pairwise ainda
precisa atender aos limites absolutos do produto. Os
[conceitos atuais de evaluation do LangSmith](https://docs.langchain.com/langsmith/evaluation-concepts)
incluem avaliação offline/online e diferentes tipos de avaliador; a escolha depende da
propriedade que você quer demonstrar.

## 8. Segurança: confiança na origem, acesso e ação são decisões distintas

A aplicação decide quem pode fornecer conhecimento, quem pode recebê-lo e quais ações
podem ser executadas. Um documento não pode ampliar a própria confiança ou as permissões
do caller. Uma tool call é uma proposta que precisa passar pelo contrato de autorização.

A [orientação da OWASP](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
é compatível com defesa em camadas: reduzir o alcance de entradas adversariais e limitar
o efeito de decisões indevidas. Um filtro textual ou instrução de sistema isolada não
certifica proteção completa.

No projeto local de Segurança, proveniência autoriza roots controladas pela aplicação.
Isso bloqueia fixtures externas no estado atual, sem resolver comprometimento da própria
origem autorizada. As capturas antigas de baseline e o código atual devem ser comparados
por perfil e revisão; não reutilize o resultado de um para declarar eficácia do outro.

## Como decidir o próximo investimento

Comece pela falha observada mais cara. Se falta evidência, melhorar o prompt pode não ajudar.
Se a evidência existe mas é inacessível ao usuário, a resposta deve respeitar esse limite.
Se a resposta está correta e chega tarde, investigue tempo por etapa e contrato de entrega.
Se o sistema funciona mas ninguém consegue reproduzir o resultado, fixe versões e registre
a execução antes de aumentar a complexidade.
