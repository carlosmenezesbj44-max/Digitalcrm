from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime
import enum

# Tabela associativa para many-to-many entre usuários e permissões
usuario_permissao = Table(
    'usuario_permissao',
    Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id')),
    Column('permissao_id', Integer, ForeignKey('permissao.id'))
)

# Tabela associativa para many-to-many entre grupos e permissões
grupo_permissao = Table(
    'grupo_permissao',
    Base.metadata,
    Column('grupo_id', Integer, ForeignKey('grupo.id')),
    Column('permissao_id', Integer, ForeignKey('permissao.id'))
)

# Tabela associativa para many-to-many entre usuários e grupos
usuario_grupo = Table(
    'usuario_grupo',
    Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id')),
    Column('grupo_id', Integer, ForeignKey('grupo.id'))
)

class TipoRole(str, enum.Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    TECNICO = "tecnico"
    CLIENTE = "cliente"

class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nome_completo = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True)
    role = Column(String(20), default=TipoRole.CLIENTE)
    foto_url = Column(String(255), nullable=True)
    preferencias = Column(String, nullable=True)
    
    # Campos para auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acesso = Column(DateTime, nullable=True)
    
    # Relacionamentos
    permissoes = relationship("Permissao", secondary=usuario_permissao, back_populates="usuarios")
    grupos = relationship("Grupo", secondary=usuario_grupo, back_populates="usuarios")
    logs_auditoria = relationship("AuditoriaLog", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario(username='{self.username}', email='{self.email}')>"

class Permissao(Base):
    __tablename__ = "permissao"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255))
    modulo = Column(String(50))  # clientes, faturamento, etc
    
    usuarios = relationship("Usuario", secondary=usuario_permissao, back_populates="permissoes")
    grupos = relationship("Grupo", secondary=grupo_permissao, back_populates="permissoes")

class Grupo(Base):
    __tablename__ = "grupo"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255))
    criado_em = Column(DateTime, default=datetime.utcnow)

    permissoes = relationship("Permissao", secondary=grupo_permissao, back_populates="grupos")
    usuarios = relationship("Usuario", secondary=usuario_grupo, back_populates="grupos")

class AuditoriaLog(Base):
    __tablename__ = "auditoria_log"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    acao = Column(String(100))  # create, update, delete, login
    recurso = Column(String(100))  # clientes, faturas, etc
    detalhes = Column(String(500))
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="logs_auditoria")
