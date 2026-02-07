from pydantic import BaseModel
from typing import Optional


class PlanoBloqueioCreate(BaseModel):
    nome: str
    ip_privado: str
    reduzir_velocidade: bool = False
    dias_bloqueio: int
    tipo_bloqueio: str = "bloqueio_total"
    ativo: bool = True


class PlanoBloqueioUpdate(BaseModel):
    nome: Optional[str] = None
    ip_privado: Optional[str] = None
    reduzir_velocidade: Optional[bool] = None
    dias_bloqueio: Optional[int] = None
    tipo_bloqueio: Optional[str] = None
    ativo: Optional[bool] = None