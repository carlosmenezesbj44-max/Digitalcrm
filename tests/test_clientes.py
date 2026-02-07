from crm_modules.clientes.service import ClienteService
from crm_modules.clientes.schemas import ClienteCreate
import uuid


def test_criar_cliente(db_session):
    service = ClienteService(db_session)
    token_int = uuid.uuid4().int
    email = f"joao_{token_int % 10**8}@example.com"
    cpf = f"{token_int % 10**11:011d}"
    cliente_data = ClienteCreate(
        nome="João Silva",
        email=email,
        telefone="123456789",
        cpf=cpf,
        endereco="Rua A, 123"
    )
    cliente = service.criar_cliente(cliente_data)
    assert cliente.nome == "João Silva"
    assert cliente.email == email


def test_listar_clientes_ativos(db_session):
    service = ClienteService(db_session)
    clientes = service.listar_clientes_ativos()
    assert isinstance(clientes, list)
