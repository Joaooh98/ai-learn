# Aula 12 — Governança mínima - acesso, custo e limites

[Índice do módulo](../README.md)

> Curso: **AI Gateways** · Duração: `03:41`

## Resumo

Quando IA passa a ser usada por várias aplicações, a camada compartilhada precisa de governança mínima. Não basta “funcionar”: é preciso saber quem pode usar, quanto pode gastar, quais limites existem e como auditar o uso.

Nesta aula, governança aparece como parte da arquitetura, não como burocracia externa.

## 1. Camada compartilhada de acesso

![Camada compartilhada](./01.png)

Aplicações web, mobile, serviços internos e APIs passam por uma camada técnica comum. Nessa camada entram:

- autenticação e autorização;
- validações e filtros;
- logs e traces;
- rate limit e quotas;
- cache e otimizações.

Centralizar acesso permite controlar visibilidade, segurança e uso responsável em escala.

## 2. Perguntas de governança

![Perguntas de uso](./02.png)

O gateway pode tomar decisões diferentes dependendo do contexto:

- é um modelo caro?
- é um processo em batch?
- é uma feature experimental?
- é usuário interno?

Com essas respostas, ele pode permitir, bloquear, rotear, limitar ou registrar de forma diferente.

## 3. Controle por chave

![Controle por chave](./03.png)

Cada chave pode ter limites próprios:

- requisições por minuto;
- tokens por minuto;
- orçamento diário;
- permissões por capacidade.

Em IA, custo não é apenas “número de chamadas”. O custo depende de modelo, tokens de entrada, tokens de saída e frequência.

## 4. Observabilidade e impacto arquitetural

![Observabilidade](./04.png)

Para cada chamada, é útil registrar:

- quem chamou;
- qual capacidade usou;
- qual modelo/deployment respondeu;
- quantos tokens foram consumidos;
- com que frequência acontece.

Sem esse nível de observabilidade, uma feature pode consumir quota compartilhada e afetar relatórios, fluxos internos ou experiências críticas.

## 5. Governança desde o início

![Governança por capacidade](./05.png)

Nem toda capacidade merece o mesmo tratamento. Uma classificação simples pode usar modelo barato, limite alto e política mais permissiva. Uma análise crítica pode usar modelo caro, limite baixo e controles mais rígidos.

## Ideia-chave

Governança mínima em AI Gateway significa responder três perguntas desde cedo: quem pode acessar, quanto pode gastar e até onde pode ir.

## Complemento — Limites precisam de escopo e evidência

RPM limita frequência; TPM limita volume de tokens por janela; concorrência limita chamadas simultâneas; orçamento limita gasto no período definido. Uma restrição não substitui as outras. Registre também como estimativas de tokens e gasto são atualizadas ao terminar ou falhar uma chamada.

Uma chamada pode ser autorizada para um modelo e inadequada para determinada informação ou finalidade. O produto precisa definir o escopo de uso, e a operação precisa aplicar a política em todas as rotas, inclusive fallback e cache.

**No repositório:** os Compose das aulas 14–18 não incluem banco, Redis, virtual keys por aplicação ou quotas. Eles demonstram acesso com master key e nomes lógicos. A [seção de governança](../README.md#governança-do-laboratório-e-da-operação) mostra o passo seguinte sem atribuir recursos ausentes ao exemplo.

Para avaliar uso em cache, diferencie consumo efetivo do provider, consumo lógico do produto e economia estimada. Os três podem divergir.
