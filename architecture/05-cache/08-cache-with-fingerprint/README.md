# Aula 08 — Cache com fingerprint

> Curso: **Cache** · Duração: `07:32`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Esta aula implementa, na prática, o conceito de fingerprint apresentado na aula 07, substituindo a
chave de cache bruta do cache exato (aula 06) por uma chave normalizada e mais robusta a pequenas
variações de entrada.

## O que a aula deve cobrir

- Função de normalização do prompt e dos parâmetros relevantes.
- Geração do fingerprint (ex.: hash) a partir da entrada normalizada.
- Uso do fingerprint como chave no padrão cache-aside já implementado na aula 06.
- Comparação de taxa de hit antes e depois da normalização, evidenciando o ganho do fingerprint
  sobre o cache exato ingênuo.

## Ideia-chave

O fingerprint fecha o bloco de cache exato do módulo: é o ponto de maior sofisticação possível
sem sair da ideia de "mesma entrada, mesma resposta". A partir da aula 09, o módulo muda de
categoria — de cache exato para cache **semântico**, baseado em significado, não em igualdade de
texto.
