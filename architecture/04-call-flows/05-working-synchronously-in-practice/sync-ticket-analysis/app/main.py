"""Aplicação FastAPI: demonstra a chamada SINCRONA para a IA."""

import json

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from .ai_client import analyze_ticket
from .schemas import TicketAnalysis, TicketRequest

app = FastAPI(title="Análise de Ticket de Suporte com IA (síncrono)")


@app.post("/tickets/analyze", response_model=TicketAnalysis)
def analyze(request: TicketRequest) -> TicketAnalysis:
    """Recebe a mensagem, chama a IA e devolve a análise estruturada."""

    try:
        return analyze_ticket(request.message)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="A IA retornou um JSON inválido.") from exc
    except ValidationError as exc:
        raise HTTPException(status_code=500, detail="A resposta da IA não tem o formato esperado.") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro ao chamar a IA.") from exc
