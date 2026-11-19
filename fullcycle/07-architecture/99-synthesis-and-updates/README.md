# Arquitetura com IA: síntese e atualização

[Voltar à trilha](../README.md) · Revisão focal: **19/11/2026**

## O que conecta o material

As oito trilhas tratam responsabilidades diferentes do mesmo sistema. Acoplamento organiza
o código para permitir mudança. Gateway concentra políticas de acesso ao provider. O fluxo
de chamada define como entregar o trabalho. Cache controla reutilização. RAG seleciona a
evidência. Observabilidade permite diagnosticar. Evaluation mede comportamento. Segurança
controla as fronteiras de confiança, acesso e ação.

O ponto comum é distinguir uma possibilidade de uma garantia: API compatível não implica
qualidade equivalente; stream aberto não implica resultado completo; similaridade não implica
reutilização correta; citação não implica origem confiável; nota alta não implica ausência
de falha crítica. Cada garantia precisa de responsável, contrato e evidência.

## Cobertura desta rodada

Foram lidas **63 imagens em dez aulas**, com um recorte por trilha e três aulas de Segurança.
Cinco aulas já escritas receberam aprofundamento e cinco READMEs vazios foram preenchidos:
privacidade, juiz e segurança de RAG. As demais imagens e aulas permanecem para revisão em
rodadas posteriores; esta pasta não declara auditoria integral das 763 imagens de Arquitetura.

- [Aplicação atual por responsabilidade](application-guide.md)
- [Exercício integrando as trilhas](integration-exercise.md)
- [Registro das aulas e 63 imagens](review-record.md)

## Ganhos concretos

O novo texto diferencia retenção de sampling e corrige a interpretação de hash como redução
de cardinalidade. A rubrica do juiz agora distingue escalas ilustrativas da escala usada no
código. As notas de Segurança explicam cada estágio do ataque e contrastam a baseline dos
prints com o controle de proveniência presente nos arquivos atuais.

Os exemplos de resiliência, streaming, cache e retrieval ganharam cenários verificáveis.
As notas de acoplamento deixaram de apresentar distância da main sequence como uma fila
automática de refatoração e incluem um exemplo aritmético para interpretação.
