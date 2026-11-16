00:00
Olá pessoal, tudo bem?
00:02
No vídeo anterior a gente começou a avaliar a resposta final usando métricas de RAG, tá?
00:06
A ideia foi sair de uma avaliação puramente manual e
00:10
começar a medir coisas como relação entre resposta, pergunta,
00:14
contexto usado e etc, tá?
00:16
Agora a gente vai falar de uma técnica muito comum em sistemas com IA,
00:20
que é usar um modelo para julgar a resposta de outro modelo.
00:24
Isso normalmente aparece com o nome de LLMSA Judge.
00:28
A ideia parece simples. Você tem uma pergunta,
00:32
uma resposta gerada pela aplicação, talvez um contexto,
00:36
talvez uma resposta de referência,
00:38
e pede para o outro modelo avaliar se aquela resposta está boa.
00:42
Só que aqui que mora um cuidado importante.
00:45
Um judge não é a fonte absoluta da verdade.
00:48
Ele é mais uma ferramenta dentro do processo de evaluation.
00:52
Se você simplesmente manda o modelo essa resposta está boa,
00:57
e aceita qualquer nota que ele der,
00:59
você não criou uma avaliação confiável, você criou uma opinião automatizada.
01:03
Para um LLM as a judge funcionar, ele precisa de uma rubrica.
01:08
Rubrica é um conjunto de critérios que o juiz, o judge, deve usar para avaliar.
01:14
Em vez de pedir uma nota genérica,
01:17
a gente define dimensões mais claras. Por exemplo, relevância, completude,
01:22
groundedness, clareza e o uso correto das fontes.
01:27
Relevância responde. A resposta realmente trata a pergunta.
01:31
Completude responde. A resposta cobre as partes importantes da pergunta.
01:35
O groundedness, ele responde.
01:37
A resposta está sendo sustentada pelo contexto fornecido.
01:41
Clareza responde. A resposta está compreensível para o usuário.
01:45
O uso de fontes responde. As fontes citadas realmente sustentam aquilo que foi dito.
01:50
Percebe a diferença? A gente não está mais perguntando,
01:53
ficou bom. A gente está dizendo para o judge.
01:56
O que significa bom naquele contexto. E isso muda bastante.
02:01
Também é importante pedir uma saída estruturada. Se o juiz devolve um texto livre,
02:06
fica difícil comparar os resultados.
02:09
O ideal é ele retornar algo como score, pass ou fail.
02:13
A razão da nota e talvez notas separadas por critério.
02:17
Por exemplo, um juiz pode retornar... O score geral,
02:21
0 .82. O groundedness, ele pode retornar 0 .9.
02:26
A relevância, 0 .8. Completude, 0 .7. Passou? Sim.
02:32
Motivo? A resposta está correta, baseada no contexto,
02:35
mas deixou de mencionar uma condição importante.
02:38
Então, isso transforma uma avaliação subjetiva em algo mais mensurável.
02:43
Mas, ainda assim...
02:45
Existem riscos, tá? Um juiz pode favorecer respostas mais longas,
02:49
pode preferir um estilo específico de escrita,
02:52
pode ser influenciado pela ordem das opções quando compara duas respostas,
02:57
pode ser mais tolerante com o erro dependendo do prompt que foi escrito,
03:01
ele pode dar notas diferentes se a rubrica não for clara e, em alguns casos,
03:06
pode ser enganado por uma resposta bem escrita,
03:09
mas errada. Então a gente precisa calibrar. Calibrar...
03:13
Significa testar se o judge está se comportando de acordo com o que a gente espera.
03:18
Uma forma simples de fazer isso é pegar alguns exemplos conhecidos.
03:23
Caso em que você sabe que a resposta é boa,
03:27
casos em que você sabe que a resposta é ruim,
03:31
casos parcialmente corretos e casos que deveriam ser recusados.
03:35
Aí você roda o judge e vê se ele dá notas coerentes.
03:39
Se uma resposta claramente errada recebe nota alta,
03:41
a rubrica precisa melhorar. Se uma resposta correta recebe nota baixa,
03:45
porque foi curta,
03:46
talvez o judge esteja confundindo completude com tamanho.
03:50
Se o juiz sempre aprova respostas que citam qualquer fonte,
03:54
talvez você precise deixar claro que a fonte precisa sustentar a conclusão,
03:58
não apenas estar relacionada ao tema.
04:01
Outra prática importante é combinar evaluators.
04:04
Nem tudo precisa passar pelo judge.
04:06
Se eu consigo validar com código que hasAnswer é igual a falso,
04:10
eu não preciso ter sources e eu uso o código.
04:12
Se eu consigo validar que a fonte veio de
04:15
um arquivo aceito e eu uso só um evaluator determinístico,
04:20
por exemplo. Se eu consigo validar que os termos obrigatórios apareceram,
04:23
também eu posso usar código. Então, eu deixo o judge para aquilo que é mais...
04:29
A resposta está fundamentada, ela está completa, ela está clara,
04:33
ela está alinhada com a pergunta.
04:35
Então, essa combinação é muito saudável. Também dá para usar a comparação par a par,
04:41
o pairwise. Em vez de você pedir para o juiz dar uma nota absoluta,
04:45
você mostra duas respostas e a pergunta qual é a melhor base na rubrica.
04:51
Isso é útil quando você quer comparar duas versões do pipeline.
04:55
O modelo A contra o modelo B. O prompt antigo contra o prompt novo,
05:00
com re-ranking e contra sem re-ranking, por exemplo. Mas, mesmo assim,
05:05
o resultado precisa ser tratado como sinal e não como verdade absoluta.
05:11
Em sistemas críticos,
05:12
a avaliação humana continua importante.
05:14
O judge pode ajudar a priorizar casos, encontrar regressões,
05:18
medir tendência e reduzir o trabalho anual. Mas dependendo do risco do domínio,
05:23
ainda faz sentido ter revisão humana em amostras,
05:26
casos de baixa confiança ou mudanças grandes no pipeline.
05:30
No nosso projeto, a gente vai usar o LLMS Judge de forma controlada.
05:34
A ideia não é substituir as avaliações que a gente já fez.
05:37
A gente já tem testes de contrato e avaliação por componente e métricas de reg. Agora,
05:43
a gente vai adicionar uma camada para avaliar a resposta
05:45
final com uma rubrica clara e saída estruturada.
05:50
O Judge vai receber a pergunta, a resposta,
05:53
as fontes e o contexto usado. Ele não vai acessar a base inteira.
05:57
Ele vai julgar apenas aquilo que foi produzido naquela execução.
06:00
E isso é importante. O Judge avalia a evidência apresentada,
06:04
não adivinha o que deveria existir ali no sistema. Então,
06:08
guarda essa ideia. LLMS Judge é útil, mas precisa de rubrica,
06:12
estrutura e calibração. Ele não substitui testes determinísticos,
06:17
ele não substitui métricas específicas e não substitui
06:20
revisão humana quando o risco é alto.
06:22
E aí, no próximo vídeo, a gente vai implementar isso na prática. Então, vamos nessa!