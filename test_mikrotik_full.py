#!/usr/bin/env python3
"""
Script completo de teste para o módulo MikroTik
"""

import sys
import os

# Adiciona o caminho do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_core.config.settings import settings
from crm_modules.mikrotik.integration import (
    get_mikrotik_server, 
    criar_profile_mikrotik, 
    sincronizar_cliente_mikrotik,
    coletar_logs_mikrotik,
    monitorar_sessoes_mikrotik
)

def test_mikrotik_full():
    """Testa todas as funcionalidades do MikroTik"""
    print("=== Teste Completo do Módulo MikroTik ===\n")
    
    # 1. Verificar configurações
    print("1. Verificando configurações:")
    server = get_mikrotik_server()
    if server:
        print(f"   ✅ Servidor MikroTik encontrado: {server.nome} ({server.ip})")
        host = server.ip
        user = server.usuario
        password = server.senha
    else:
        print("   ⚠️  Nenhum servidor MikroTik no banco de dados")
        if all([settings.mikrotik_host, settings.mikrotik_user, settings.mikrotik_password]):
            print("   ✅ Usando configurações do .env")
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            password = settings.mikrotik_password
        else:
            print("   ❌ Configurações do MikroTik não definidas")
            return False
    
    # 2. Testar criação de profile
    print("\n2. Testando criação de profile:")
    try:
        success, msg = criar_profile_mikrotik(
            name="test_profile_full",
            download_limit=50,
            upload_limit=20,
            host=host,
            user=user,
            secret=password
        )
        if success:
            print("   ✅ Profile criado com sucesso")
        else:
            print("   ❌ Falha na criação do profile")
    except Exception as e:
        print(f"   ❌ Erro ao criar profile: {e}")
    
    # 3. Testar sincronização de cliente
    print("\n3. Testando sincronização de cliente:")
    try:
        sincronizar_cliente_mikrotik(
            username="test_client_full",
            password="test_password_123",
            profile="test_profile_full",
            host=host,
            user=user,
            secret=password
        )
        print("   ✅ Cliente sincronizado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro na sincronização: {e}")
    
    # 4. Testar coleta de logs
    print("\n4. Testando coleta de logs:")
    try:
        logs = coletar_logs_mikrotik(host=host, user=user, secret=password)
        if logs:
            print(f"   ✅ Coletados {len(logs)} logs")
            # Mostra os últimos 3 logs
            for log in logs[-3:]:
                print(f"     - {log.get('time', '')}: {log.get('message', '')}")
        else:
            print("   ⚠️  Nenhum log encontrado")
    except Exception as e:
        print(f"   ❌ Erro ao coletar logs: {e}")
    
    # 5. Testar monitoramento de sessões
    print("\n5. Testando monitoramento de sessões:")
    try:
        sessions = monitorar_sessoes_mikrotik(host=host, user=user, secret=password)
        if sessions:
            print(f"   ✅ Encontradas {len(sessions)} sessões ativas")
            for session in sessions[:3]:  # Mostra as 3 primeiras
                print(f"     - {session.get('name', '')}: {session.get('address', '')}")
        else:
            print("   ⚠️  Nenhuma sessão ativa")
    except Exception as e:
        print(f"   ❌ Erro ao monitorar sessões: {e}")
    
    print("\n=== Teste completo concluído ===")
    return True

if __name__ == "__main__":
    test_mikrotik_full()