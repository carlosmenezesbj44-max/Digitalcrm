from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class FaturaCreate(BaseModel):
    cliente_id: int
    numero_fatura: str
    data_vencimento: date
    valor_total: float
    descricao: Optional[str] = None


class FaturaUpdate(BaseModel):
    numero_fatura: Optional[str] = None
    data_vencimento: Optional[date] = None
    valor_total: Optional[float] = None
    status: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None


class PagamentoCreate(BaseModel):
    fatura_id: int
    valor_pago: float
    metodo_pagamento: str
    referencia: Optional[str] = None
    observacoes: Optional[str] = None


class PagamentoUpdate(BaseModel):
    valor_pago: Optional[float] = None
    metodo_pagamento: Optional[str] = None
    referencia: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class FaturaResponse(BaseModel):
    id: int
    cliente_id: int
    numero_fatura: str
    data_emissao: datetime
    data_vencimento: date
    valor_total: float
    status: str
    valor_pago: float
    descricao: Optional[str]
    ativo: bool


class PagamentoResponse(BaseModel):
    id: int
    fatura_id: int
    numero_fatura: Optional[str] = None
    cliente_nome: Optional[str] = None
    cliente_id: Optional[int] = None
    valor_pago: float
    data_pagamento: datetime
    metodo_pagamento: str
    referencia: Optional[str]
    observacoes: Optional[str]
    ativo: bool