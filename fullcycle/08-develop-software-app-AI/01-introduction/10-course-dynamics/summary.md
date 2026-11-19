## Dinâmica pedagógica baseada em evolução de projetos
Projetos práticos podem começar do zero ou partir de um codebase legado, porque esses dois cenários exigem decisões diferentes de contexto, leitura, refatoração e delegação para agentes. O ganho pedagógico está em acompanhar a evolução do mesmo tipo de problema sob níveis distintos de complexidade operacional. Em um projeto novo, a ênfase recai sobre estruturação inicial; em um projeto existente, o desafio passa a ser interpretar restrições, preservar coerência e intervir sem degradar o sistema.

## Escolha de modelos por tarefa, custo e latência
A seleção de modelos não deve ser uniforme ao longo do workflow. Planejamento, execução, correção de bugs e geração de mensagens de commit têm perfis diferentes de raciocínio, velocidade e custo, então a escolha precisa considerar criticidade, latência aceitável e orçamento de tokens. Um workflow maduro usa modelos mais caros onde o erro custa mais e modelos mais baratos onde o volume é alto e a exigência cognitiva é menor.

## Comandos, plugins e adaptação ao projeto
Comandos simples resolvem tarefas recorrentes do dia a dia e reduzem atrito operacional, enquanto plugins encapsulam capacidades mais estruturadas e reutilizáveis. Retomando o uso de plugins e MCP já estabelecido, o avanço aqui está em deixar de apenas consumir integrações prontas e passar a construir extensões alinhadas ao contexto real da empresa ou do produto. Esse passo transforma automação genérica em capacidade específica do projeto.

## Melhoria incremental da taxa de acerto dos agentes
A taxa de acerto dos agentes melhora quando o projeto acumula contexto operacional útil, e não apenas quando o modelo é trocado. Pequenos ajustes de instrução, organização de contexto, artefatos auxiliares e especialização por tarefa reduzem tempo desperdiçado em tentativas desnecessárias. O efeito prático é simples: problemas que antes exigiam vários minutos de exploração passam a ser resolvidos rapidamente porque o agente deixa de operar no escuro.

## Skills orientados ao codebase
Skills permitem carregar conhecimento especializado apenas quando a tarefa exige, evitando que o agente precise reler o codebase inteiro a cada execução. Quando um skill é construído a partir das convenções, estruturas e padrões do próprio projeto, ele passa a funcionar como uma camada de memória operacional reutilizável. Isso aumenta consistência de execução e reduz o custo de contexto em tarefas específicas.

## Debugging como prática recorrente
Debugging continua sendo uma atividade central mesmo em workflows altamente automatizados, porque bugs surgem em qualquer nível de maturidade do processo. Retomando as ferramentas híbridas já vistas, o ponto novo é tratar estratégias de investigação como parte explícita do trabalho com IA: observar comportamento, testar hipóteses, reproduzir falhas e usar a ferramenta adequada para encurtar o ciclo de diagnóstico. Sem esse método, a automação apenas acelera tentativas mal direcionadas.

## Equilíbrio na geração de testes automatizados
Testes automatizados gerados por IA precisam de critério, porque quantidade não equivale a cobertura útil. Um agente pode produzir centenas ou milhares de testes triviais se a instrução não delimitar o que deve ser validado, como aconteceu no exemplo de componentes React com geração excessiva. O objetivo correto é equilibrar testes básicos, cenários de regressão e edge cases, evitando tanto o excesso de testes irrelevantes quanto a ausência de verificações que realmente protegem o sistema.

## Commit, pull request e revisão inicial com IA
Commit, pull request e code review inicial podem ser delegados à IA quando o projeto já possui contexto suficiente para descrever mudanças com precisão. O benefício não é evitar um `git add`, mas eliminar o trabalho repetitivo de reconstruir manualmente a narrativa técnica de vários arquivos alterados. A automação aqui aumenta rastreabilidade e velocidade, desde que o desenvolvedor continue validando a qualidade do que foi sintetizado.

## Subagentes com janelas de contexto próprias
Subagentes são agentes especializados que operam com contextos separados, o que reduz interferência entre tarefas e prolonga a capacidade de execução útil. Em vez de concentrar tudo em uma única conversa saturada, o workflow distribui frentes de trabalho para unidades menores e mais focadas. Isso permite manter a IA programando por mais tempo com menos degradação de desempenho contextual.

## Progressão de workflows básicos para workflows avançados
Um workflow básico já sustenta tarefas simples do dia a dia, mas começa a mostrar limites quando o projeto exige robustez, coordenação entre etapas e paralelização real. O avanço para workflows mais sofisticados não é cosmético; ele reorganiza como tarefas são quebradas, delegadas, monitoradas e consolidadas. Esse é o ponto em que o processo deixa de ser apenas assistido por IA e passa a ser estruturado para operar com agentes de forma contínua.

## Loop agents para tarefas longas
Loop agents executam ciclos sucessivos dentro de um workflow até concluir uma tarefa, atingir um critério de parada ou esgotar o que conseguem resolver. Eles são úteis em trabalhos longos porque eliminam a necessidade de confirmação manual a cada passo intermediário. O resultado esperado não é perfeição autônoma, mas avanço substancial sem supervisão contínua, como deixar uma execução rodando durante a noite e revisar o estado pela manhã.

## Execução paralela e remota
Retomando a paralelização já discutida, a camada nova está em operar múltiplas features simultaneamente no mesmo codebase com agentes independentes e execução remota. Quando o workflow está bem organizado, disparar, acompanhar e coordenar tarefas pelo celular vira apenas uma superfície de controle, não uma limitação técnica. A mobilidade só funciona porque o processo, o ambiente e os checkpoints já foram preparados para isso.