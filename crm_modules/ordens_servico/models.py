from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from crm_core.db.models_base import Base
from datetime import datetime


class OrdemServicoModel(Base):
    __tablename__ = "ordens_servico"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    tipo_servico = Column(String, nullable=False)  # "instalacao", "manutencao", "reparo", "upgrade", etc.
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="aberta")  # "aberta", "em_andamento", "aguardando_peca", "concluida", "cancelada"
    prioridade = Column(String, nullable=False, default="normal")  # "baixa", "normal", "alta", "urgente"
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_agendamento = Column(DateTime, nullable=True)
    data_inicio = Column(DateTime, nullable=True)  # Quando a OS foi iniciada
    data_aguardando_peca = Column(DateTime, nullable=True)  # Quando entrou em espera de peça
    data_conclusao = Column(DateTime, nullable=True)
    tecnico_responsavel = Column(String, nullable=True)
    observacoes = Column(Text, nullable=True)
    valor_servico = Column(Float, nullable=True)
    custo_empresa = Column(Float, nullable=True)  # Custo para a empresa
    endereco_atendimento = Column(String, nullable=True)  # Se diferente do endereço do cliente