# Aula 07 — LiteLLM na prática

> Curso: **AI Gateways** · Duração: `04:59`

Esta aula aplica LiteLLM no projeto prático para substituir os SDKs nativos da OpenAI e da Anthropic por uma chamada unificada.

## Material prático

O prompt extraído dos prints está em:

[provider-selection-example/litellm-in-practice.md](provider-selection-example/litellm-in-practice.md)

O resultado esperado é manter o mesmo comportamento da aplicação, mas remover a duplicação de clients, SDKs e formatos de chamada usando `completion()` da LiteLLM.
