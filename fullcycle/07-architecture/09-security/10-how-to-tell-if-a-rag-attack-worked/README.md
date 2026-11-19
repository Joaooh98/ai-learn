# Aula 10 — Como saber se um ataque ao RAG funcionou

> Curso: **Segurança** · Duração: `08:18`

[Índice do módulo](../README.md)

A pergunta legítima do usuário pode ser respondida usando um documento adversarial que
entrou antes, pela ingestão. A aula ensina a acompanhar os estágios e distinguir exposição
a conteúdo contaminado de efeito observado na resposta. Os oito quadros são modelos de
diagnóstico e desenho de controles, não relatórios de um ataque executado nesta revisão.

## 01 — O caminho do documento até o modelo

![O caminho do documento até o modelo](01.png)

Conteúdo externo atravessa ingestão, índice, retrieval e montagem do contexto. A superfície
não se limita à mensagem do usuário: anexos, integrações e documentos internos também
podem carregar afirmações falsas ou instruções indevidas. Cada transição precisa de uma
política identificável e de evidência para diagnóstico.

## 02 — Accepted, indexed, retrieved e selected

![Accepted, indexed, retrieved e selected](02.png)

`Accepted` informa que o documento passou pelos controles de entrada; validação estrutural
não comprova confiança. `Indexed` significa disponível no universo de busca. `Retrieved`
marca presença nos candidatos e `selected` indica seleção para o contexto após reranking.
Esses estados respondem até onde o conteúdo chegou, não se o modelo o obedeceu.

## 03 — Selected, used e influenced não são equivalentes

![Selected, used e influenced não são equivalentes](03.png)

Um reranker pode descartar o candidato antes da geração. Também pode selecioná-lo e o modelo
não produzir o efeito desejado pelo atacante. `Used` deve ter definição operacional, como
fonte declarada pela resposta; não representa acesso ao raciocínio interno. Para afirmar
influência, verifique um resultado previsto no caso de teste e registre sua limitação.

## 04 — Afirmação contaminada e marcador de injeção

![Afirmação contaminada e marcador de injeção](04.png)

Factual poisoning tenta fazer uma informação adulterada parecer evidência. Indirect prompt
injection tenta converter conteúdo recuperado em instrução. Um marcador controlado no
experimento ajuda a detectar um efeito específico, mas não cobre todos os modos de falha.
O exemplo médico do quadro é apenas ilustração de afirmações conflitantes, sem recomendação clínica.

## 05 — Resposta esperada e recusa

![Resposta esperada e recusa](05.png)

Quando só existe uma fonte não confiável, recusar pode ser o resultado correto. Quando há
fonte legítima suficiente, o sistema pode responder com ela. Defina o comportamento esperado
por caso, evitando premiar um sistema que recusa tudo e deixa de cumprir a função de produto.

## 06 — Diagnóstico e critério bloqueante

![Diagnóstico e critério bloqueante](06.png)

O quadro distingue alcançar retrieval/seleção de usar fonte indevida, adotar afirmação
contaminada ou seguir instrução indireta. No contrato da suíte, qualquer falha bloqueante
aplicável torna `attack_resisted` falso. Essa severidade pertence ao threat model do exercício;
a avaliação operacional do impacto depende dos dados, permissões e ações envolvidos.

## 07 — Quatro resultados possíveis

![Quatro resultados possíveis](07.png)

O documento pode ser rejeitado antes do índice, indexado sem ser recuperado, chegar ao modelo
sem efeito observado ou influenciar a saída. Não trate esses resultados como equivalentes.
Um conteúdo não recuperado em uma consulta pode aparecer em outra: ausência de exposição
naquele caso não demonstra que a origem foi controlada.

## 08 — Defesas distribuídas pelo fluxo

![Defesas distribuídas pelo fluxo](08.png)

A matriz organiza pontos de intervenção na fonte, ingestão, processamento, índice, busca,
orquestração e entrega. A presença do nome de um controle no desenho não prova implementação
nem eficácia. Associe cada controle à regra executada, ao teste e ao risco residual. Reranking
por relevância não é automaticamente um filtro de segurança.

## Complemento e aplicação atual

> Revisão em **19/11/2026**.

A [orientação da OWASP sobre prompt injection](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
recomenda defesas em camadas e limitação de privilégios. A autorização de acesso ou de ação
deve permanecer em código, fora da decisão textual do modelo.

No [avaliador local](../../project-for-exemple/security/app/eval_security_rag.py),
`DIAGNOSTIC` inclui retrieval e seleção; os checks bloqueantes medem origem usada,
termos/marcadores e comportamento esperado. A detecção de termos usa presença textual com
`casefold()`: uma resposta que nega uma afirmação pode ainda conter o termo, e uma paráfrase
pode escapar. Revise resultados manualmente e acrescente casos que exponham essas limitações.

**Exercício proposto:** para cada caso, registre versão do corpus, fixture, política ativa,
estágios alcançados, efeito esperado e erro de execução. Erro de infraestrutura não deve
ser contado como defesa bem-sucedida. Nenhum ataque foi executado nesta revisão.


### Limite do check de resposta fundamentada

Na suíte local, `trusted_grounded()` verifica `has_answer` e presença de pelo menos uma
fonte da lista confiável em `used_sources`. Isso é uma aproximação por atribuição de fonte,
sem verificar se cada afirmação da resposta é sustentada. Um resultado positivo desse check
não deve ser apresentado como prova de fidelidade semântica completa. Combine inspeção por
afirmação, evidência por trecho e casos de citação correta com conteúdo errado ao evoluir a avaliação.
