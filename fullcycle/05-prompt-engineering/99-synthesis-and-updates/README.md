# Prompt Engineering: síntese e atualização

[Voltar ao módulo](../README.md) · Revisão: **19/11/2026**

## O que o material ensina

A trilha começa com instruções e exemplos, avança para composição de etapas e agentes,
separa o prompt da aplicação por versionamento e termina medindo as consequências de cada
escolha. O aprendizado central é transformar uma intenção vaga em comportamento observável.
Um prompt melhor precisa melhorar a tarefa, e não apenas produzir um texto mais elaborado.

No exemplo de code review, três políticas procuram os mesmos tipos de falha com níveis
diferentes de tolerância a suspeitas. O print de evaluation mostra que a versão conservadora
tem precision de 1,00 e recall de 0,13; a balanceada melhora o F1 para 0,40, sem resolver
a baixa cobertura. A comparação ensina a olhar o perfil do erro, não só o vencedor.

## O que foi incrementado

As dez notas de `my-summary/comparative-evaluation/` receberam complementos específicos.
Todas as sete imagens desse conjunto foram abertas e interpretadas. As fórmulas ganharam
contagens completas; os números do dashboard foram transcritos; as notas práticas agora
explicam o que o avaliador realmente mede e quais erros de parsing podem distorcer o resultado.

- [Guia para aplicar os conceitos hoje](application-guide.md): prompting, contexto, agentes,
  versionamento e experimentação, com fontes oficiais.
- [Registro de evidências e limitações](review-record.md): arquivos conferidos e fronteiras
  entre demonstração, observação visual e recomendação.

## Como aproveitar no próximo projeto

Escolha uma tarefa estreita, como identificar uma família de problemas em um diff. Defina a
saída esperada, construa referências e rode uma instrução simples como baseline. Acrescente
few-shot ou decomposição somente quando os erros indicarem uma necessidade concreta.
Preserve a versão anterior e promova a nova apenas após comparar qualidade e custo.

Um experimento deve permitir responder: qual entrada falhou, por que a referência a considera
falha, o que mudou e se a melhoria se mantém em exemplos que não foram usados no ajuste.
Essa disciplina continua útil mesmo quando mudam o modelo, o framework ou o dashboard.
