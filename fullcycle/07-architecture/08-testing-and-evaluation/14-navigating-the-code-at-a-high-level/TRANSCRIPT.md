00:00
Olá pessoal, tudo bem? Seguinte, eu quero dar uma passada aqui pra vocês,
00:06
pelo menos nessa parte do Raga,
00:08
somente pra que você tenha uma ideia aqui de código, já que, vamos dizer,
00:12
acaba sendo um framework novo no meio da história,
00:15
tá? Então, seguinte, pra ficar mais fácil,
00:18
normalmente eu costumo mostrar sempre de trás pra frente, né? Então,
00:23
se você olhar aqui... Eu tenho um load cases,
00:26
onde eu vou carregar meus códigos.
00:28
Eu tenho um filtro aqui para saber os casos que eu vou poder responder,
00:32
ou seja, são os casos respondíveis. E eu vou selecionar esses caras aqui.
00:37
Eu verifico se ele está seguindo as políticas, se tem budget,
00:42
se os dados do modelo estão certos e etc.
00:45
E eu tenho aqui o build metrics, aqui para mim também.
00:51
Mas agora o grande ponto aqui é que a gente tem o Run Pipeline, tá?
00:56
E o que acontece no meio dessa história?
01:00
A gente vai rodar o Pipeline, tá? Então esse é o grande ponto,
01:05
falando que a gente vai usar o Rerank e tudo mais.
01:08
Aí a gente vai pegar tudo que pode ser pontuável,
01:13
no final das contas, né? E tudo que a gente pode ter...
01:17
métricas de erro, ou seja, que ele não conseguiu pontuar aí nesse caso.
01:22
Daí a gente vai gerar o report e vai salvar o report,
01:25
basicamente isso. Ou seja, de forma grosseira, ele carrega os casos,
01:30
filtra os respondíveis, roda o pipeline, separa os que têm resposta,
01:35
pontua, salva e daí ele vai imprimir ali na tela,
01:39
ali pra gente, tá? Então esse aí é um ponto importante.
01:42
Agora... Qual trecho aqui que eu acho que é importante que você veja?
01:46
Primeiro aqui, deixa eu buscar, eu devo ter aqui um run,
01:50
pipeline, que
01:53
é esse método aqui, deixa eu pegar esse cara. Então, é o seguinte,
01:56
esse aqui é o pipeline de produção, ele não é uma cópia, entende? Então,
02:03
ele não é uma versão de teste. O mesmo RAG pipeline que a PU usa é esse cara aí.
02:09
Então, se eu me disse uma cópia,
02:10
eu estaria avaliando um sistema que ninguém usa. Então,
02:13
esse aí é o grande ponto importante.
02:17
Então, tudo que você está vendo aqui no final das contas,
02:20
eu estou rodando realmente ali num pipeline aqui.
02:25
Agora, se você começa a olhar,
02:29
eu tenho um outro cara que é chamado de Run for Evaluation.
02:34
Esse cara, Run for Evaluation... o que que esse cara,
02:39
ele acaba fazendo, né? O Ragas,
02:43
ele precisa do texto dos trechos que alimentam a resposta, certo?
02:48
Mas o projeto tem uma regra desde a aula de observabilidade,
02:53
né? O conteúdo do chunk, ele não sai, ele não vai pra API, nem pro trace,
02:58
nem pro nosso log, tá? Então, esse aí é um ponto importante, tá? Então...
03:05
a gente tem que pensar sempre nesse aspecto,
03:08
que eu preciso, na realidade, nesse caso,
03:11
dessas informações para eu fazer a minha avaliação.
03:17
Então, esse aí é um ponto importante.
03:20
E aqui, inclusive, por exemplo, se eu for buscar,
03:23
eu acho que é RAG Pipeline Result, você
03:29
Vai ver que todo o nosso Pipeline Result do...
03:34
Do reg, do pipeline, a gente não traz as informações.
03:38
E por isso aí que é importante para a gente conseguir trabalhar.
03:43
Então, essa que é a ideia principal.
03:48
Porém, se você olhar aqui... Cadê o meu camarada aqui? Run pipeline.
03:54
Se eu olhar aqui, on context. Deixa eu olhar aqui. Context.
04:05
Aqui, case run, selected context,
04:08
Retrieve context, context
04:12
Precision, que são as métricas que eu estou querendo.
04:15
Só estou querendo chegar aqui onde que eu faço encher a minha lista sem passar.
04:20
Porque no final das contas, o que acontece é o seguinte.
04:24
Na realidade, não é no eval rag, é no rag pipeline.
04:28
Aqui, se você olhar aqui, quando eu tenho o run for evaluation,
04:33
Você vai ver que eu rodo a pergunta normal,
04:35
mas no onContext, eu dou um context.extend.
04:39
E o que acontece? Quando eu tenho esse context.extend,
04:43
eu encho aquela minha lista com as...
04:46
com os dados que eu estava precisando,
04:48
mas essas informações não vazam ali para a API.
04:52
Então, isso aí é um ponto importante, porque, inclusive,
04:55
o meu módulo nem tem esse campo.
04:57
Esse cara aqui acaba funcionando como uma callback ali nesse
04:59
caso e acaba resolvendo um pouco a minha vida,
05:02
tá? Agora, um caso que é importante aqui é o nosso build matrix,
05:09
tá? Por quê? Porque o build metrics, o que ele vai fazer?
05:12
Ele vai pegar os dados, o cliente da OpenAI,
05:15
a gente vai configurar o nosso caso aqui, o nosso modelo.
05:21
Eu vou falar qual que é o meu modelo de
05:25
embedding e eu vou retornar quais métricas que eu queria. A faithfulness,
05:30
que inclusive é um objeto aqui que vem do próprio Ragas.
05:35
É o Answer Relevance e o Context Precision Without Reference.
05:40
Perceba que para esses caras funcionarem,
05:42
eu passo qual modelo eu quero utilizar. Por quê? Porque ele vai usar, por exemplo,
05:49
o GPT-X para conseguir fazer essa
05:54
verificação em relação a bater ali no modelo,
05:58
tá? E ele tem um outro cara aqui que é importante vocês verem,
06:01
que é o Score Runs, aqui no final das contas.
06:04
Esse score runs é importante por quê? Porque no final das contas...
06:09
Ah, e antes de eu falar do runs,
06:11
rapidinho, não sei se você viu o context precision lá em cima,
06:14
que é context precision without reference. Por que está without reference?
06:19
Porque a gente não tem a referência do gabarito, da nossa rubrica,
06:23
porque a gente não tem essa informação no dataset.
06:26
Foi exatamente esse caso que eu acabei falando antes,
06:30
nesse tempo, que a gente precisaria ter...
06:34
essa informação para a gente comparar a resposta.
06:38
Como a gente não tem, a gente não tem como trazer essa informação. Então,
06:42
eu falo que a gente tem a precisão, mas sem utilizar a referência.
06:48
E aqui no score run, basicamente, se você olhar,
06:51
eu tenho cada item com um batch score e eu passo as minhas métricas.
06:56
Por quê? Porque ele consegue mandar essa informação ali para mim em batch.
07:01
Se uma métrica falhar, ela vira None. E as outras duas,
07:05
no final das contas, elas acabam continuando. Ou seja,
07:08
perder uma métrica é melhor do que perder a rodada inteira.
07:11
O que ia acabar custando,
07:13
sei lá, seis minutos ali da nossa vida, nossas chamadas, tá?
07:17
Eu acho que esse é o principal ponto em relação a isso.
07:20
Um outro ponto que é interessante é o case run, né?
07:26
Onde eu tenho aqui o meu case run aqui.
07:30
Na realidade, ele
07:34
está no eval Ragas, que é o nome da minha classe.
07:38
Cadê? Case run. Ah, está aqui. O meu case run,
07:42
aqui no meu caso, o que é no final das contas?
07:45
É uma data class onde eu tenho o caso,
07:48
o meu result do meu pipeline, o contexto que eu queria,
07:52
o erro e os scores que eu estou querendo. Então, basicamente,
07:56
o resultado que eu vou ter vai ser esse cara.
08:00
Ali pra mim, tá? E eu tenho uma linha por caso,
08:03
e o scoreable é a regra inteira da aula em três palavras,
08:07
no final das contas. Só entra na média quem tem resposta,
08:11
tá? Então é basicamente isso aqui. E eu tenho aqui o meu S-Report,
08:15
eu tenho meu Build Metrics e tudo mais.
08:17
Então, esse meu case run aqui em relação a essa minha classe,
08:23
é exatamente as informações que eu preciso...
08:26
para que eu consiga fazer essas métricas e ter tudo mais, tá? Então,
08:32
eu acho que... Esse eu acho que é o ponto principal, tá?
08:36
Inclusive, esse Scorebo é o cara que eu falei
08:40
pra você em relação a essas métricas agora.
08:42
Ele só vai gerar o cara que for Scorebo. O cara que não é, vai sair fora, tá?
08:47
Então, de forma geral, galera, eu não quero dar um curso de Ragas aqui pra você, mas eu queria mostrar,
08:53
no final das contas, que eu tenho um case run...
08:56
quando eu executo o meu Evaldo Ragas,
09:00
ele chama o pipeline de verdade,
09:02
mas na hora que ele está chamando o pipeline de verdade,
09:05
eu rodo esse case aqui,
09:07
através ali de uma callback, eu vou pegar todas as informações,
09:13
ou seja, eu consigo recuperar os dados realmente de... as fontes,
09:20
eu consigo consultar o banco vetorial e pegar todas as
09:23
informações que foram usadas para daí trazer as métricas.
09:26
E o interessante é que isso que eu estou fazendo não tem perigo, por exemplo,
09:29
de respingar na minha API, porque eu estou fazendo isso de uma forma,
09:33
vamos dizer, ali separada. Mas lembre-se,
09:36
o que é importante sempre para mim aqui nesse caso é,
09:40
eu quero rodar um caso e pegar...
09:44
essas métricas. O Ragas é um cara que faz isso,
09:46
depois você pode, como que eu posso dizer,
09:49
se aprimorar nele, entender, ver esse cara com mais profundidade,
09:53
tá? Mas como eu disse,
09:54
meu ponto aqui não é ficar ensinando o código detalhe por detalhe,
09:59
você vai ter acesso a esse repositório e você pode navegar e iterar sobre esse cara.
10:04
Mas o importante é você entender...
10:06
Qual que foi o funcionamento dele, tanto nesse vídeo onde eu acabei mostrando agora,
10:10
quanto no vídeo mais teórico que eu acabei falando sobre como que o Regras funciona,
10:15
inclusive para ele verificar algumas precisões,
10:18
como ele faz algumas coisas de trás para frente.
10:21
Eu não ficaria preso nesses detalhes de implementação, mas eu entenderia o conceito.
10:28
E eu fico feliz se você entendeu esse conceito,
10:31
que no final eu vou conseguir saber a relevância,
10:34
a precisão e a fidelidade, eu já fico feliz.
10:40
O importante é saber o que a gente está medindo e
10:43
por isso que é importante aqui para a gente.
10:45
Fechou? Então, era sobre isso que eu queria falar nesses casos,
10:50
nesses tipos de métrica, mas a gente tem um outro cara que vai seguir,
10:53
onde a gente vai ver por um outro prisma que
10:55
vai acontecer com a gente nas próximas aulas.
