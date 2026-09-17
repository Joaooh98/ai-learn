# Aula 16 — Adicionando e alternando modelos no Proxy

> Curso: **AI Gateways** · Duração: `06:12`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de estudo pela continuidade do módulo, depois das aulas práticas 14 e 15.

Quando os prints forem adicionados, este README pode ser refinado com o fluxo exato exibido na aula.

## Resumo

Depois que a aplicação passa a chamar o LiteLLM Proxy usando um nome lógico, a próxima evolução natural é adicionar mais modelos ao proxy e alternar entre eles sem mudar o código da aplicação.

O objetivo arquitetural é manter a aplicação dependente de um contrato interno, enquanto o proxy controla qual provider/modelo real atende cada capacidade.

## Ideia central

Em vez de escrever na aplicação:

```python
model = "gpt-4.1-mini"
```

a aplicação continua usando um nome interno:

```python
model = "developer-assistant"
```

O proxy pode alterar o mapeamento interno para outro modelo:

```yaml
model_list:
  - model_name: developer-assistant
    litellm_params:
      model: openai/gpt-4.1-mini
      api_key: os.environ/OPENAI_API_KEY
```

ou expor uma nova capacidade:

```yaml
model_list:
  - model_name: developer-assistant
    litellm_params:
      model: openai/gpt-4.1-mini
      api_key: os.environ/OPENAI_API_KEY

  - model_name: deep-analysis
    litellm_params:
      model: anthropic/claude-sonnet-4-5
      api_key: os.environ/ANTHROPIC_API_KEY
```

## O que observar na prática

- adicionar modelo no proxy não deveria obrigar alteração em todos os serviços;
- alternar modelo físico deveria ser uma decisão de configuração;
- nomes lógicos devem representar capacidade, não marca do provider;
- a aplicação só deveria mudar quando a capacidade de negócio muda;
- chaves reais continuam no proxy, não na aplicação.

## Checklist de entendimento

- A aplicação conhece o nome lógico?
- O proxy sabe resolver esse nome para um modelo real?
- Cada provider tem sua chave configurada no ambiente correto?
- A troca de modelo preserva formato, qualidade e custo aceitáveis?
- Existe observabilidade para saber qual deployment respondeu?

## Ideia-chave

Adicionar e alternar modelos no proxy é o que transforma o gateway em ponto de controle. O contrato da aplicação fica estável, enquanto a infraestrutura de IA pode evoluir.
