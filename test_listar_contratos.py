"""Script para testar listagem de contratos"""
from crm_core.db.base import get_db_session
from crm_modules.contratos.repository import ContratoRepository

# Criar sessão
db = get_db_session()

try:
    print("=== LISTANDO CONTRATOS NO BANCO ===\n")
    
    repository = ContratoRepository(session=db)
    contratos = repository.list(limit=100, offset=0)
    
    if not contratos:
        print("❌ Nenhum contrato encontrado no banco de dados")
        print("   Crie um contrato primeiro usando: python test_criar_contrato.py")
    else:
        print(f"✅ Encontrados {len(contratos)} contrato(s):\n")
        
        for i, contrato in enumerate(contratos, 1):
            print(f"{i}. ID: {contrato.id}")
            print(f"   Título: {contrato.titulo}")
            print(f"   Cliente ID: {contrato.cliente_id}")
            print(f"   Status: {contrato.status_assinatura.value}")
            print(f"   Criado em: {contrato.data_criacao}")
            print(f"   PDF: {contrato.arquivo_contrato}")
            print()
        
        # Testar conversão para dict (como usado no template)
        print("=== TESTE DE CONVERSÃO PARA TEMPLATE ===\n")
        primeiro = contratos[0]
        contrato_dict = {
            "id": primeiro.id,
            "cliente_id": primeiro.cliente_id,
            "titulo": primeiro.titulo,
            "descricao": primeiro.descricao,
            "status_assinatura": primeiro.status_assinatura.value,
            "data_criacao": primeiro.data_criacao,
            "data_assinatura": primeiro.data_assinatura,
            "arquivo_contrato": primeiro.arquivo_contrato
        }
        
        print("Dicionário para template:")
        for key, value in contrato_dict.items():
            print(f"  {key}: {value}")
        
        print("\n✅ Status convertido corretamente:", contrato_dict['status_assinatura'])
        
finally:
    db.close()
