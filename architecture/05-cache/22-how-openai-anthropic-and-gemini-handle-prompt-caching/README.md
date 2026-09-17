# Aula 22 — Como OpenAI, Anthropic e Gemini tratam prompt caching

> Curso: **Cache** · Duração: `07:33`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados — e a comparação exata de
comportamento/preço de cada provider — este README pode ser ajustado para refletir o conteúdo
exato da aula.

## Resumo

Depois de diferenciar cache da aplicação de cache do provider (aula 21), esta aula compara como
os principais providers implementam prompt caching nativamente: o que é cacheado, por quanto
tempo e como isso afeta custo e latência.

## Pontos de comparação esperados

- **O que pode ser cacheado**: normalmente o início do prompt (ex.: system prompt, instruções
  fixas, poucos documentos de contexto reutilizados entre chamadas).
- **Como o cache é ativado**: automático a partir de um tamanho mínimo de prompt repetido, ou
  explícito via parâmetro/flag na chamada — depende do provider.
- **Tempo de vida do cache**: cada provider define por quanto tempo um prefixo cacheado permanece
  reaproveitável antes de expirar.
- **Impacto em custo e latência**: tokens cacheados costumam ser cobrados a um valor menor que
  tokens processados do zero, além de reduzir o tempo de processamento daquela parte do prompt.

## Ideia-chave

Prompt caching nativo não é um recurso configurado do zero pela aplicação — é um comportamento do
provider que a aplicação precisa conhecer e estruturar o prompt para aproveitar (ex.: colocando o
conteúdo fixo e repetido no início do prompt). A próxima aula coloca isso em prática.
