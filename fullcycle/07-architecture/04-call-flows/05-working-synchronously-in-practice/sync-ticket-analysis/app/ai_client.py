"""Cliente de IA: encapsula a chamada SINCRONA (bloqueante) para a OpenAI."""

import json
import os

from openai import OpenAI

from .schemas import TicketAnalysis

client = OpenAI()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = (
    "Você é um assistente que analisa tickets de suporte. "
    "Responda SEMPRE em JSON válido, sem texto extra, com exatamente estas chaves: "
    '"category" (ex: billing, technical, account), '
    '"priority" (low, medium ou high) e '
    '"summary" (resumo curto do problema em português).'
)


def analyze_ticket(message: str) -> TicketAnalysis:
    """Chama a IA de forma síncrona e devolve a análise já validada."""

    completion = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    raw = completion.choices[0].message.content or ""
    data = json.loads(raw)
    return TicketAnalysis(**data)
