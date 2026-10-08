"""Aplicação FastAPI com fluxo síncrono e fluxo via streaming."""

import json

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from .ai_client import analyze_ticket, explain_ticket
from .schemas import TicketAnalysis, TicketRequest

app = FastAPI(title="Análise de Ticket de Suporte com IA")


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


@app.post("/tickets/explain")
def explain(request: TicketRequest) -> StreamingResponse:
    """Chama a IA com streaming e devolve a explicação textual em partes."""

    chunks = explain_ticket(request.message)

    try:
        first_chunk = next(chunks)
    except StopIteration:
        first_chunk = ""
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro ao iniciar a explicação com a IA.") from exc

    def body():
        yield first_chunk
        yield from chunks

    return StreamingResponse(body(), media_type="text/plain; charset=utf-8")
