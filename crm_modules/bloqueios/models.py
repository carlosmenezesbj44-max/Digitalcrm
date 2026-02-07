from sqlalchemy import Column, Integer, String, Boolean
from crm_core.db.models_base import Base


class PlanoBloqueioModel(Base):
    __tablename__ = "planos_bloqueio"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ip_privado = Column(String, nullable=False)  # IP privado para redirecionamento
    reduzir_velocidade = Column(Boolean, default=False)  # Se deve reduzir velocidade ou bloquear totalmente
    dias_bloqueio = Column(Integer, nullable=False)  # Dias após instalação para aplicar bloqueio
    tipo_bloqueio = Column(String, nullable=False, default="bloqueio_total")  # "bloqueio_total", "reducao_velocidade", "pagina_bloqueio"
    ativo = Column(Boolean, default=True)