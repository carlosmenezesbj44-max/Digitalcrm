from sqlalchemy import Column, Integer, String, Float, Boolean
from crm_core.db.models_base import Base
from typing import Optional as TypingOptional


class PlanoModel(Base):
    __tablename__ = "planos"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String, nullable=False)
    velocidade_download: int = Column(Integer, nullable=False)  # Mbps
    velocidade_upload: int = Column(Integer, nullable=False)  # Mbps
    valor_mensal: float = Column(Float, nullable=False)
    descricao: TypingOptional[str] = Column(String, nullable=True)
    ativo: bool = Column(Boolean, default=True)