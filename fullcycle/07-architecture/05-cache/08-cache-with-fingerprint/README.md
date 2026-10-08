# Aula 08 — Cache com fingerprint

> Curso: **Cache** · Duração: `07:32`

## Material e foco da aula

Os 21 prints mostram fingerprint em código, endpoints de configuração e mudança de chave
por versão. [05.png](05.png) registra a construção e o hash; [17.png](17.png) mostra configuração
alterada; [21.png](21.png) mostra acesso sob a versão anterior.

## Implementação observada

No [snapshot da aula](mba-ia-cache/README.md), as funções relevantes são:

```python
def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()

def build_fingerprint(message: str) -> dict:
    return {
        "prompt_version": runtime_config["prompt_version"],
        "rules_version": runtime_config["rules_version"],
        "model_capability": runtime_config["model_capability"],
        "normalized_text": normalize_text(message),
    }

def build_cache_key(fingerprint: dict) -> str:
    raw = json.dumps(fingerprint, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
```

O padrão continua cache-aside. `GET /config` consulta rótulos atuais; `PUT /config` os altera
em memória. A resposta da análise expõe chave e fingerprint para inspeção didática.

## Complemento de estudo: versão é um compromisso operacional

Alterar `prompt_version` **não edita o prompt**. Alterar `model_capability` **não troca o modelo**.
São rótulos para separar entradas; modelo e prompt são criados na inicialização.
Mantenha os rótulos sincronizados com mudanças reais.

Mudança de versão produz invalidação lógica, sem remover entradas. Se `prompt_v1` ainda estiver
em `CACHE`, voltar a essa versão pode restaurar o hit. O mesmo princípio vale para os filtros
de versão da tabela semântica. Configuração e cache em memória não são compartilhados entre workers.

`sort_keys=True` evita que a ordem das propriedades altere o JSON deste dicionário;
`ensure_ascii=False` mantém caracteres Unicode. [Referência: módulo `json` do Python](https://docs.python.org/3/library/json.html#json.dumps).

## Roteiro de verificação

1. Calcule duas vezes o fingerprint da mesma mensagem e configuração: as chaves devem coincidir.
2. Altere só `prompt_version`: a chave deve mudar.
3. Altere só `rules_version` ou `model_capability`: a chave também deve mudar.
4. Teste caixa e espaços: confira as variações que a normalização realmente aproxima.
5. Volte à versão original: verifique que a entrada anterior não foi apagada.

Essas verificações podem usar apenas funções puras. Requisições de inferência em
[test.http](mba-ia-cache/test.http) usam o provedor e podem ter custo.

## Limite desta etapa

Este snapshot termina no cache exato com fingerprint. Busca semântica e pgvector aparecem nas
aulas seguintes; por isso uma chave diferente nesta etapa leva a uma nova chamada ao modelo.
