from sqlalchemy import Column, Integer, String, Boolean
from crm_core.db.models_base import Base


class ServidorModel(Base):
    __tablename__ = "servidores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    tipo_conexao = Column(String, nullable=False)  # mikrotik, accel-ppp, huawei, cisco
    tipo_acesso = Column(String, nullable=False)  # ssh, telnet
    usuario = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    alterar_nome = Column(Boolean, default=True)
    ativo = Column(Boolean, default=True)