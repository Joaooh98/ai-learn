# Aula 02 — Chamando OpenAI com SDK

> Curso: **AI Gateways** · Duração: `04:20`

Esta aula materializa o cenário mais simples da aula anterior: uma aplicação Python chamando diretamente a OpenAI pelo SDK nativo.

## Resumo

O exemplo cria uma integração mínima com a OpenAI usando `openai` e `python-dotenv`. A aplicação conhece diretamente o provider, o SDK, o modelo, o formato de mensagem e a variável `OPENAI_API_KEY`.

Esse é o ponto de partida da trilha prática. Ele é intencionalmente simples para deixar visível o acoplamento inicial: a aplicação depende de detalhes concretos da OpenAI.

## Material prático

O projeto prático desta aula está em:

[sdk-simple-example](sdk-simple-example)

Arquivos principais:

| Arquivo | Papel |
|---------|-------|
| [calling-openai-with-sdk.md](sdk-simple-example/calling-openai-with-sdk.md) | Prompt usado para gerar o exemplo |
| [main.py](sdk-simple-example/main.py) | Script Python com chamada direta ao SDK da OpenAI |
| [requirements.txt](sdk-simple-example/requirements.txt) | Dependências do exemplo |
| [.env.example](sdk-simple-example/.env.example) | Variáveis esperadas |

## O que o exemplo demonstra

O script faz o fluxo básico:

```text
carrega .env
valida OPENAI_API_KEY
lê pergunta por sys.argv
cria client OpenAI
envia system prompt + user prompt
imprime modelo, pergunta e resposta
```

Essa simplicidade é útil didaticamente porque remove qualquer camada intermediária. Não há gateway, roteamento, fallback, cache, métricas ou normalização. A aplicação conversa diretamente com o provider.

## Acoplamentos introduzidos

Mesmo pequeno, o exemplo já acopla a aplicação a várias decisões:

- nome da variável de ambiente (`OPENAI_API_KEY`);
- biblioteca usada (`openai`);
- formato de mensagens (`role` e `content`);
- método de chamada (`chat.completions.create`);
- estrutura da resposta (`response.choices[0].message.content`);
- modelo padrão;
- tratamento de erro específico da chamada.

Isso não é errado para um primeiro passo. É justamente o baseline que permitirá entender por que um gateway começa a fazer sentido quando mais providers entram.

## Leitura das imagens

As imagens desta aula mostram o prompt de geração do exemplo, incluindo:

- objetivo do projeto mínimo;
- arquivos permitidos;
- dependências;
- variáveis de ambiente;
- pergunta padrão;
- prompt de sistema;
- comportamento esperado do código.

O foco não é criar uma arquitetura final, mas demonstrar a versão mais direta possível da integração.

## Ideia-chave

Antes de abstrair, é importante sentir o acoplamento. A chamada direta via SDK é rápida e clara, mas faz a aplicação conhecer detalhes que depois ficarão caros de espalhar.
