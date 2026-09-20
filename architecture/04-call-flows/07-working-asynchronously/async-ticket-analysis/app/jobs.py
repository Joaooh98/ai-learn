"""Armazenamento de jobs EM MEMORIA - apenas didático."""

import uuid

# job_id -> {"job_id", "status", "result"?, "error"?}
_jobs: dict[str, dict] = {}


def create_job() -> str:
    """Cria um job com status inicial 'pending' e devolve seu id único."""

    job_id = "job_" + uuid.uuid4().hex[:8]
    _jobs[job_id] = {"job_id": job_id, "status": "pending"}
    return job_id


def get_job(job_id: str) -> dict | None:
    """Devolve o job ou None se não existir."""

    return _jobs.get(job_id)


def mark_processing(job_id: str) -> None:
    _jobs[job_id]["status"] = "processing"


def mark_completed(job_id: str, result: dict) -> None:
    _jobs[job_id]["status"] = "completed"
    _jobs[job_id]["result"] = result


def mark_failed(job_id: str, error: str) -> None:
    _jobs[job_id]["status"] = "failed"
    _jobs[job_id]["error"] = error
