00:00
Olá pessoal, tudo bem?
00:03
Seguinte, tá? Falando agora sobre LLM as a Judge, né?
00:07
Quando a gente tava trabalhando com o Ragas,
00:09
né? A gente conseguia medir propriedades e,
00:13
na final das contas, outra pessoa definiu. Ou seja,
00:16
fidelidade ao contexto, a relevância, a precisão do material e tudo bem.
00:19
Mas ninguém do time do Ragas,
00:21
que tava desenvolvendo, conhece o nosso produto, né?
00:25
Então, eles não sabem, na realidade,
00:27
sei lá... Se uma resposta sobre SLA tem que dizer sobre o plano,
00:32
nem que tem que citar fonte,
00:33
nada disso. Porque acaba sendo uma biblioteca genérica, tá? E no final das contas,
00:38
quem sabe isso é a gente, tá? E é por isso que ter a utilização de um juiz,
00:44
né? Acaba nos ajudando muito.
00:46
Porque eu consigo escrever qual que é a resposta boa...
00:51
Significa, por exemplo, nesse produto, e um modelo aplica,
00:55
no final das contas, essa definição. Então,
00:58
a gente tem que entender que nós temos algo que é a nossa rubrica.
01:02
A rubrica, no final das contas, acaba sendo o nosso contrato.
01:06
Se você for aqui no nosso eval judge, você vai ver que eu tenho o
01:12
nosso system prompt aqui.
01:15
E se você avaliar o nosso prompt, que é uma das coisas, na realidade,
01:21
mais importantes quando a gente está trabalhando com juízes aqui nesse caso,
01:26
é porque é o seguinte, olha só,
01:28
você vai dar notas produzidas por
01:32
um assistente de suporte do FCIA,
01:37
você nunca vai responder a questão... por você mesmo, tá?
01:43
Você tem que dar a resposta somente contra o contexto abaixo
01:47
e você não pode usar nada que você sabe sobre isso.
01:51
como SLA, pricing, suporte e qualquer coisa fora disso.
01:57
Se o contexto não diz isso,
01:59
isso não é suportado, não importa como que isso aí pareça.
02:04
Você não pode dar nenhuma recompensa na resposta pelo fato dela
02:10
ser longa ou por ela não punir pelo fato dela ser short,
02:15
pela ser pequena. E aqui, na realidade, ele está falando.
02:20
rubric, que é a nossa rubrica, o nosso contrato. Ou seja,
02:25
ele vai dar um score para cada critério entre 0 e 1.
02:30
E aqui eu tenho groundedness score, que é 1.
02:36
Todo item que acaba sendo importante é suportado por esse contexto.
02:43
O 0 .5 é parcialmente suportado. Aqui,
02:47
o 0 .0 é algo importante, que se diz importante,
02:53
mas não é suportado de forma geral.
02:56
Aí eu tenho a mesma coisa, com um score relevance,
02:59
se a questão é respondida diretamente, se ela é respondida parcialmente,
03:03
ou se ela é irrelevante. A completeness, aqui,
03:07
que ela vai cobrir se a questão realmente,
03:11
se a pergunta era...
03:14
a gente precisava disso, ou se ela deixa informação de fora, ou se isso aí,
03:19
no final das contas, ela não é useful, ela não é útil nesse nosso caso.
03:25
E aqui, Source Support Score, ou seja, um,
03:29
se todas as listas das sources,
03:33
das fontes como base, são claras e elas conseguem sustentar... A resposta aqui,
03:40
as fontes são relacionadas, mas não conseguem suportar todos,
03:45
ou as fontes não suportam nada aqui nesse caso.
03:48
E a gente tem aqui um Clarity Score,
03:51
que mostra o quanto que a resposta está mais clara.
03:55
Mesmo esquema aqui, eu tenho um Overall Score.
03:58
E aqui, o Overall Judgment, isso aqui é um ponto importante, galera.
04:03
é o julgamento dele de forma geral. E eu tô falando aqui, ó, não faça uma média, tá?
04:11
Por exemplo, groundedness e relevance, o peso desses caras é maior do que um estilo,
04:17
né? Por exemplo, uma resposta totalmente bonita,
04:21
escrita, que não suporta o contexto e que acaba sendo uma resposta ruim,
04:27
né? E aí eu tenho outro ponto.
04:29
Se passou, ou seja, se é true...
04:32
quando a resposta é boa o suficiente para ser entregue como isso,
04:37
e a razão pelo fato disso, com duas sentenças em português,
04:42
vou pedir, main issue, ou seja, qual que é o maior problema,
04:46
as sources listadas, ou seja, as fontes listadas, e o contexto que foi dado. Então,
04:52
se você perceber aqui, isso aqui está embedado na nossa resposta,
04:57
no que está indo para o agente.
04:59
onde eu tenho a sources e eu tenho aqui o contexto dado para o nosso juiz.
05:04
Isso para a gente é muito importante, porque se você perceber,
05:08
esse system prompt é a forma que a gente está
05:11
dando para o juiz conseguir balizar na realidade
05:14
e julgar que resposta pode ser boa e resposta que
05:19
pode não ser boa no final das contas.
05:22
Então se, por exemplo, eu for rodar esse cara aqui,
05:25
só para eu rodar o programa, depois a gente vai olhando o código em conjunto.
05:29
Eu coloco Observability como False, Eval Judge com limite de 5 aqui,
05:35
e agora ele vai rodar esse cara aqui. Normalmente,
05:38
como Judge, galera, normalmente eu costumo colocar um modelo melhor,
05:43
apesar de o 4 .1 Mini, né? Na realidade,
05:45
o 4 .1 Mini foi um modelo qualquer que eu peguei, porque a gente já tá no, sei lá,
05:49
GPT -6, tá? Mas é um modelo rápido e barato e tudo mais,
05:54
mas é sempre bom você pegar...
05:57
modelos mais inteligentes para conseguir fazer e dar respostas,
06:01
nesse caso, melhores. Então, nesse caso,
06:04
o modelo consegue fazer uma boa diferença para
06:07
conseguir fazer esses tipos de avaliação.
06:12
Então, outro ponto importante, eu tenho aqui o Threshold, que é 0 .75, ou seja,
06:18
abaixo disso, isso aí já não é aceitável em relação à nota ali para mim.
06:24
Então, ele rodou um caso aqui do plano Enterprise,
06:26
agora ele está rodando o SLA aqui P1 do plano Pro.
06:32
agora SLA Starter sem garantia,
06:34
então ele tá pegando aqui alguns casos pra ele fazer esse julgamento aqui pra gente, tá?
06:40
Então eu acho que esse aí é um ponto importante,
06:42
e aí a gente vai conseguir ter um summary,
06:46
tipo um resumo da avaliação do juiz em relação aos casos, ou seja,
06:50
a gente vai ter quantos casos a gente tem no dataset,
06:54
a gente vai ter quantos casos eram respondíveis, quantos casos o juiz respondeu,
06:59
Que nesse caso eu coloquei um limite de 5,
07:01
Né? Quantos ele escapou e tudo mais. Então,
07:04
Só vamos aguardar ele rodar os últimos aqui e
07:08
para a gente conseguir ter o resultado.
07:10
Aqui, show. Então, se você olhar aqui,
07:13
Nós temos os nossos datasets, que o juiz ajudou cinco casos e aqui,
07:18
Olha só, average groundedness, relevance, completeness,
07:23
source support, clarity e o average overall, um. Então,
07:28
Todos esses casos aqui, ele passou como cinco. Agora,
07:32
Esse resultado é um problema. Por quê?
07:37
Porque um juiz que nunca discorda, ele não serve. Concordam comigo?
07:42
Um, nos cinco critérios que eu rodei, nesse caso, pode ter algum problema.
07:48
E isso tem duas explicações e elas acabam sendo opostas. Um, o pipeline é muito bom.
07:56
Ou a rubrica que ela é muito frouxa e o juiz aprova qualquer coisa.
08:02
De fora, as duas, no final das contas, acabam sendo idênticas,
08:06
porque o número final é o mesmo.
08:08
Aceitar um como uma boa notícia é o erro mais comum de quem está montando um juiz.
08:14
A única forma de separar é dar a ele respostas que você sabe que são ruins.
08:21
Porque até agora eu tenho uma rubrica, mas de respostas que eu sei que são boas.
08:27
Agora, esse é o grande ponto. Se eu der para ele respostas que são ruins,
08:32
aí eu começo a ter algo interessante.
08:35
Então, o que acontece é o seguinte.
08:38
Eu escrevi, vamos dizer assim, na mão, algumas respostas.
08:45
E eu acabei versionando isso junto,
08:47
com código, e cada uma, tá? Acaba meio que errando de um jeito, tá? Então,
08:52
Acho que esse aí é importante a gente saber. E esse cara aqui,
08:55
Ó, eu tô no Judge Calibration, aqui, ó, tá? Então, se você olhar,
09:01
Eu peguei tipos diferentes, né? de atributos,
09:06
ou seja, grounded answer, invented claim,
09:08
off-topic, incomplete answer, unclear answer, weak source support.
09:15
E no final das contas, o que acontece?
09:18
Ele traz aqui, qual é o prazo de resposta para um chamado P1 no plano PRO.
09:22
Se você olhar aqui, as perguntas são as mesmas,
09:25
mas as respostas são diferentes. Aqui tem o contexto, tudo certinho.
09:29
Aqui foi colocado o source.
09:32
E aqui eu tenho a resposta. E cada uma dessas respostas,
09:36
elas acabam tendo um problema, de forma geral,
09:39
em um desses itens aqui para mim. E aí as coisas acabam sendo mais interessantes,
09:46
Tá? Então isso normalmente é chamado de sonda,
09:49
onde eu consigo ter esse tipo de coisa.
09:52
Então isso aí acaba gerando esses tipos de situação.
09:58
Agora, um ponto que é importante aqui...
10:00
Eu trago como que eu imaginava aquele ponto. Então,
10:04
Issue expected, none, at least groundedness é 0.9,
10:10
O relevant score 0.9, o overall score 0.5,
10:15
A note está aqui, diz de fato,
10:18
Diz o fato e para. O piso rubrica aqui. Se esse não passar, o judge está quebrado.
10:24
Aqui note, fluente, plausível, inteiramente inventada.
10:27
É o caso que justifica a existência do judge.
10:31
Então aqui, basicamente, é uma forma de você calibrar.
10:34
Você tem itens que você consegue,
10:38
No final das contas... A fazer uma calibragem,
10:41
Porque quando o juiz ele roda isso, no final das contas,
10:45
Ele entende ali pra ele o que é bom,
10:47
O que é ruim. Ou seja,
10:49
É como se eu estivesse treinando esse cara aqui nesse caso, tá?
10:53
E isso aí é interessante. E pra eu calibrar esse cara,
10:57
Eu criei um... Como se diz?
11:01
Um parâmetro aqui, quer ver? Que é o menos, menos calibrate.
11:06
Quando eu rodo esse cara, no final das contas,
11:10
O que que acontece? Ele nem vai tocar na pipeline,
11:12
Nem no banco de dados. Vão ser seis chamadas que a gente acaba fazendo,
11:16
Né? São seis itens ali pra gente.
11:18
Provavelmente eu vou ter uns quatro, ok?
11:20
E unexpected o clarity e o suporte a que talvez a gente tenha...
11:26
Algum problema, aqui ó, non-gap,
11:28
O juiz recebe as fontes com nomes de arquivo e o contexto sem atribuição,
11:32
Então não tem como ligar um ao outro,
11:34
E isso exige um pipeline entregar a origem de cada trecho, tá?
11:39
Aqui são pontos importantes aqui,
11:43
Mas o ponto claro aqui é que eu tenho sondas aqui pra mim que acabaram passando, né?
11:50
Agora, o interessante aqui é se você olhar aqui ó, olhando de cima pra baixo,
11:55
Eu tenho aqui Invented Claim. E você olhar esse cara, a clareza dele tá 1.0.
12:02
Ou seja, tá 1. Ou seja, está super clara a resposta.
12:06
Mas ela tá como 0 de Grounded. Ou seja,
12:09
Ela não consegue se apoiar em nenhuma fonte, basicamente.
12:13
E em geral, ele achou 0.3.
12:15
Se você acabar olhando, tá? Se você olhar aqui o terceiro item, né?
12:22
Eu tenho overall zero, grounded zero, e o clarity, aqui no meu caso, um.
12:28
Ou seja, a resposta acaba sendo irrelevante.
12:33
Resposta incompleta. Eu tenho clareza um e o grounded zero aqui.
12:38
A resposta que não está clara.
12:39
Eu tenho grounded um, mas a clareza da resposta, nesse caso, ela não está tão boa.
12:46
Entendeu? Então esse aí que é o grande ponto que eu queria trazer aqui,
12:50
Que vocês conseguissem entender como são importantes esses tipos de informação.
12:56
Agora, o interessante disso é que, entre aspas,
12:59
Eu consigo calibrar o meu juiz. Esse último ponto aqui,
13:04
Ele realmente viu aqui como pra gente que é um gap que eu conheço já,
13:09
Tá? A primeira vez que eu rodei eu tinha tido mais problemas,
13:12
Dessa vez eu só tive um, que na realidade ele não consegue...
13:15
Fazer a ligação de um contexto atribuindo qual é o arquivo referente.
13:19
Então, ele não consegue fazer esse cruzamento e por isso que
13:25
Ele vai entrar aqui para a gente como tudo um aqui,
13:29
Mas no final das contas tem um gap. Por isso ele não consegue,
13:32
Vamos dizer, medir certo, tá? Mas isso aí não tem problema.
13:36
Cada critério que eu coloquei aqui, inclusive,
13:38
É independente para um propósito de diferença,
13:41
Tá? Então, isso aí que é um ponto importante, tá?
13:47
Agora, um ponto importante aqui, tá? É o seguinte, como que eu posso dizer?
13:54
Apesar dele ter dado uma nota geral, né?
13:58
Quem disse se o negócio passou ou não fui eu no meu programa,
14:03
onde eu falei qual que é o mínimo que tem que ter,
14:07
vamos dizer, o score mínimo que ele tem que ter pra conseguir dar como ele passou.
14:12
E eu acho que isso aí é o importante, tá? Por quê?
14:15
Porque quem define no final das contas sou eu com a minha regra e etc.
14:19
Então isso aí que eu acho que é um dos pontos mais importantes.
14:23
E também tem um caso que, por exemplo, um juiz não consegue julgar. Ou seja,
14:28
o caso é que ele não é julgado. O que pode acontecer?
14:32
Ou seja, lembra aquele caso onde eu tenho...
14:37
que eu quero saber o e-mail do financeiro lá,
14:39
aquela história do financeiro onde ele pega os oito itens que ele
14:44
não consegue medir por conta que ele não trouxe lá o e-mail.
14:47
Se eu rodar esse cara aqui,
14:49
eu vou ter em tese que o juiz não consegue
14:52
julgar porque eu não consegui rodar nem o pipeline e etc.
14:58
por conta desse tipo de problema no final das contas, tá?
15:03
Então... O juiz, de forma geral,
15:05
ele traz as rubricas desse nosso projeto. O RAGAS,
15:11
ele trazia baseado em métricas com propriedades nomeadas ali por ele.
15:16
O componente que a gente trabalhava,
15:19
a gente consegue ver de onde a informação se perdeu. E o contrato,
15:23
a gente começa a ver em relação de onde veio essa parte da API.
15:28
Então, a gente tem contrato de API, a gente tem visualização por componente,
15:33
a gente tem o RAGAS, que ele tem métricas nomeadas,
15:36
que a gente já tem, e a gente tem o Judge,
15:39
que no final das contas a gente tem essas rubricas e etc.
15:46
Agora, somente para a gente entender, inclusive como termo,
15:49
se você usar a parte de calibrar o juiz,
15:52
se você perceber a parte de calibrar o juiz,
15:55
na realidade, eu estou medindo... a eficiência do juiz, mas não das respostas,
16:02
tá? Então, isso aí é importante no final das contas. Por quê?
16:05
Porque esse tipo de teste permite eu conseguir verificar como que tá o juiz. Por exemplo,
16:10
se um dia eu rodar uma rodada e vai dar um pra tudo, eu vou desconfiar,
16:17
então eu vou rodar a calibração. Então, eu vou ter duas respostas possíveis.
16:22
A calibração passa, ou seja, o 1.0 é real,
16:25
então o pipeline, ele é bom mesmo. A calibração falha,
16:30
então é o juiz que está cego e o 1.0 não vale nada.
16:33
Então, sem essa calibração, você não tem como distinguir. Então,
16:37
o único jeito de saber se um número está realmente bonito,
16:41
ou se a gente tem uma notícia boa,
16:43
é saber se a gente tem algum problema que está ali quebrado.
16:47
Então, o interessante desses tipos de calibração é o seguinte,
16:50
imagina que eu rodo uma aplicação, dá tudo 1, passei em tudo.
16:55
Daí eu falo, opa, tem coisa estranha, né?
16:57
Como é que eu posso passar em tudo? Aí eu rodei essa calibração.
17:00
E na calibração não deu 1 em tudo. Deu realmente os dados que eu estava imaginando.
17:05
Então significa que as minhas respostas deram 1 em
17:08
tudo porque a resposta era muito boa.
17:10
Agora, esse que é o ponto.
17:12
Imagina que eu rodo e as respostas dão todas muito boas. É todas 1.
17:16
E eu rodo a calibração, dá tudo 1 também. O que significa?
17:20
Eu estou com um problema no meu juiz. Então,
17:23
a parte de calibração, no final das contas,
17:26
é para a gente conseguir ter uma forma de eu conseguir medir se
17:30
o juiz está medindo da forma como imagino que ele tem que medir.
17:35
Então, por que eu estou dizendo isso?
17:37
Porque normalmente tem uma confusão muito grande entre o
17:40
juiz dar a resposta do que ele acha,
17:44
baseado na nossa rubrica e no nosso dataset,
17:48
E tem a situação onde que o juiz,
17:52
ele está sendo avaliado e não mais o nosso dataset,
17:55
para eu garantir que ele está avaliando corretamente. Então,
17:58
essa calibração é como se fosse uma forma de eu
18:01
avaliar o juiz e não avaliar a resposta do nosso dataset.
18:06
Então, por isso que eu tenho esse judgecalibration.json,
18:10
porque é uma forma de eu realmente medir se ele está...
18:14
nessa calibração saindo do jeito que eu estou esperando. Então,
18:17
quando eu rodo aqueles monte de respostas como um e vejo
18:21
o meu juiz aqui com essas respostas nessa forma,
18:24
eu vou acreditar que as minhas respostas estão todas um,
18:27
elas realmente estão muito boas. Por quê? Porque eu sei que o juiz,
18:31
ele já foi no passado aqui capaz de mostrar que ele é capaz de dar notas ruins.
18:37
Caso ele tenha alguma resposta incoerente aqui nesse caso.
18:42
E obviamente que essa parte de calibração,
18:44
você precisa ter um dataset maior. Eu fiz sempre a mesma pergunta,
18:48
então você pode trabalhar com mais dados e tudo mais.
18:51
Mas a ideia principal do conceito é esse.
18:54
Então, lembre-se, LLMS Judge vai julgar o seu dataset baseado na sua rubrica,
19:01
mas você também tem que conseguir...
19:03
ter formas de calibragem para que você consiga verificar
19:07
se o prompt do juiz está correto de forma geral. Então,
19:12
acho que esse aí é o principal aprendizado também em relação a isso.
19:17
Agora, como que foi feito isso? Na realidade, não tem segredo aqui.
19:22
É um prompt que eu vou passar para o juiz.
19:25
O calibration, na realidade, tem o meu modelo,
19:29
com os itens que eu quis passar para ele.
19:34
O passar, né, o veredito é basicamente se ele passa do meu mínimo, score mínimo,
19:39
que nesse caso é o meu threshold que eu tinha passado,
19:41
0.75, e aqui o calibration, ele vai ler aqueles arquivos, né,
19:47
aquele arquivo pra sair trazendo as informações, e aqui é o judge runs,
19:53
né, ou seja, eu tenho um run,
19:55
E esse run, o que ele faz?
19:56
Ele pega todas aquelas informações e dá um invoke no juiz, ou seja,
20:01
ele chama o modelo, passando esse prompt para o juiz,
20:04
e aí o juiz vai trazer o resultado. Então,
20:07
no final das contas, o LLMS Judge é pegar a sua resposta,
20:12
a resposta desejada, as fontes,
20:16
e pedir para ele avaliar em relação a isso. Ou seja,
20:18
é a utilização comum da IA, de forma geral, tá?
20:22
Então, eu acho que esse aí é um ponto importante para
20:25
Que você saiba como é que as coisas funcionam.
20:28
Aí eu tenho a forma para ele sumarizar e para ele gerar um relatório e tudo mais.
20:32
Mas o que eu acho que é o mais importante
20:34
De tudo é você saber que o LLM ou como juiz,
20:40
Ele tem um objetivo. Você vai passar um prompt,
20:42
Você vai passar todas as informações e, baseado nesse prompt,
20:45
Ele vai dar uma nota para você.
20:47
Mas quem controla como ele vai dar essa nota vai ser tudo isso baseado no prompt. Então,
20:53
Se eu pudesse dar um resumo para você, o que mais, não é que é o que mais pega,
20:59
O LLM como juiz é completamente dependente do prompt.
21:05
É o prompt dele que realmente vai dizer o que é bom,
21:08
O que é ruim e vai definir os limiares de notas e etc.
21:14
Então, basicamente é isso aí.