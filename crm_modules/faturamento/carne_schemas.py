from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ParcelaResponse(BaseModel):
    id: int
    numero_parcela: int
    valor: float
    data_vencimento: date
    status: str
    valor_pago: float
    data_pagamento: Optional[datetime]
    codigo_barras: Optional[str]
    linha_digitavel: Optional[str]
    gerencianet_charge_id: Optional[str]
    gerencianet_link_boleto: Optional[str]


class CarneCreate(BaseModel):
    cliente_id: int
    valor_total: float
    quantidade_parcelas: int  # ex: 12 para 12x
    data_inicio: date
    data_primeiro_vencimento: date
    intervalo_dias: int = 30
    descricao: Optional[str] = None
    gerar_boletos: bool = False  # Se True, gera boletos no Gerencianet


class CarneUpdate(BaseModel):
    valor_total: Optional[float] = None
    quantidade_parcelas: Optional[int] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    ativo: Optional[bool] = None


class CarneResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nome: Optional[str]
    numero_carne: str
    valor_total: float
    quantidade_parcelas: int
    valor_parcela: float
    data_inicio: date
    data_primeiro_vencimento: date
    intervalo_dias: int
    descricao: Optional[str]
    status: str
    gerencianet_subscription_id: Optional[str]
    data_criacao: datetime
    data_atualizacao: datetime
    parcelas: List[ParcelaResponse] = []


class BoletoCreate(BaseModel):
    cliente_id: int
    fatura_id: Optional[int] = None
    parcela_id: Optional[int] = None
    valor: float
    data_vencimento: date
    descricao: Optional[str] = None


class BoletoResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nome: Optional[str] = None
    numero_boleto: str
    valor: float
    data_vencimento: date
    codigo_barras: Optional[str]
    linha_digitavel: Optional[str]
    url_boleto: Optional[str]
    gerencianet_charge_id: Optional[str]
    gerencianet_status: str
    status: str
    data_emissao: datetime
    data_criacao: datetime
