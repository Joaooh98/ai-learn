# Aula 03 — Adicionando Anthropic como opção

> Curso: **AI Gateways** · Duração: `04:28`

Esta aula evolui o exemplo anterior para permitir escolher entre OpenAI e Anthropic por variável de ambiente. A mudança é pequena no produto, mas grande na arquitetura: a aplicação passa a conhecer dois SDKs, dois clients, duas chaves e dois formatos de chamada.

## Resumo

A ideia da aula não é implementar fallback. O objetivo é mostrar o custo de suportar mais de um provider sem uma camada de compatibilidade. A escolha é feita por execução, via `AI_PROVIDER`, mas a aplicação continua carregando detalhes específicos de cada provider.

Esse é um passo importante porque evidencia o problema que o AI Gateway tentará resolver: reduzir a fricção de múltiplos providers sem duplicar conhecimento técnico em cada feature.

## Material prático

O prompt extraído das imagens está em:

[provider-selection-example](provider-selection-example)

Arquivos principais:

| Arquivo | Papel |
|---------|-------|
| [adding-anthropic-as-option.md](provider-selection-example/adding-anthropic-as-option.md) | Prompt da aula 03 |

## O que muda em relação à aula 02

Na aula 02, o código tinha uma única direção:

```text
Aplicação -> SDK OpenAI -> OpenAI
```

Nesta aula, a aplicação passa a escolher:

```text
AI_PROVIDER=openai    -> SDK OpenAI    -> OpenAI
AI_PROVIDER=anthropic -> SDK Anthropic -> Anthropic
```

A variável `AI_PROVIDER` controla qual bloco de código será usado. A variável `AI_MODEL` permite escolher o modelo, com defaults diferentes para cada provider.

## O aprendizado arquitetural

Adicionar um segundo provider parece só adicionar uma condição, mas traz várias decisões novas:

- qual SDK importar;
- qual client instanciar;
- qual API key validar;
- qual modelo padrão usar;
- como montar a request;
- como ler a resposta;
- como tratar erro;
- como comunicar provider inválido.

Se esse padrão for repetido por várias features, a aplicação começa a carregar a complexidade de integração que deveria estar centralizada.

## O que ainda não existe aqui

Esta aula ainda não implementa:

- fallback;
- retry;
- roteamento inteligente;
- normalização completa de entrada e saída;
- medição centralizada de custo;
- dashboard;
- políticas de uso.

Isso é proposital. O exercício mostra apenas a dor inicial: suportar dois providers sem gateway já aumenta a superfície de manutenção.

## Ideia-chave

Escolher provider por variável de ambiente é melhor do que duplicar aplicações, mas ainda não é gateway. A aplicação continua sabendo demais sobre cada provider.
