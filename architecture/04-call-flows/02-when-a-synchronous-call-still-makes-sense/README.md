# Aula 02 — Quando uma chamada síncrona ainda faz sentido

> Curso: **Fluxos de Chamada** · Duração: `04:17`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo, a partir da aula anterior
([`01-execution-problem-in-ai-applications`](../01-execution-problem-in-ai-applications/README.md)).
Quando os prints forem adicionados, este README pode ser ajustado para refletir o fluxo exato da
aula.

## Resumo

Depois de apresentar o problema de latência e variabilidade das chamadas de IA, a aula equilibra
o discurso: nem toda chamada precisa virar streaming ou processamento assíncrono. Em muitos casos
o modelo síncrono clássico — a aplicação chama, espera e responde — continua sendo a solução mais
simples e correta.

## Quando síncrono ainda é a escolha certa

- **Resposta curta e rápida o suficiente**: classificações, extrações pequenas ou respostas
  objetivas em que a latência esperada é baixa e previsível.
- **Fluxo interativo que já espera uma pausa**: o usuário fez uma pergunta e sabe que uma resposta
  elaborada leva alguns segundos — não há expectativa de resposta instantânea.
- **Baixo volume ou uso interno**: ferramentas internas, scripts, automações pontuais, onde não há
  concorrência de muitos usuários disputando os mesmos recursos.
- **Simplicidade operacional**: síncrono não exige fila, worker, callback ou webhook — menos peças
  móveis, menos pontos de falha.

## O limite do modelo síncrono

```text
Aplicação -> aguarda modelo -> resposta -> aplicação continua
```

O risco aparece quando esse padrão simples é aplicado sem questionar em cenários de alto volume,
prompts grandes ou UI que precisa parecer responsiva. Nesses casos, manter tudo síncrono começa a
gerar timeouts, filas de requisições paradas e má experiência percebida — motivo pelo qual o
módulo segue explorando streaming (aula 03) e processamento assíncrono (aula 04).

## Ideia-chave

Síncrono não é a opção "ruim" da arquitetura. É a opção padrão, e continua sendo a correta sempre
que a espera é curta, previsível e aceitável para quem está do outro lado da chamada. A decisão
de sair do síncrono deve ser motivada por um problema real de latência percebida ou de uso de
recursos, não por hábito.
