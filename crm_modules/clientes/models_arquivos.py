from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from crm_core.db.models_base import Base
from datetime import datetime


class ClienteArquivoModel(Base):
    __tablename__ = "cliente_arquivos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    data_upload = Column(DateTime, default=datetime.utcnow, name="uploaded_at")
