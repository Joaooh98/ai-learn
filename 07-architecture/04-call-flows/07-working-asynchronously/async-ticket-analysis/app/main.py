"""Aplicação FastAPI com fluxos síncrono, streaming e assíncrono."""

import json

from dotenv import load_dotenv

load_dotenv()

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from . import jobs
from .ai_client import analyze_ticket, explain_ticket, full_analysis
from .schemas import TicketAnalysis, TicketRequest

app = FastAPI(title="Análise de Ticket de Suporte com IA")


@app.post("/tickets/analyze", response_model=TicketAnalysis)
def analyze(request: TicketRequest) -> TicketAnalysis:
    """Fluxo 1: request espera a IA terminar e devolve JSON."""

    try:
        return analyze_ticket(request.message)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise HTTPException(status_code=500, detail="A resposta da IA não tem o formato esperado.") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erro ao chamar a IA.") from exc


@app.post("/tickets/explain")
def explain(request: TicketRequest) -> StreamingResponse:
    """Fluxo 2: request recebe texto em partes via streaming."""

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


def _process_job(job_id: str, message: str) -> None:
    """Roda fora da requisição HTTP via BackgroundTasks."""

    jobs.mark_processing(job_id)
    try:
        result = full_analysis(message)
        jobs.mark_completed(job_id, result.model_dump())
    except Exception:
        jobs.mark_failed(job_id, "Não foi possível concluir a análise do ticket.")


@app.post("/tickets/full-analysis")
def create_full_analysis(request: TicketRequest, background: BackgroundTasks) -> dict:
    """Cria o job e retorna imediatamente, sem esperar a IA."""

    job_id = jobs.create_job()
    background.add_task(_process_job, job_id, request.message)
    return {"job_id": job_id, "status": "pending"}


@app.get("/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    """Consulta o status/resultado do job pelo id."""

    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job não encontrado.")
    return job
