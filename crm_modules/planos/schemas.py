from pydantic import BaseModel
from typing import Optional


class PlanoCreate(BaseModel):
    nome: str
    velocidade_download: int
    velocidade_upload: int
    valor_mensal: float
    descricao: Optional[str] = None
    ativo: bool = True


class PlanoUpdate(BaseModel):
    nome: Optional[str] = None
    velocidade_download: Optional[int] = None
    velocidade_upload: Optional[int] = None
    valor_mensal: Optional[float] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None


class PlanoResponse(BaseModel):
    id: int
    nome: str
    velocidade_download: int
    velocidade_upload: int
    valor_mensal: float
    descricao: Optional[str] = None
    ativo: bool = True