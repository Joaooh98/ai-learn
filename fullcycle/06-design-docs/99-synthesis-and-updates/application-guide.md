# Documentação útil para pessoas e ferramentas de IA

[Índice da revisão](README.md) · Fontes consultadas em **19/11/2026**.

## Escolha o menor conjunto que fecha as decisões

| Necessidade | Artefato possível | Conteúdo essencial |
|---|---|---|
| Alinhar valor e escopo | PRD ou issue detalhada | Problema, público, métricas, restrições e exclusões |
| Explicar estrutura | HLD com diagramas | Limites, responsabilidades, integrações e cenários de falha |
| Discutir alternativas | RFC | Opções reais, critérios, riscos e questões abertas |
| Preservar uma decisão | ADR | Contexto, escolha, consequências, status e revisão |
| Implementar uma feature | FDD/contrato | Entradas, efeitos, saídas, autorização, falhas e testes |
| Operar e recuperar | Runbook | Sintoma, diagnóstico, ação, verificação e retorno seguro |

Essa tabela é uma proposta para aplicar a taxonomia do curso, sem impor sequência rígida.
Uma alteração pequena pode caber em um único registro. Uma mudança de autenticação,
consistência ou contrato entre times exige mais profundidade porque o custo de erro aumenta.

## Quatro referências que complementam os quadros

O [C4](https://c4model.com/diagrams/container) ajuda a descrever estrutura e comunicação,
e distingue aplicação/armazenamento de unidade de deploy. O
[arc42](https://arc42.org/overview/) oferece um roteiro adaptável de contexto, vistas,
decisões e requisitos de qualidade. O [MADR](https://adr.github.io/madr/) dá forma a uma
decisão individual. O [Diátaxis](https://diataxis.fr/) organiza a documentação conforme a
necessidade de aprender, executar uma tarefa, consultar ou compreender. Use cada referência
para a pergunta correspondente, sem tratá-las como concorrentes.

Essas práticas são referências mantidas e consultadas na data acima, não novidades inventadas
para esta revisão nem prova de adoção por todo o mercado.

## Documentos como código, com uma fonte canônica

A proposta de [docs as code](https://www.writethedocs.org/guide/docs-as-code/) aproxima texto
e código por controle de versão, revisão e verificações. No projeto do curso, isso pode
significar Markdown próximo da implementação, links verificáveis e exemplos executáveis.

Não mantenha manualmente versões Markdown e JSON da mesma informação sem definir qual é
a origem. Gere a representação secundária ou valide equivalência para evitar divergência.
Para APIs HTTP, [OpenAPI](https://spec.openapis.org/oas/latest.html) torna o contrato legível
por ferramentas. Escolha uma versão aceita pelos validadores e geradores usados no projeto;
publicar uma versão mais nova não garante suporte em toda a cadeia.

## IA com proveniência e limites claros

Uma síntese de reunião pode confundir sugestão com decisão e uma busca pode trazer contexto
sem validade para sua versão. Classifique cada afirmação relevante como observada, decidida,
proposta ou pendente. Registre onde verificar: arquivo/commit, trecho da transcrição ou fonte
primária. Uma referência só ajuda quando sustenta exatamente a afirmação associada.

Não use o documento para descrever como implementado algo que está apenas planejado. Antes
de aceitar uma atualização gerada por IA, confira caminhos, contratos e efeitos no código.
Para metas de qualidade, exija cenário de medição: ambiente, volume, distribuição, percentil,
janela e condição de falha. “Baixa latência” sem esse contexto não é critério de aceite.

## Como manter a revisão proporcional

Inclua dono, status e referência do estado do sistema; mantenha histórico de decisões em vez
de apagar a justificativa anterior. Quando uma decisão for substituída, aponte a sucessora.
Revise os documentos afetados na mesma mudança do contrato ou comportamento.

Verificação de links detecta referências quebradas; revisão de schema detecta formato;
execução de exemplos detecta parte das divergências de comportamento. Nenhuma dessas
verificações isoladamente demonstra que um requisito atende a necessidade do usuário.
Use leitura crítica para completar o ciclo.

## Perguntas para revisar o FDD do rate limiter

- O limite é por usuário, tenant, rota ou combinação? Qual a origem confiável da identidade?
- Qual estratégia foi escolhida? O PRD e o HLD contam a mesma história?
- O que é compartilhado entre réplicas? O modo em memória preserva qual garantia?
- Como a decisão reage a timeout, partição, repetição e reinício?
- Qual condição permite degradação e como o operador identifica sua ativação?
- As respostas de bloqueio informam comportamento e unidade de tempo ao consumidor?
- Qual cenário concorrente demonstra que a quota não foi ultrapassada?

As respostas fecham a ponte entre o diagrama e a implementação. Sem elas, acrescentar mais
seções não resolve a ambiguidade.
