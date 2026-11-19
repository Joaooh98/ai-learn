# Design Docs: síntese e atualização

[Voltar ao módulo](../README.md) · Revisão: **19/11/2026**

## O que entendi do material

A trilha apresenta documentação como uma forma de reduzir perda de contexto. A parte histórica
mostra o custo de decidir sem feedback; Agile reposiciona a documentação como apoio à entrega;
a parte de IA mostra que o documento também orienta ferramentas. O ganho depende de manter
informações corretas, encontráveis e ligadas ao trabalho real.

O eixo de produto responde qual problema resolver. O eixo de arquitetura define responsabilidades
e relações. O detalhamento de feature fecha contratos, falhas e critérios verificáveis. Uma
RFC organiza a proposta em discussão; um ADR preserva o motivo de uma decisão e suas consequências.
Esses papéis importam mais que exigir um arquivo para cada sigla.

## O que foi incrementado

As **22 imagens** foram abertas e interpretadas. Foram revisadas **21 notas**, com explicações
visuais, cenários de fronteira e vínculos a práticas atuais. Uma duplicação literal entre os
casos de uso 4 e 5 foi consolidada: o primeiro preserva a explicação, o segundo traz exercício.

No exemplo de rate limiting, a revisão destacou uma divergência real entre as notas: o PRD
cita serviço dedicado e janela deslizante, enquanto HLD/FDD descrevem SDK e outras estratégias.
A solução não foi escolhida silenciosamente; ficou registrada como decisão a resolver.

- [Guia de aplicação e fontes atuais](application-guide.md)
- [Exemplo de rastreabilidade e critérios de aceite](traceability-example.md)
- [Registro visual e limites da revisão](review-record.md)

## Como estudar agora

Leia uma nota e use o complemento para tentar produzir uma evidência: um requisito com origem,
um contrato sem ambiguidade ou um cenário de teste. Ao terminar o rate limiter, explique
qual arquitetura escolheu, quais falhas ela tolera e como demonstrará isso. Não apresente
uma meta do documento como se fosse resultado já medido.
