import sys
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Erro: OPENAI_API_KEY não configurada")
    sys.exit(1)

model = os.getenv("OPENAI_MODEL", "gpt-4-mini")

if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
else:
    question = "O que é uma AI Gateway e por que ela é importante em aplicações com IA?"

system_prompt = """Você é um arquiteto de software explicando IA para desenvolvedores. Responda de forma didática, prática e objetiva. O tema é AI Gateway. Explique o conceito conectando com problemas reais de aplicações que chamam modelos de IA em produção."""

try:
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    print(f"Modelo: {model}")
    print(f"Pergunta: {question}")
    print(f"Resposta:\n{response.choices[0].message.content}")

except Exception as e:
    print(f"Erro ao chamar OpenAI: {e}")
    sys.exit(1)
