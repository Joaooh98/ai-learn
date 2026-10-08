# Aula 02 — Hit, miss e cache-aside

> Curso: **Cache** · Duração: `04:06`

## Material e foco da aula

Os quatro prints mostram consulta ao cache antes da inferência, retorno imediato no hit e
gravação da resposta no miss. [O fluxo controlado pela aplicação](03.png) prepara o padrão
usado nas aulas práticas.

## Conceitos

- **Hit**: há uma entrada que atende à chave, ao escopo e à política de validade; a aplicação a reutiliza.
- **Miss**: não há entrada utilizável. Ausência, expiração ou rejeição de um candidato podem levar a miss.
- **Cache-aside**: a aplicação consulta o cache, executa o trabalho original no miss e decide se grava o resultado.

```text
requisição → constrói chave e escopo → consulta cache
  entrada válida → retorna resposta armazenada
  miss           → chama modelo → valida saída → grava se elegível → retorna
```

O cache não chama o modelo por conta própria nesse padrão. No exemplo, a decisão está em
`analyze_ticket()` de [main.py](../mba-ia-cache/main.py), e o cache exato é o dicionário `CACHE`.

## Complemento de estudo: acerto, falha e concorrência

Falha de acesso ao cache não é igual a miss normal. Ela pode exigir um caminho alternativo,
mas esse comportamento precisa ser explícito. Cache-aside também não mantém automaticamente
o cache consistente com alterações da fonte. [Referência: Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).

Três situações tornam o fluxo mais realista:

1. **Resposta inválida**: JSON que não atende ao contrato não deve ser gravado ou servido como hit.
2. **Miss simultâneo**: duas requisições para a mesma chave podem chamar o modelo antes de
   qualquer uma gravar. Coordenação por chave, como *single-flight*, evita trabalho duplicado.
3. **Cache indisponível**: seguir ao modelo pode preservar disponibilidade, mas elevar carga
   e custo. Timeout, limite de concorrência e política de contingência precisam ser combinados.

O projeto não implementa coordenação por chave. O dicionário e o contador são locais ao processo:
reiniciar a aplicação os zera, e múltiplos workers mantêm estados diferentes.

## Métricas para revisar o fluxo

`hit_rate = hits / consultas elegíveis` é útil, desde que o denominador seja definido. Separe
hits exatos, hits semânticos, candidatos rejeitados e erros de infraestrutura. Na cascata, a
camada semântica só é consultada depois de miss exato; sua taxa de hit usa esse subconjunto.

## Exercício

Descreva o que deve acontecer se a inferência funciona, mas a gravação no cache falha. Compare
com falha de leitura antes da inferência e com dois misses concorrentes.
