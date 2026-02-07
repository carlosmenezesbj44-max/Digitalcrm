"""Modelos SQLAlchemy para Contratos"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime
import enum


class StatusAssinatura(enum.Enum):
    AGUARDANDO = "aguardando"
    ASSINADO = "assinado"
    LIBERADO = "liberado"


class TipoContrato(enum.Enum):
    SERVICO = "servico"
    ASSINATURA = "assinatura"
    MANUTENCAO = "manutencao"
    SUPORTE = "suporte"
    OUTRO = "outro"


class StatusRenovacao(enum.Enum):
    NAO_RENOVAVEL = "nao_renovavel"
    RENOVACAO_AUTOMATICA = "renovacao_automatica"
    RENOVACAO_MANUAL = "renovacao_manual"
    EXPIRADO = "expirado"


class ContratoModel(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    status_assinatura = Column(Enum(StatusAssinatura, values_callable=lambda x: [e.value for e in x]), default=StatusAssinatura.AGUARDANDO)
    tipo_contrato = Column(Enum(TipoContrato, values_callable=lambda x: [e.value for e in x]), default=TipoContrato.SERVICO)
    
    # Datas críticas
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_assinatura = Column(DateTime, nullable=True)
    data_vigencia_inicio = Column(DateTime, nullable=True)
    data_vigencia_fim = Column(DateTime, nullable=True)
    data_notificacao_renovacao = Column(DateTime, nullable=True)
    
    # Financeiro
    valor_contrato = Column(Float, nullable=True)
    moeda = Column(String(3), default="BRL")
    desconto_total = Column(Float, default=0.0)
    juros_atraso_percentual = Column(Float, default=1.0)  # 1% ao mês por padrão
    
    # Pagamentos
    data_primeiro_pagamento = Column(DateTime, nullable=True)
    data_proximo_pagamento = Column(DateTime, nullable=True)
    dia_pagamento = Column(Integer, default=10)  # Dia do mês para vencimento (1-31)
    frequencia_pagamento = Column(String(50), default="mensal")  # mensal, bimestral, trimestral, semestral, anual
    
    # Arquivo e assinatura
    arquivo_contrato = Column(String)
    hash_assinatura = Column(String, nullable=True)
    assinatura_digital = Column(Text, nullable=True)
    assinado_por = Column(String, nullable=True)
    
    # Renovação
    status_renovacao = Column(Enum(StatusRenovacao, values_callable=lambda x: [e.value for e in x]), default=StatusRenovacao.RENOVACAO_MANUAL)
    proximo_contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=True)
    
    # Observações
    observacoes = Column(Text)
    
    # Auditoria
    criado_por = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_por = Column(String, nullable=True)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletado_em = Column(DateTime, nullable=True)

    # Relacionamentos
    cliente = relationship("ClienteModel", back_populates="contratos")
    historiador = relationship("ContratoHistoricoModel", back_populates="contrato", cascade="all, delete-orphan", lazy="dynamic")


class ContratoHistoricoModel(Base):
    __tablename__ = "contratos_historico"
    
    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    
    # O que mudou
    campo_alterado = Column(String(100), nullable=False)
    valor_anterior = Column(String, nullable=True)
    valor_novo = Column(String, nullable=True)
    
    # Quem e quando
    alterado_por = Column(String, nullable=False)
    alterado_em = Column(DateTime, default=datetime.utcnow)
    
    # Contexto
    motivo = Column(String(500), nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Relacionamento
    contrato = relationship("ContratoModel", back_populates="historiador")


class ContratoTemplate(Base):
    __tablename__ = "contrato_templates"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    tipo_contrato = Column(Enum(TipoContrato, values_callable=lambda x: [e.value for e in x]), default=TipoContrato.SERVICO)
    template_html = Column(Text, nullable=False)
    ativo = Column(Integer, default=1)  # 1=ativo, 0=inativo

    # Auditoria
    criado_por = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_por = Column(String, nullable=True)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)