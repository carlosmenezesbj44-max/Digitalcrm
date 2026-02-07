import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crm_core.db.models_base import Base
from interfaces.web.app import app
from crm_core.db.base import get_db
from crm_modules.servidores.service import ServidorService
from crm_modules.servidores.schemas import ServidorCreate

# Configurar banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas no banco de teste
Base.metadata.create_all(bind=engine)

# Dependency override para usar o banco de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    """Fixture para criar uma sessão de banco de dados para cada teste"""
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def servidor_service(db_session):
    """Fixture para criar uma instância do serviço de servidores"""
    return ServidorService(repository_session=db_session)

@pytest.fixture
def servidor_cadastrado(servidor_service):
    """Fixture para cadastrar um servidor de teste"""
    servidor_data = ServidorCreate(
        nome="Servidor Teste",
        ip="192.168.1.100",
        tipo_conexao="mikrotik",
        tipo_acesso="ssh",
        usuario="admin",
        senha="senha123",
        alterar_nome=True,
        ativo=True
    )
    return servidor_service.criar_servidor(servidor_data)

def test_criar_servidor(servidor_cadastrado):
    """Testar se o servidor é criado corretamente"""
    assert servidor_cadastrado.id is not None
    assert servidor_cadastrado.nome == "Servidor Teste"
    assert servidor_cadastrado.ip == "192.168.1.100"

def test_excluir_servidor(servidor_cadastrado, servidor_service):
    """Testar se o servidor é desativado ao excluir"""
    # Verificar que o servidor está ativo inicialmente
    assert servidor_cadastrado.ativo is True

    # Desativar o servidor
    servidor_service.desativar_servidor(servidor_cadastrado.id)

    # Recuperar o servidor novamente
    servidor_atualizado = servidor_service.obter_servidor(servidor_cadastrado.id)

    # Verificar que o servidor foi desativado
    assert servidor_atualizado.ativo is False

def test_listar_servidores_ativos(servidor_cadastrado, servidor_service):
    """Testar se apenas servidores ativos são listados"""
    # Listar servidores ativos
    servidores_ativos = servidor_service.listar_servidores_ativos()
    
    # Verificar que o servidor cadastrado está na lista
    assert len(servidores_ativos) == 1
    assert any(servidor.id == servidor_cadastrado.id for servidor in servidores_ativos)

def test_servidor_desativado_nao_listado(servidor_cadastrado, servidor_service):
    """Testar se servidor desativado não é listado"""
    # Desativar o servidor
    servidor_service.desativar_servidor(servidor_cadastrado.id)
    
    # Listar servidores ativos
    servidores_ativos = servidor_service.listar_servidores_ativos()
    
    # Verificar que o servidor desativado não está na lista
    assert len(servidores_ativos) == 0