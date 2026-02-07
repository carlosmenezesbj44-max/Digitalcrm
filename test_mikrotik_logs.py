#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para coleta de logs do MikroTik
Usa o banco de dados para obter as configuracoes
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_core.db.base import get_db_session
from crm_modules.servidores.repository import ServidorRepository


def get_mikrotik_server_from_db():
    """Obtem o servidor MikroTik do banco de dados"""
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        servidores = repo.listar_servidores_ativos()
        mikrotik_servers = [s for s in servidores if s.tipo_conexao and s.tipo_conexao.lower() == 'mikrotik']
        
        # Filtrar por nome 'sede' se existir
        sede = [s for s in mikrotik_servers if s.nome and 'sede' in s.nome.lower()]
        if sede:
            return sede[0]
        
        # Se nao encontrar 'sede', usa o primeiro
        if mikrotik_servers:
            return mikrotik_servers[0]
        
        return None
    finally:
        db.close()


def test_mikrotik_logs():
    """Testa a coleta de logs do MikroTik"""
    print("=== Teste de Coleta de Logs do MikroTik ===")
    print("")
    
    # Obtem servidor do banco de dados
    server = get_mikrotik_server_from_db()
    
    if not server:
        print("[ERRO] Nenhum servidor MikroTik encontrado no banco de dados!")
        print("")
        print("Servidores ativos no banco:")
        db = get_db_session()
        repo = ServidorRepository(db)
        servidores = repo.listar_servidores_ativos()
        for s in servidores:
            print(f"  ID: {s.id}, Nome: {s.nome}, IP: {s.ip}, Tipo: {s.tipo_conexao}")
        db.close()
        return False
    
    print("Servidor encontrado:")
    print(f"  Nome: {server.nome}")
    print(f"  IP: {server.ip}")
    print(f"  Usuario: {server.usuario}")
    print("")
    
    # Testa a coleta de logs
    from crm_modules.mikrotik.integration import coletar_logs_mikrotik
    
    print("Conectando ao MikroTik...")
    try:
        logs = coletar_logs_mikrotik(
            host=server.ip,
            user=server.usuario,
            secret=server.senha
        )
        
        print("[OK] Conexao bem-sucedida!")
        print("Total de logs: " + str(len(logs)))
        print("")
        
        if logs:
            print("Ultimos 10 logs:")
            for i, log in enumerate(logs[:10]):
                time_val = log.get('time', 'N/A')
                topics_val = log.get('topics', 'INFO')
                message_val = log.get('message', '')
                print("  " + str(i+1) + ". [" + str(time_val) + "] " + str(topics_val) + ": " + str(message_val))
        else:
            print("[AVISO] Nenhum log encontrado")
            print("")
            print("Possiveis causas:")
            print("  - O usuario nao tem permissao para ler logs")
            print("  - Os logs estao desabilitados no MikroTik")
            print("  - O MikroTik nao tem logs registrados")
        
        return True
        
    except Exception as e:
        print("[ERRO] Erro ao coletar logs: " + str(e))
        print("")
        print("Possiveis causas:")
        print("  - IP incorreto")
        print("  - Credenciais invalidas")
        print("  - Porta 8728 bloqueada")
        print("  - Firewall bloqueando a conexao")
        return False


if __name__ == "__main__":
    test_mikrotik_logs()
