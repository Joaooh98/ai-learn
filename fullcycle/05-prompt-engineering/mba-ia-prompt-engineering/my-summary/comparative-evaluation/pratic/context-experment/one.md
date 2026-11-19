## Pull de prompts e escolha entre remoto e local
`pull prompt` carrega do LangSmith uma versão já registrada do prompt, em vez de manter o texto apenas no código local. Isso permite versionamento, reaproveitamento por API e rastreabilidade entre execuções, o que é especialmente útil quando prompt A e prompt B evoluem ao longo de vários experimentos. Retomando o cenário de comparação entre prompts, aqui A e B vêm do repositório remoto, enquanto o juiz permanece local; essa combinação mostra que geração e julgamento não precisam usar a mesma estratégia de armazenamento. Se quiser centralizar tudo, o prompt do juiz também pode ser criado remotamente e recuperado depois por API.

## Funções separadas para gerar A e B
O exemplo usa uma função para executar A e outra para B, ambas com o mesmo contrato de entrada. Também seria possível parametrizar uma função compartilhada pelo prompt. O desenho procura isolar o efeito da instrução, mantendo dataset, modelo e demais configurações sob controle. Para atribuir as diferenças à mudança, fixe as versões e repita as execuções, considerando a variabilidade da geração.

## Criação do pairwise evaluator com juiz
O pairwise evaluator é instanciado a partir do template do judge e da conexão com o modelo que fará o julgamento. Como o método pairwise já foi definido anteriormente, o ponto novo aqui é operacional: o juiz recebe as duas saídas geradas e executa a terceira chamada do fluxo, produzindo a comparação dentro do LangSmith. O template do juiz concentra as regras de decisão, e por isso ele determina como a preferência será computada, inclusive quando há ranqueamento por pontos. Se o critério estiver mal especificado, o experimento continua executando, mas a auditoria posterior perde valor.

## Ordem real da execução
A execução completa ocorre em três blocos: primeiro roda o prompt A sobre o dataset, depois o prompt B sobre o mesmo conjunto de exemplos e, por fim, o evaluator compara os pares de respostas. Essa ordem importa porque o experimento pairwise no LangSmith referencia os nomes dos dois experimentos já concluídos para montar a comparação. Na prática, o código captura o nome retornado por cada run e o reaproveita na etapa comparativa. Sem esse encadeamento explícito, o sistema não sabe quais execuções devem ser confrontadas.

## Prefixo e concorrência como parâmetros operacionais
O prefixo nomeia o experimento de forma legível e ajuda a localizar runs relacionadas no painel, principalmente quando você repete o teste várias vezes após alterar o prompt. Já a concorrência controla quantas execuções podem ocorrer em paralelo, afetando tempo total, pressão sobre a API e previsibilidade de custo. Esses parâmetros não mudam a lógica do julgamento, mas mudam a operabilidade do experimento. Em ambiente de iteração rápida, nomear bem e ajustar concorrência evita confusão entre versões e gargalos desnecessários.

## Verificação do dataset antes do run
Antes de executar, vale confirmar que o dataset existe, está no projeto correto e contém a quantidade esperada de samples. No exemplo, a checagem mostra um dataset pairwise com 10 registros e ainda sem experimentos associados, o que valida o ponto de partida antes de consumir tokens. Essa verificação simples evita dois erros comuns: rodar contra o dataset errado e interpretar resultados de um experimento anterior como se fossem da execução atual. Em avaliação comparativa, esse tipo de erro compromete a leitura inteira do teste.

## Redução de custo removendo evaluators extras
Evaluators redundantes podem ser removidos quando seu resultado não participa da decisão, reduzindo chamadas e custo. Preserve verificações absolutas relevantes, como formato válido, correção e ausência de violações de segurança: uma resposta pode vencer a comparação relativa e ainda falhar nesses requisitos. Reaproveite saídas armazenadas para evitar novas gerações quando o objetivo for somente revisar o julgamento.

## Leitura do placar agregado no LangSmith
Depois da execução, o LangSmith cria um experimento de comparação com placar agregado, como vitória de A por 5,5 contra 4,5. Esse número depende da regra embutida no prompt do juiz, que pode atribuir pontos em vez de apenas contar vitórias simples. O painel oferece uma leitura rápida de quem venceu no conjunto, mas esse resumo só é confiável quando você entende a política de pontuação usada pelo judge. Sem essa leitura do critério, o placar vira um número opaco.

## Inspeção por registro e auditoria do julgamento
O valor prático do pairwise aparece quando você abre cada registro e verifica quem venceu caso a caso. O painel marca visualmente vitórias e derrotas, e o detalhamento mostra o input original, a linguagem, a saída da versão A e a saída da versão B. Isso permite depurar decisões concretas: por exemplo, um lado apontou `command injection`, o outro `missing output validation`, e o juiz precisou decidir qual resposta era superior para aquele código. A comparação deixa de ser apenas um placar agregado e passa a ser um artefato auditável.

## Trace, API Run e inspeção do prompt do juiz
Ao abrir o trace ou a API Run, você consegue ver exatamente o que foi enviado ao modelo julgador: o prompt completo, as regras, os inputs e o output final. Essa visibilidade é crucial quando o resultado parece estranho, porque permite verificar se o judge recebeu contexto suficiente, se as regras estavam claras e se a resposta vencedora foi escolhida pelos motivos esperados. No exemplo, o trace mostra o texto que instrui o modelo a agir como juiz imparcial e o output final indicando vitória de A. Quando necessário, o próximo refinamento é pedir justificativa textual da decisão para tornar a auditoria ainda mais forte.

---

> Complemento de estudo revisado em 19/11/2026.

## Versão remota, custo e limites da conclusão

Recuperar o prompt pelo nome sem revisão pode selecionar uma versão diferente entre runs.
Fixe o identificador imutável e registre também o juiz. Gere A e B para o mesmo ID de exemplo,
mantenha as respostas para auditoria e compute a comparação apenas quando ambas forem válidas.
A documentação atual recomenda o [SDK do LangSmith para gerenciar prompts](https://docs.langchain.com/langsmith/manage-prompts-programmatically).

Um placar de `5,5 × 4,5` em dez itens é uma preferência pequena na amostra. Sem repetição,
intervalo ou análise dos empates, não sustenta uma decisão geral. Você pode reaproveitar
saídas armazenadas para testar juízes diferentes; uma nova comparação não exige sempre
regenerar A e B. Traces registram os dados instrumentados, sem revelar o raciocínio interno
não exposto pelo modelo.
