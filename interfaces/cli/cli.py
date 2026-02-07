import typer
from crm_modules.clientes.service import ClienteService

app = typer.Typer()


@app.command()
def create_cliente(nome: str, email: str, telefone: str, cpf: str, endereco: str):
    """Cria um novo cliente."""
    service = ClienteService()
    cliente = service.criar_cliente({
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cpf": cpf,
        "endereco": endereco
    })
    typer.echo(f"Cliente criado: {cliente.id}")


@app.command()
def list_clientes():
    """Lista todos os clientes ativos."""
    service = ClienteService()
    clientes = service.listar_clientes_ativos()
    for cliente in clientes:
        typer.echo(f"{cliente.id}: {cliente.nome} - {cliente.email}")


if __name__ == "__main__":
    app()
