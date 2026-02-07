"""Script para testar criação de contrato"""
import sys
from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import ContratoCreate
from crm_core.db.base import get_db_session

# Criar sessão
db = get_db_session()

try:
    # Verificar se existe cliente
    from crm_modules.clientes.models import ClienteModel
    cliente = db.query(ClienteModel).first()
    
    if not cliente:
        print("❌ ERRO: Nenhum cliente encontrado no banco!")
        print("   Crie um cliente primeiro.")
        sys.exit(1)
    
    print(f"✓ Cliente encontrado: {cliente.nome} (ID: {cliente.id})")
    
    # Criar contrato de teste
    print("\n=== CRIANDO CONTRATO DE TESTE ===")
    
    contrato_data = ContratoCreate(
        cliente_id=cliente.id,
        titulo="Teste - Plano Internet 100MB",
        descricao="Contrato de teste para verificar funcionamento",
        valor_contrato=99.90,
        incluir_pdf=True
    )
    
    print(f"Dados do contrato: {contrato_data.dict()}")
    
    # Criar service e tentar criar contrato
    service = ContratoService(repository_session=db)
    
    print("\nTentando criar contrato...")
    contrato = service.criar_contrato(contrato_data, usuario_id="TESTE_SCRIPT")
    
    print(f"\n✅ SUCESSO! Contrato criado com ID: {contrato.id}")
    print(f"   Título: {contrato.titulo}")
    print(f"   Status: {contrato.status_assinatura}")
    print(f"   Arquivo PDF: {contrato.arquivo_contrato}")
    
except Exception as e:
    print(f"\n❌ ERRO ao criar contrato:")
    print(f"   Tipo: {type(e).__name__}")
    print(f"   Mensagem: {str(e)}")
    
    # Mostrar traceback completo
    import traceback
    print("\n=== TRACEBACK COMPLETO ===")
    traceback.print_exc()
    
finally:
    db.close()
