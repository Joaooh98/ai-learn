"""
Minimal application calling LiteLLM Proxy.

Architecture:

    Python application -> LiteLLM Proxy -> OpenAI

Important points:
1. The application does not call OpenAI directly.
2. The application calls LiteLLM Proxy over HTTP at http://localhost:4000.
3. The model is an internal gateway name: "developer-assistant".
4. The application does not know which real model is behind that name.
5. The OpenAI SDK is used only as an HTTP-compatible client.
"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL = "developer-assistant"

DEFAULT_QUESTION = (
    "O que e uma AI Gateway e por que ela e importante em aplicacoes com IA?"
)

SYSTEM_PROMPT = (
    "Voce e um arquiteto de software explicando IA para desenvolvedores. "
    "Responda de forma didatica, pratica e objetiva. O tema e AI Gateway. "
    "Explique o conceito conectando com problemas reais de aplicacoes que "
    "chamam modelos de IA em producao. Responda com 2 paragrafos."
)


def main() -> None:
    client = OpenAI(
        base_url="http://localhost:4000",
        api_key=os.environ["LITELLM_MASTER_KEY"],
    )

    question = " ".join(sys.argv[1:]).strip() or DEFAULT_QUESTION

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
    )

    print(f"Modelo:   {MODEL}")
    print(f"Pergunta: {question}")
    print()
    print("Resposta:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
