from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from datetime import datetime
from crm_core.db.models_base import Base


class TecnicoModel(Base):
    __tablename__ = "tecnicos"

    # Informações Básicas
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=True)
    telefone_secundario = Column(String, nullable=True)
    cpf = Column(String, nullable=True, unique=True)
    data_nascimento = Column(DateTime, nullable=True)
    
    # Foto/Avatar
    foto_url = Column(String, nullable=True)
    
    # Endereço
    endereco_rua = Column(String, nullable=True)
    endereco_numero = Column(String, nullable=True)
    endereco_complemento = Column(String, nullable=True)
    endereco_bairro = Column(String, nullable=True)
    endereco_cidade = Column(String, nullable=True)
    endereco_estado = Column(String, nullable=True)
    endereco_cep = Column(String, nullable=True)
    
    # Profissional
    especialidades = Column(String, nullable=True)  # CSV: instalação, manutenção, reparo
    crea = Column(String, nullable=True)  # Número CREA se for engenheiro
    formacao = Column(String, nullable=True)
    experiencia_anos = Column(Integer, nullable=True)
    
    # Financeiro
    salario_taxa = Column(Float, nullable=True)
    banco = Column(String, nullable=True)
    agencia = Column(String, nullable=True)
    conta = Column(String, nullable=True)
    tipo_conta = Column(String, nullable=True)  # Corrente, Poupança
    
    # Emprego
    data_admissao = Column(DateTime, nullable=True)
    data_demissao = Column(DateTime, nullable=True)
    cargo = Column(String, nullable=True)
    
    # Status e Observações
    status = Column(String, default="ativo")  # ativo, inativo, férias, licença
    ativo = Column(Boolean, default=True)
    observacoes = Column(Text, nullable=True)
    
    # Auditoria
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
