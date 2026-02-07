from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


class OrdemServicoBase(BaseModel):
    cliente_id: int
    tipo_servico: str
    titulo: str
    descricao: str
    prioridade: str = "normal"
    data_agendamento: Optional[datetime] = None
    tecnico_responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    valor: Optional[float] = None
    custo: Optional[float] = None
    endereco_servico: Optional[str] = None


class OrdemServicoCreate(OrdemServicoBase):
    pass


class OrdemServicoUpdate(BaseModel):
    tipo_servico: Optional[str] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    data_agendamento: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None
    tecnico_responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    valor: Optional[float] = None
    custo: Optional[float] = None
    endereco_servico: Optional[str] = None


class OrdemServico(OrdemServicoBase):
    id: int
    status: str
    data_criacao: datetime
    data_conclusao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)