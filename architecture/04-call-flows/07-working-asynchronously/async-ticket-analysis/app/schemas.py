from pydantic import BaseModel, Field


class TicketRequest(BaseModel):
    """Entrada do endpoint: a mensagem do cliente."""

    message: str = Field(..., min_length=1, description="Mensagem do cliente no ticket de suporte")


class TicketAnalysis(BaseModel):
    """Resposta curta da análise síncrona."""

    category: str = Field(..., description="Categoria do ticket, ex: billing, technical, account")
    priority: str = Field(..., description="Prioridade: low, medium ou high")
    summary: str = Field(..., description="Resumo curto do problema relatado")


class FullTicketAnalysis(TicketAnalysis):
    """Resposta completa usada pelo job assíncrono."""

    recommended_action: str = Field(..., description="Recomendação inicial de tratamento")
