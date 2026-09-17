# Aula 17 — Fallback técnico

> Curso: **AI Gateways** · Duração: `06:32`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de estudo pela continuidade do módulo de resiliência.

Quando os prints forem adicionados, este README pode ser ajustado para refletir o fluxo exato da aula.

## Resumo

Fallback técnico é uma alternativa automática quando o caminho principal falha. Em AI Gateway, isso normalmente significa tentar outro modelo, deployment, região ou provider sem exigir que a aplicação implemente essa lógica.

O objetivo não é melhorar a resposta. O objetivo principal é manter o serviço disponível quando o caminho principal está lento, indisponível ou retornando erro.

## Fluxo conceitual

```text
Aplicacao
  -> AI Gateway
    -> tentativa principal
      -> sucesso: retorna resposta
      -> falha: tenta fallback tecnico
        -> sucesso: retorna resposta alternativa
        -> falha: retorna erro controlado
```

## Exemplos de fallback técnico

- modelo principal indisponível -> usar outro modelo compatível;
- região principal indisponível -> usar deployment em outra região;
- provider principal com erro -> usar provider secundário;
- timeout no modelo forte -> usar modelo mais rápido;
- erro temporário -> tentar rota alternativa com limite.

## Cuidados

Fallback não é invisível do ponto de vista do produto. Mesmo que a API responda com sucesso, a resposta pode mudar em:

- qualidade;
- estilo;
- latência;
- custo;
- aderência ao formato esperado;
- capacidade de seguir instruções complexas.

Por isso, fallback técnico precisa de observabilidade. O time deve conseguir saber quando a resposta veio do caminho principal e quando veio de uma alternativa.

## Boas perguntas

- O fallback tem qualidade suficiente para esse caso de uso?
- O usuário precisa saber que houve degradação?
- O custo do fallback é maior ou menor?
- A resposta mantém o mesmo contrato?
- O fallback pode mascarar incidentes importantes?

## Ideia-chave

Fallback técnico aumenta disponibilidade, mas cria trade-offs. Ele precisa ser configurado por capacidade, não como regra genérica para todos os usos de IA.
