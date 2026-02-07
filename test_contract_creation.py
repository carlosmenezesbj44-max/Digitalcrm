#!/usr/bin/env python3
"""
Test script to verify contract creation works after fixing the contratos_historico table issue
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crm_core.db.base import get_db_session
from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import ContratoCreate
from crm_modules.clientes.service import ClienteService
from crm_modules.clientes.schemas import ClienteCreate

def test_contract_creation():
    """Test creating a contract to verify the fix works"""
    db = get_db_session()
    try:
        print("Testing contract creation...")

        # First, create a test client if needed
        cliente_service = ClienteService(repository_session=db)
        clientes = cliente_service.listar_clientes()

        if not clientes:
            print("No clients found, creating a test client...")
            cliente_data = {
                "nome": "Cliente Teste",
                "email": "teste@example.com",
                "telefone": "11999999999",
                "cpf": "12345678901",
                "username": "cliente_teste",
                "password": "123456",
                "ativo": True
            }
            cliente_create = ClienteCreate(**cliente_data)
            cliente = cliente_service.criar_cliente(cliente_create)
            cliente_id = cliente.id
            print(f"Test client created with ID: {cliente_id}")
        else:
            cliente_id = clientes[0].id
            print(f"Using existing client with ID: {cliente_id}")

        # Now create a contract
        contrato_service = ContratoService(repository_session=db)
        contrato_data = {
            "titulo": "Contrato de Teste",
            "descricao": "Contrato criado para testar a correção da tabela contratos_historico",
            "cliente_id": cliente_id
        }

        contrato_create = ContratoCreate(**contrato_data)
        contrato = contrato_service.criar_contrato(contrato_create)

        print(f"Contract created successfully with ID: {contrato.id}")
        print(f"Contract status: {contrato.status_assinatura}")

        # Verify the history was created
        historico = contrato.historiador.all()
        print(f"Number of history records: {len(historico)}")

        if historico:
            print("History record details:")
            for h in historico:
                print(f"  - Field: {h.campo_alterado}, Old: {h.valor_anterior}, New: {h.valor_novo}")

        print("✅ Contract creation test PASSED!")
        return True

    except Exception as e:
        print(f"❌ Contract creation test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_contract_creation()
    sys.exit(0 if success else 1)
