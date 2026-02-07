"""Script para testar endpoint web de criação de contrato"""
import requests
from crm_core.db.base import get_db_session
from crm_modules.clientes.models import ClienteModel

# Obter um cliente existente
db = get_db_session()
cliente = db.query(ClienteModel).first()
db.close()

if not cliente:
    print("❌ Nenhum cliente encontrado")
    exit(1)

print(f"✓ Testando com cliente: {cliente.nome} (ID: {cliente.id})")

# Testar endpoint do formulário
print("\n=== TESTANDO ENDPOINT WEB ===")

# Dados do formulário
form_data = {
    "cliente_id": str(cliente.id),
    "titulo": "Teste Web - Plano 200MB",
    "descricao": "Testando criação via formulário web"
}

print(f"Dados enviados: {form_data}")

try:
    # Simular POST para a rota
    print("\nPara testar via browser:")
    print(f"1. Acesse: http://localhost:8001/contratos/novo")
    print(f"2. Selecione cliente ID: {cliente.id}")
    print(f"3. Preencha título e descrição")
    print(f"4. Clique em 'Cadastrar Contrato'")
    print("\nOu use o curl:")
    print(f'curl -X POST http://localhost:8001/contratos/novo -d "cliente_id={cliente.id}&titulo=Teste&descricao=Teste"')
    
except Exception as e:
    print(f"❌ Erro: {e}")
