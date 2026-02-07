#!/usr/bin/env python3
"""
Teste para a rota /api/v1/mikrotik/servers
"""

from crm_core.db.base import get_db_session
from crm_modules.servidores.repository import ServidorRepository

def test_listar_servidores_mikrotik():
    """Testa a listagem de servidores MikroTik"""
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        servidores = repo.listar_todos()
        print(f"Servidores encontrados: {len(servidores)}")
        
        for s in servidores:
            print(f"ID: {s.id}, Nome: {s.nome}, IP: {s.ip}, Tipo: {s.tipo_conexao}, Ativo: {s.ativo}")
        
        mikrotik_servers = [
            {
                'id': s.id,
                'nome': s.nome,
                'ip': s.ip,
                'tipo_conexao': s.tipo_conexao,
                'ativo': s.ativo
            }
            for s in servidores if s.tipo_conexao and s.tipo_conexao.lower() == 'mikrotik'
        ]
        
        print(f"\nServidores MikroTik: {len(mikrotik_servers)}")
        for server in mikrotik_servers:
            print(server)
            
        return mikrotik_servers
        
    finally:
        db.close()

if __name__ == "__main__":
    print("Testando rota /api/v1/mikrotik/servers")
    print("=" * 50)
    test_listar_servidores_mikrotik()
    print("=" * 50)
    print("Teste concluído")