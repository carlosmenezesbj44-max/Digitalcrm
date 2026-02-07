from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime


class CarneModel(Base):
    """Modelo para planos de pagamento parcelado (carnês)"""
    __tablename__ = "carnes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_carne = Column(String, unique=True, nullable=False)  # e.g., "CARNE-2024-001"
    
    valor_total = Column(Float, nullable=False)
    quantidade_parcelas = Column(Integer, nullable=False)  # quantas parcelas
    valor_parcela = Column(Float, nullable=False)
    
    data_inicio = Column(Date, nullable=False)
    data_primeiro_vencimento = Column(Date, nullable=False)
    intervalo_dias = Column(Integer, default=30)  # dias entre parcelas
    
    descricao = Column(Text, nullable=True)
    status = Column(String, default="ativo")  # "ativo", "cancelado", "finalizado"
    ativo = Column(Boolean, default=True)
    
    # Integração Gerencianet
    gerencianet_subscription_id = Column(String, nullable=True)  # ID da recorrência no Gerencianet
    
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="carnes")
    parcelas = relationship("ParcelaModel", back_populates="carne", cascade="all, delete-orphan")


class ParcelaModel(Base):
    """Modelo para cada parcela do carnê"""
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True, index=True)
    carne_id = Column(Integer, ForeignKey("carnes.id"), nullable=False)
    numero_parcela = Column(Integer, nullable=False)  # 1, 2, 3...
    
    valor = Column(Float, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    
    status = Column(String, default="pendente")  # "pendente", "pago", "atrasado"
    valor_pago = Column(Float, default=0.0)
    data_pagamento = Column(DateTime, nullable=True)
    
    # Integração Gerencianet
    gerencianet_charge_id = Column(String, nullable=True)  # ID do boleto no Gerencianet
    gerencianet_link_boleto = Column(String, nullable=True)  # Link do boleto para download
    codigo_barras = Column(String, nullable=True)
    linha_digitavel = Column(String, nullable=True)
    
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    carne = relationship("CarneModel", back_populates="parcelas")


class BoletoModel(Base):
    """Modelo para boletos gerados (pode ser de fatura única ou parcela do carnê)"""
    __tablename__ = "boletos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    fatura_id = Column(Integer, ForeignKey("faturas.id"), nullable=True)  # Se for de fatura única
    parcela_id = Column(Integer, ForeignKey("parcelas.id"), nullable=True)  # Se for de carnê
    
    numero_boleto = Column(String, unique=True, nullable=False)
    valor = Column(Float, nullable=False)
    
    data_vencimento = Column(Date, nullable=False)
    data_emissao = Column(DateTime, default=datetime.utcnow)
    
    # Dados do boleto
    codigo_barras = Column(String, nullable=True)
    linha_digitavel = Column(String, nullable=True)
    url_boleto = Column(String, nullable=True)
    
    # Integração Gerencianet
    gerencianet_charge_id = Column(String, nullable=True, unique=True)
    gerencianet_status = Column(String, default="aberto")  # aberto, pago, cancelado, vencido
    
    status = Column(String, default="pendente")  # pendente, pago, cancelado
    ativo = Column(Boolean, default=True)
    
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="boletos")
    fatura = relationship("FaturaModel")
    parcela = relationship("ParcelaModel")
