from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from crm_core.db.models_base import Base


class ProdutoModel(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, unique=True)
    tipo = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    preco_custo = Column(Float, nullable=True)
    categoria = Column(String(100), nullable=False)
    unidade = Column(String(50), nullable=False)
    descricao = Column(Text, nullable=True)
    sku = Column(String(100), nullable=True, unique=True)
    codigo_barras = Column(String(100), nullable=True, unique=True)
    quantidade_estoque = Column(Float, default=0)
    estoque_minimo = Column(Float, default=0)
    ncm = Column(String(20), nullable=True)  # Código NCM para impostos
    cfop = Column(String(10), nullable=True)  # Código CFOP
    icms = Column(Float, default=0)  # Percentual ICMS
    fornecedor = Column(String(255), nullable=True)
    imagem_url = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True)

    # Campos de auditoria
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('usuario.id'), nullable=True)
