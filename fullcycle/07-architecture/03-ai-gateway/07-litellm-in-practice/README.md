# Aula 07 — LiteLLM na prática

[Índice do módulo](../README.md)

> Curso: **AI Gateways** · Duração: `04:59`

Esta aula aplica LiteLLM no projeto prático para substituir os SDKs nativos da OpenAI e da Anthropic por uma chamada unificada.

## Material prático

O prompt extraído dos prints está em:

[provider-selection-example/litellm-in-practice.md](provider-selection-example/litellm-in-practice.md)

O resultado esperado é manter o mesmo comportamento da aplicação, mas remover a duplicação de clients, SDKs e formatos de chamada usando `completion()` da LiteLLM.

## Fluxo implementado e limites

O [main.py](provider-selection-example/main.py) valida `AI_PROVIDER`, escolhe um modelo, adiciona prefixo quando necessário e chama `completion()` uma vez no código da aplicação. O LiteLLM passa a normalizar a integração, mas a seleção por execução continua explícita; não há proxy nem fallback configurado.

O prompt e o resultado do repositório usam defaults diferentes. A [documentação do exemplo](provider-selection-example/README.md) registra essa diferença e os comandos com override de ambiente.

Se `AI_MODEL` já contém `/`, o código usa esse valor sem conferir se o prefixo combina com `AI_PROVIDER`. Assim, `AI_PROVIDER=openai` junto com um modelo `anthropic/...` faz a validação local olhar a chave OpenAI, embora o destino da chamada seja Anthropic. Mantenha as variáveis coerentes. Uma versão mais robusta resolveria e validaria o provider efetivo a partir da configuração final.

**Exercício:** execute os dois providers com a mesma pergunta e compare o conteúdo, não apenas a estrutura da resposta. Reduzir código de integração não torna o comportamento dos modelos igual.
