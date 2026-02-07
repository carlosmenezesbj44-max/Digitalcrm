"""Script para corrigir status no banco de dados"""
from crm_core.db.base import get_db_session
from sqlalchemy import text

db = get_db_session()

try:
    print("=== VERIFICANDO STATUS DOS CONTRATOS ===\n")
    
    # Verificar os status atuais
    result = db.execute(text("SELECT id, titulo, status_assinatura FROM contratos"))
    contratos = result.fetchall()
    
    print(f"Encontrados {len(contratos)} contrato(s):\n")
    
    for contrato in contratos:
        print(f"ID: {contrato[0]} | Título: {contrato[1]} | Status: '{contrato[2]}'")
    
    print("\n=== CORRIGINDO STATUS INVÁLIDOS ===\n")
    
    # Corrigir status em maiúsculo para minúsculo
    updates = [
        ("AGUARDANDO", "aguardando"),
        ("ASSINADO", "assinado"),
        ("LIBERADO", "liberado")
    ]
    
    total_corrigidos = 0
    for status_antigo, status_novo in updates:
        result = db.execute(
            text("UPDATE contratos SET status_assinatura = :novo WHERE status_assinatura = :antigo"),
            {"novo": status_novo, "antigo": status_antigo}
        )
        if result.rowcount > 0:
            print(f"✅ Corrigidos {result.rowcount} contrato(s) de '{status_antigo}' → '{status_novo}'")
            total_corrigidos += result.rowcount
    
    db.commit()
    
    if total_corrigidos == 0:
        print("✅ Todos os status já estão corretos!")
    else:
        print(f"\n✅ Total de {total_corrigidos} status corrigidos!")
    
    # Verificar novamente
    print("\n=== STATUS APÓS CORREÇÃO ===\n")
    result = db.execute(text("SELECT id, titulo, status_assinatura FROM contratos"))
    contratos = result.fetchall()
    
    for contrato in contratos:
        print(f"ID: {contrato[0]} | Título: {contrato[1]} | Status: '{contrato[2]}'")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    db.rollback()
    import traceback
    traceback.print_exc()
finally:
    db.close()
