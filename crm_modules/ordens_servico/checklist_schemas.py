from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


class ChecklistItemBase(BaseModel):
    tipo_servico: str
    nome_tarefa: str
    descricao: Optional[str] = None
    ordem: int = 0
    ativo: bool = True


class ChecklistItemCreate(ChecklistItemBase):
    pass


class ChecklistItem(ChecklistItemBase):
    id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)


class ChecklistProgressBase(BaseModel):
    ordem_servico_id: int
    item_id: int
    completado: bool = False
    observacoes: Optional[str] = None


class ChecklistProgress(ChecklistProgressBase):
    id: int
    data_completado: Optional[datetime] = None
    completado_por: Optional[str] = None
    criado_automaticamente: bool = True

    model_config = ConfigDict(from_attributes=True)


class ChecklistItemWithProgress(BaseModel):
    """Item do checklist com informações de progresso"""
    id: int
    nome_tarefa: str
    descricao: Optional[str] = None
    ordem: int
    completado: bool
    data_completado: Optional[datetime] = None
    completado_por: Optional[str] = None
    observacoes: Optional[str] = None


class ChecklistProgressSummary(BaseModel):
    """Resumo do progresso do checklist"""
    total: int
    completed: int
    percentage: float
    is_complete: bool


class ChecklistResponse(BaseModel):
    """Resposta completa do checklist"""
    ordem_servico_id: int
    tipo_servico: str
    items: list[ChecklistItemWithProgress]
    summary: ChecklistProgressSummary


class ToggleItemRequest(BaseModel):
    completado_por: Optional[str] = None
    observacoes: Optional[str] = None


class UpdateObservacoesRequest(BaseModel):
    observacoes: str
