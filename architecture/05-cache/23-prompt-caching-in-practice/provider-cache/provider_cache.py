import logging
import os
import time
from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
PROMPT_CACHE_KEY = os.getenv("PROMPT_CACHE_KEY", "ticket-classifier-v1")


class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    ACCOUNT = "account"
    CANCELLATION = "cancellation"
    OTHER = "other"


class TicketAnalysis(BaseModel):
    category: TicketCategory
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str


class AnalyzerRequest(BaseModel):
    message: str


class AnalyzerResponse(BaseModel):
    provider_cache_hit: bool
    cached_tokens: int
    input_tokens: int
    output_tokens: int
    ai_calls: int
    elapsed_ms: int
    result: TicketAnalysis


# O prefixo precisa ser grande. Em produção, a parte estática (regras, políticas,
# exemplos e schemas de tools) costuma ser justamente o que mais pesa.
# Tudo abaixo é fixo; somente a mensagem do usuário, enviada depois, varia.
SYSTEM_PROMPT = """Você é um classificador de tickets de suporte de uma empresa \
de software por assinatura (SaaS). Sua única tarefa é ler a mensagem do cliente \
e classificá-la em exatamente UMA das cinco categorias descritas abaixo, \
seguindo rigorosamente as definições, os exemplos e as regras de desempate \
deste guia. Não responda ao cliente, não resolva o problema, não peça mais \
informações: apenas classifique.

## Categorias

### billing — cobrança, faturas e pagamentos
Use quando o assunto central é dinheiro: valores cobrados, faturas, boletos,
notas fiscais, cartão de crédito recusado, cobrança duplicada, reembolso,
estorno, mudança de plano por causa de preço, cupom de desconto que não foi
aplicado, dúvidas sobre o valor da renovação ou sobre impostos na fatura.
Exemplos típicos: "fui cobrado duas vezes este mês", "a fatura veio com valor
errado", "como emitir nota fiscal da assinatura?", "meu cartão foi recusado na
renovação", "quero o reembolso do mês passado", "o cupom BLACKFRIDAY não
funcionou no checkout".

### technical_support — erros, bugs e mau funcionamento
Use quando algo no produto não funciona como deveria: mensagens de erro,
telas que não carregam, lentidão, travamentos, funcionalidades que pararam de
funcionar, problemas de integração ou de API, falhas de sincronização, dados
que não aparecem, exportações que falham, aplicativo que fecha sozinho.
Exemplos típicos: "o dashboard não carrega desde ontem", "recebo erro 500 ao
salvar", "a integração com o Slack parou de enviar notificações", "o app
trava quando abro o relatório", "a exportação em CSV vem com colunas vazias".

### account — cadastro, login e acesso
Use quando o assunto é a conta do usuário em si: não conseguir fazer login,
recuperação ou troca de senha, e-mail de verificação que não chega,
autenticação em dois fatores, alteração de dados cadastrais (nome, e-mail,
CNPJ, endereço), gerenciamento de usuários e permissões da equipe, conta
bloqueada ou suspensa, exclusão de dados pessoais.
Exemplos típicos: "não consigo acessar minha conta", "não recebo o e-mail de
redefinição de senha", "quero trocar o e-mail de login", "como adiciono um
usuário com permissão de leitura?", "minha conta aparece como suspensa".

### cancellation — cancelamento de serviço ou assinatura
Use quando o cliente pede para encerrar a relação: cancelar a assinatura,
não renovar o contrato, encerrar a conta definitivamente, ou quando pergunta
sobre o processo, prazos e consequências do cancelamento (multa, fidelidade,
o que acontece com os dados após cancelar).
Exemplos típicos: "quero cancelar minha assinatura hoje", "como faço para não
renovar o plano anual?", "se eu cancelar, perco meus relatórios?", "qual a
multa para encerrar o contrato antes do prazo?".

### other — todo o resto
Use quando a mensagem não se encaixa com clareza em nenhuma das quatro
categorias acima: elogios, sugestões de funcionalidades, dúvidas comerciais
de quem ainda não é cliente, parcerias, imprensa, spam, mensagens vazias ou
incompreensíveis, perguntas sobre o uso normal do produto que não relatam
nenhum defeito ("como criar um relatório?" é dúvida de uso, não é bug).

## Regras de desempate

1. Cancelamento por causa de preço ("está caro demais, quero cancelar")
   é cancellation — a intenção de sair prevalece sobre o motivo financeiro.
2. Reclamação de cobrança APÓS cancelar ("cancelei e continuam me cobrando")
   é billing — o cancelamento já ocorreu; o problema atual é a cobrança.
3. Não conseguir PAGAR por erro do sistema (botão de pagamento quebrado,
   checkout com erro) é technical_support; dúvida sobre o VALOR é billing.
4. Não conseguir logar é account, mesmo que o cliente chame isso de "bug".
   Erro DENTRO do produto depois de logado é technical_support.
5. Ameaça vaga de cancelar no meio de outra reclamação ("resolvam ou vou
   cancelar") segue a reclamação principal, não cancellation.
6. Se ainda assim duas categorias parecerem igualmente plausíveis, escolha
   a mais específica; use other apenas como último recurso.

## Confiança

Reporte um número entre 0.0 e 1.0: acima de 0.9 quando a mensagem cita
explicitamente o assunto da categoria; entre 0.7 e 0.9 quando exige alguma
interpretação; abaixo de 0.7 quando a mensagem é curta, ambígua ou depende
de contexto que você não tem. A justificativa (reason) deve ter uma ou duas
frases, em português, citando o trecho da mensagem que motivou a escolha."""


# ChatOpenAI direto: o recurso é específico da OpenAI. include_raw=True mantém
# a AIMessage bruta, onde o LangChain normaliza os metadados de uso.
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0,
    model_kwargs={"prompt_cache_key": PROMPT_CACHE_KEY},
)

# invoke retorna {"raw": AIMessage, "parsed": TicketAnalysis,
# "parsing_error": Exception | None}.
analyzer = llm.with_structured_output(TicketAnalysis, include_raw=True)

ai_calls = 0


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("tickets")
logging.getLogger("httpx").setLevel(logging.WARNING)


def log_block(title: str, rows: list[tuple[str, str]]) -> None:
    """Bloco único por requisição: título e pares rótulo/valor alinhados."""
    rule = "─" * 64
    width = max(len(label) for label, _ in rows)
    lines = [rule, f"  {title}", rule]
    lines += [f"  {label.ljust(width)}  {value}" for label, value in rows]
    lines.append(rule)
    logger.info("\n".join(lines))


app = FastAPI(
    title="Analisador de Tickets — cache do provider (OpenAI)",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "model": OPENAI_MODEL,
        "prompt_cache_key": PROMPT_CACHE_KEY,
        "provider_cache": "automático na OpenAI para prompts de 1024+ tokens (prefixo exato)",
    }


@app.post("/tickets/analyze", response_model=AnalyzerResponse)
def analyze_ticket(payload: AnalyzerRequest) -> AnalyzerResponse:
    global ai_calls
    start = time.perf_counter()

    # Sempre chama a IA. Não existe cache de resposta nesta aplicação.
    # O que varia é quanto do prefixo o provider consegue reaproveitar.
    ai_calls += 1
    out = analyzer.invoke(
        [("system", SYSTEM_PROMPT), ("human", payload.message)]
    )
    result: TicketAnalysis = out["parsed"]

    # usage_metadata é o formato normalizado do LangChain para o uso da API.
    usage = out["raw"].usage_metadata or {}
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cached_tokens = usage.get("input_token_details", {}).get("cache_read", 0)
    hit = cached_tokens > 0

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    if hit:
        title = "PROVIDER CACHE HIT — OpenAI reaproveitou o prefixo (IA FOI chamada)"
        cached_line = (
            f"{cached_tokens}  ({cached_tokens / input_tokens:.0%} do input com desconto)"
        )
    else:
        title = "PROVIDER CACHE MISS — prefixo processado do zero (1ª chamada, TTL ou roteamento)"
        cached_line = "0  (o prefixo ainda não estava no cache do provider)"

    log_block(
        title,
        [
            ("message", payload.message),
            ("input_tokens", str(input_tokens)),
            ("cache_read", cached_line),
            (
                "output_tokens",
                f"{output_tokens}  (saída é sempre gerada e cobrada integral)",
            ),
            (
                "result",
                f"{result.category.value} (confiança {result.confidence:.2f})",
            ),
            ("ai_calls", str(ai_calls)),
            ("elapsed", f"{elapsed_ms}ms"),
        ],
    )

    return AnalyzerResponse(
        provider_cache_hit=hit,
        cached_tokens=cached_tokens,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        ai_calls=ai_calls,
        elapsed_ms=elapsed_ms,
        result=result,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("provider_cache:app", host="0.0.0.0", port=8001, reload=True)
