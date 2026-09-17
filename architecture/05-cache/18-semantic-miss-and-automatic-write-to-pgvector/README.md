# Aula 18 — Miss semântico e gravação automática no pgvector

> Curso: **Cache** · Duração: `04:26`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Complementando a integração da aula 17, esta aula foca no outro lado do fluxo: o que acontece
quando ocorre um **miss semântico** — nenhuma entrada parecida o suficiente foi encontrada no
pgvector. Nesse caso, além de chamar o modelo normalmente, a aplicação precisa gravar
automaticamente a nova pergunta, sua resposta e seu embedding, para que ela passe a valer como
cache para as próximas perguntas parecidas.

## Fluxo conceitual

```text
miss semântico -> chama o modelo -> recebe resposta
                -> gera/reaproveita o embedding da pergunta
                -> grava (pergunta, resposta, embedding) no pgvector
```

## Ideia-chave

Sem essa gravação automática, o cache semântico nunca cresce: ele fica preso ao conjunto inicial
de exemplos e nunca aprende com o uso real. É essa escrita contínua a cada miss que faz a taxa de
hit aumentar com o tempo.
