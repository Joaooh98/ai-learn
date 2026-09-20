from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    """Entrada do endpoint: a mensagem do cliente."""

    message: str = Field(
        ...,
        min_length=1,
        description="Mensagem do cliente no ticket de suporte",
    )


class TicketAnalysis(BaseModel):
    """Resposta estruturada que esperamos da IA e devolvemos ao cliente."""

    category: str = Field(..., description="Categoria do ticket, ex: billing, technical, account")
    priority: str = Field(..., description="Prioridade: low, medium ou high")
    summary: str = Field(..., description="Resumo curto do problema relatado")
