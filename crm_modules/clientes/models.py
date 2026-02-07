from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime, date
from typing import Optional as TypingOptional


# Tabela de associação para Cliente e Produto (Muitos-para-Muitos)
cliente_produtos = Table(
    "cliente_produtos",
    Base.metadata,
    Column("cliente_id", Integer, ForeignKey("clientes.id"), primary_key=True),
    Column("produto_id", Integer, ForeignKey("produtos.id"), primary_key=True),
    Column("data_vinculo", DateTime, default=datetime.utcnow)
)


class ClienteModel(Base):
    __tablename__ = "clientes"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
    telefone: str = Column(String, nullable=False)
    whatsapp: TypingOptional[str] = Column(String, nullable=True)
    telefone_residencial: TypingOptional[str] = Column(String, nullable=True)
    telefone_comercial: TypingOptional[str] = Column(String, nullable=True)
    telefone_celular: TypingOptional[str] = Column(String, nullable=True)
    cpf: str = Column(String, unique=True, nullable=False)
    endereco: str = Column(String, nullable=False)
    cidade: TypingOptional[str] = Column(String, nullable=True)
    rua: TypingOptional[str] = Column(String, nullable=True)
    bairro: TypingOptional[str] = Column(String, nullable=True)
    cep: TypingOptional[str] = Column(String, nullable=True)
    condominio: TypingOptional[str] = Column(String, nullable=True)
    bloco: TypingOptional[str] = Column(String, nullable=True)
    estado: TypingOptional[str] = Column(String, nullable=True)
    tipo_localidade: TypingOptional[str] = Column(String, nullable=True)  # "urbana" ou "rural"
    tipo_cliente: str = Column(String, nullable=False, default="fisico")  # "fisico" ou "juridico"
    data_cadastro: datetime = Column(DateTime, default=datetime.utcnow)
    ativo: bool = Column(Boolean, default=True)
    nacionalidade: TypingOptional[str] = Column(String, nullable=True)
    rg: TypingOptional[str] = Column(String, nullable=True)
    orgao_emissor: TypingOptional[str] = Column(String, nullable=True)
    naturalidade: TypingOptional[str] = Column(String, nullable=True)
    data_nascimento: TypingOptional[date] = Column(Date, nullable=True)
    username: TypingOptional[str] = Column(String, nullable=True)
    observacoes: TypingOptional[str] = Column(String, nullable=True)
    instagram: TypingOptional[str] = Column(String, nullable=True)
    numero: TypingOptional[str] = Column(String, nullable=True)
    apartamento: TypingOptional[str] = Column(String, nullable=True)
    complemento: TypingOptional[str] = Column(String, nullable=True)
    moradia: TypingOptional[str] = Column(String, nullable=True)  # 'alugada' ou 'propria'
    latitude: TypingOptional[float] = Column(Float, nullable=True)
    longitude: TypingOptional[float] = Column(Float, nullable=True)
    plano_id: TypingOptional[int] = Column(Integer, nullable=True)
    velocidade: TypingOptional[int] = Column(Integer, nullable=True)
    data_instalacao: TypingOptional[date] = Column(Date, nullable=True)
    status_servico: TypingOptional[str] = Column(String, nullable=True, default="ativo")
    valor_mensal: TypingOptional[float] = Column(Float, nullable=True)
    valor_total: TypingOptional[float] = Column(Float, nullable=True)
    dia_vencimento: TypingOptional[int] = Column(Integer, nullable=True)
    servidor_id: TypingOptional[int] = Column(Integer, nullable=True)

    profile: TypingOptional[str] = Column(String, nullable=True)
    tipo_servico: TypingOptional[str] = Column(String, nullable=True, default="pppoe")
    comentario_login: TypingOptional[str] = Column(String, nullable=True)

    # Serviços adicionais
    servico_instalacao_equipamentos: bool = Column(Boolean, default=False)
    servico_suporte_premium: bool = Column(Boolean, default=False)
    servico_treinamentos: bool = Column(Boolean, default=False)
    servico_cortesia: bool = Column(Boolean, default=False)
    servico_wifi_publico: bool = Column(Boolean, default=False)
    servico_apps_parceiros: bool = Column(Boolean, default=False)
    servico_campanhas: bool = Column(Boolean, default=False)
    servico_personalizados: bool = Column(Boolean, default=False)
    servico_monitoramento: bool = Column(Boolean, default=False)
    servico_hospedagem: bool = Column(Boolean, default=False)
    servico_integracao: bool = Column(Boolean, default=False)
    servico_vas: bool = Column(Boolean, default=False)
    servico_streaming: bool = Column(Boolean, default=False)
    servico_backup: bool = Column(Boolean, default=False)
    servico_colaboracao: bool = Column(Boolean, default=False)

    # Histórico de serviços
    historico_chamados: bool = Column(Boolean, default=False)
    historico_instalacoes: bool = Column(Boolean, default=False)
    historico_upgrades: bool = Column(Boolean, default=False)

    # Status do cliente
    status_cliente: str = Column(String, nullable=False, default="conectado")  # "conectado", "pendencia", "bloqueio"

    # Plano de bloqueio aplicado (opcional)
    plano_bloqueio_id: TypingOptional[int] = Column(Integer, nullable=True)

    # Status de contrato
    status_contrato: str = Column(String, nullable=False, default="nenhum")  # "nenhum", "aguardando_assinatura", "assinado"
    
    # Foto da casa
    foto_casa: TypingOptional[str] = Column(String, nullable=True)

    # Relacionamentos (usando lazy loading com strings para evitar import circular)
    faturas = relationship("FaturaModel", back_populates="cliente", lazy="dynamic")
    carnes = relationship("CarneModel", back_populates="cliente", lazy="dynamic")
    boletos = relationship("BoletoModel", back_populates="cliente", lazy="dynamic")
    contratos = relationship("ContratoModel", back_populates="cliente", lazy="dynamic")
    arquivos = relationship("ClienteArquivoModel", backref="cliente", lazy="dynamic", cascade="all, delete-orphan")
    produtos = relationship("ProdutoModel", secondary=cliente_produtos, backref="clientes")

    def __init__(self, **kwargs):
        """Construtor que aceita parâmetros nomeados"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class ClienteConexaoLog(Base):
    __tablename__ = "cliente_conexao_logs"

    id: int = Column(Integer, primary_key=True, index=True)
    cliente_id: int = Column(Integer, nullable=False)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    status: str = Column(String, nullable=False)  # "online", "offline"
    ip_address: TypingOptional[str] = Column(String, nullable=True)
    latency_ms: TypingOptional[float] = Column(Float, nullable=True)
    session_id: TypingOptional[str] = Column(String, nullable=True)  # ID da sessão no router
