from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime, date
from typing import Optional as TypingOptional


class FaturaModel(Base):
    __tablename__ = "faturas"

    id: int = Column(Integer, primary_key=True, index=True)
    cliente_id: int = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_fatura: str = Column(String, unique=True, nullable=False)  # e.g., "FAT-2024-001"
    data_emissao: datetime = Column(DateTime, default=datetime.utcnow)
    data_vencimento: date = Column(Date, nullable=False)
    valor_total: float = Column(Float, nullable=False)
    status: str = Column(String, nullable=False, default="pendente")  # "pendente", "pago", "atrasado"
    valor_pago: float = Column(Float, default=0.0)
    descricao: TypingOptional[str] = Column(String, nullable=True)
    ativo: bool = Column(Boolean, default=True)

    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="faturas")
    pagamentos = relationship("PagamentoModel", back_populates="fatura")


class PagamentoModel(Base):
    __tablename__ = "pagamentos"

    id: int = Column(Integer, primary_key=True, index=True)
    fatura_id: int = Column(Integer, ForeignKey("faturas.id"), nullable=False)
    valor_pago: float = Column(Float, nullable=False)
    data_pagamento: datetime = Column(DateTime, default=datetime.utcnow)
    metodo_pagamento: str = Column(String, nullable=False)  # e.g., "dinheiro", "cartao", "transferencia"
    referencia: TypingOptional[str] = Column(String, nullable=True)  # e.g., numero do recibo
    observacoes: TypingOptional[str] = Column(String, nullable=True)
    ativo: bool = Column(Boolean, default=True)

    # Relacionamentos
    fatura = relationship("FaturaModel", back_populates="pagamentos")