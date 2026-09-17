# Aula 18 — Fallback com modelo fraco

> Curso: **AI Gateways** · Duração: `05:38`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de estudo pela continuidade das aulas sobre fallback.

Quando os prints forem adicionados, este README pode ser refinado com o exemplo específico mostrado.

## Resumo

Fallback com modelo fraco é uma forma de degradação controlada. Quando o modelo principal falha, está caro demais, lento demais ou indisponível, o gateway pode usar um modelo menor/mais barato/mais rápido para manter parte da experiência funcionando.

Esse fallback não deve ser tratado como equivalente perfeito ao modelo principal. Ele é uma alternativa de continuidade.

## Quando faz sentido

- respostas simples de suporte;
- classificação de baixo risco;
- resumo básico;
- reformulação de texto;
- tarefas em que uma resposta parcial é melhor que erro total;
- cenários em que latência importa mais que qualidade máxima.

## Quando pode ser perigoso

- análise crítica;
- decisão financeira, jurídica ou médica;
- extração estruturada com alto rigor;
- tarefas com formato rígido;
- respostas que precisam manter consistência forte;
- fluxos em que uma resposta ruim causa retrabalho caro.

## Fluxo conceitual

```text
Requisicao
  -> modelo principal
    -> sucesso: resposta completa
    -> falha/timeout/custo alto
      -> modelo fraco
        -> resposta degradada
```

## Como documentar a degradação

Para cada capacidade, vale registrar:

- modelo principal;
- modelo de fallback;
- diferença esperada de qualidade;
- diferença esperada de custo;
- se o usuário deve ser avisado;
- métricas para acompanhar uso do fallback.

## Exemplo de política

```text
Capacidade: resposta-suporte
Principal: modelo forte para respostas completas
Fallback: modelo menor para resposta curta e objetiva
Comportamento: se o principal falhar, responder com orientação resumida
Observabilidade: registrar fallback_used=true
```

## Ideia-chave

Fallback com modelo fraco não é só decisão técnica. É uma decisão sobre degradação aceitável da experiência.
