# Aula 02 — Hit, miss e cache-aside

> Curso: **Cache** · Duração: `04:06`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Antes de aplicar cache a chamadas de IA, a aula revisa o vocabulário e o padrão básico de cache
usados no resto do módulo: hit, miss e o padrão cache-aside.

## Conceitos

- **Hit**: a informação pedida já está no cache — retorna direto, sem tocar na fonte original.
- **Miss**: a informação não está no cache — é preciso buscar na fonte original (neste módulo, o
  modelo de IA) e, normalmente, gravar o resultado no cache para a próxima vez.
- **Cache-aside**: padrão em que a própria aplicação é responsável por consultar o cache antes,
  buscar na fonte em caso de miss, e gravar o resultado de volta no cache.

## Fluxo conceitual

```text
Aplicação -> consulta cache
  hit  -> retorna do cache
  miss -> chama a fonte original -> grava no cache -> retorna
```

## Ideia-chave

Cache-aside é o padrão mais simples e mais usado porque dá controle total à aplicação sobre
quando ler, quando escrever e quando invalidar — controle que se torna importante nas próximas
aulas, quando entram TTL, invalidação e cache semântico.
