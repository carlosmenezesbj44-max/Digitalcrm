"""Schemas Pydantic para Contratos"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import enum


class StatusAssinatura(str, enum.Enum):
    AGUARDANDO = "aguardando"
    ASSINADO = "assinado"
    LIBERADO = "liberado"


class TipoContrato(str, enum.Enum):
    SERVICO = "servico"
    ASSINATURA = "assinatura"
    MANUTENCAO = "manutencao"
    SUPORTE = "suporte"
    OUTRO = "outro"


class StatusRenovacao(str, enum.Enum):
    NAO_RENOVAVEL = "nao_renovavel"
    RENOVACAO_AUTOMATICA = "renovacao_automatica"
    RENOVACAO_MANUAL = "renovacao_manual"
    EXPIRADO = "expirado"


class ContratoBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    cliente_id: int
    tipo_contrato: TipoContrato = TipoContrato.SERVICO
    data_vigencia_inicio: Optional[datetime] = None
    data_vigencia_fim: Optional[datetime] = None
    valor_contrato: Optional[float] = None
    moeda: str = "BRL"
    status_renovacao: StatusRenovacao = StatusRenovacao.RENOVACAO_MANUAL
    observacoes: Optional[str] = None
    
    # Campos de pagamento
    data_primeiro_pagamento: Optional[datetime] = None
    data_proximo_pagamento: Optional[datetime] = None
    dia_pagamento: int = 10  # Dia do mês (1-31)
    frequencia_pagamento: str = "mensal"  # mensal, bimestral, trimestral, semestral, anual
    desconto_total: float = 0.0
    juros_atraso_percentual: float = 1.0


class ContratoCreate(ContratoBase):
    incluir_pdf: bool = True


class ContratoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status_assinatura: Optional[StatusAssinatura] = None
    arquivo_contrato: Optional[str] = None
    observacoes: Optional[str] = None
    data_vigencia_fim: Optional[datetime] = None
    valor_contrato: Optional[float] = None
    status_renovacao: Optional[StatusRenovacao] = None


class ContratoResponse(ContratoBase):
    id: int
    status_assinatura: StatusAssinatura
    data_criacao: datetime
    data_assinatura: Optional[datetime] = None
    arquivo_contrato: Optional[str] = None
    hash_assinatura: Optional[str] = None
    assinado_por: Optional[str] = None
    criado_por: Optional[str] = None
    atualizado_por: Optional[str] = None
    atualizado_em: Optional[datetime] = None
    data_primeiro_pagamento: Optional[datetime] = None
    data_proximo_pagamento: Optional[datetime] = None
    dia_pagamento: int = 10
    frequencia_pagamento: str = "mensal"
    desconto_total: float = 0.0
    juros_atraso_percentual: float = 1.0

    class Config:
        from_attributes = True


class ContratoHistoricoResponse(BaseModel):
    id: int
    campo_alterado: str
    valor_anterior: Optional[str] = None
    valor_novo: Optional[str] = None
    alterado_por: str
    alterado_em: datetime
    motivo: Optional[str] = None

    class Config:
        from_attributes = True


class AssinaturaDigitalRequest(BaseModel):
    assinatura_base64: str
    hash_documento: str