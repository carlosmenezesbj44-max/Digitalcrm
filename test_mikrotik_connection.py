#!/usr/bin/env python3
"""
Script de teste para conexão com MikroTik
"""

import sys
import os

# Adiciona o caminho do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_core.config.settings import settings
from crm_modules.mikrotik.integration import get_mikrotik_server, criar_profile_mikrotik, sincronizar_cliente_mikrotik

def test_mikrotik_connection():
    """Testa a conexão com o MikroTik"""
    print("=== Teste de Conexão com MikroTik ===\n")
    
    # Testa se as configurações estão definidas
    print("1. Verificando configurações do MikroTik:")
    print(f"   MIKROTIK_HOST: {settings.mikrotik_host}")
    print(f"   MIKROTIK_USER: {settings.mikrotik_user}")
    print(f"   MIKROTIK_PASSWORD: {'***' if settings.mikrotik_password else 'NÃO DEFINIDA'}")
    
    if not all([settings.mikrotik_host, settings.mikrotik_user, settings.mikrotik_password]):
        print("   ❌ Configurações do MikroTik não estão definidas no .env")
        print("   Por favor, configure as variáveis de ambiente:")
        print("   - MIKROTIK_HOST")
        print("   - MIKROTIK_USER") 
        print("   - MIKROTIK_PASSWORD")
        return False
    
    print("   ✅ Configurações básicas definidas")
    
    # Testa se há servidores no banco de dados
    print("\n2. Verificando servidores no banco de dados:")
    try:
        server = get_mikrotik_server()
        if server:
            print(f"   ✅ Servidor MikroTik encontrado: {server.nome} ({server.ip})")
            host = server.ip
            user = server.usuario
            password = server.senha
        else:
            print("   ⚠️  Nenhum servidor MikroTik encontrado no banco de dados")
            print("   Usando configurações do .env")
            host = settings.mikrotik_host
            user = settings.mikrotik_user
            password = settings.mikrotik_password
    except Exception as e:
        print(f"   ❌ Erro ao consultar banco de dados: {e}")
        return False
    
    # Testa a conexão real
    print(f"\n3. Testando conexão com MikroTik ({host}):")
    try:
        import routeros_api
        
        connection = routeros_api.RouterOsApiPool(
            host,
            username=user,
            password=password,
            port=8728,
            plaintext_login=True
        )
        api = connection.get_api()
        
        # Testa um comando simples
        system_resource = api.get_resource('/system/resource')
        info = system_resource.get()
        
        if info:
            print(f"   ✅ Conexão bem-sucedida!")
            print(f"   Dispositivo: {info[0].get('board-name', 'Desconhecido')}")
            print(f"   Versão RouterOS: {info[0].get('version', 'Desconhecido')}")
        else:
            print("   ⚠️  Conexão estabelecida, mas sem informações do sistema")
        
        connection.disconnect()
        
    except Exception as e:
        print(f"   ❌ Erro ao conectar ao MikroTik: {e}")
        print("   Possíveis causas:")
        print("   - IP incorreto")
        print("   - Credenciais inválidas")
        print("   - Porta 8728 bloqueada")
        print("   - Firewall bloqueando a conexão")
        return False
    
    # Testa a criação de profile
    print(f"\n4. Testando criação de profile PPPoE:")
    try:
        success = criar_profile_mikrotik(
            name="test_profile",
            download_limit=10,
            upload_limit=5,
            host=host,
            user=user,
            secret=password
        )
        
        if success:
            print("   ✅ Profile criado/atualizado com sucesso")
        else:
            print("   ❌ Falha ao criar profile")
            
    except Exception as e:
        print(f"   ❌ Erro ao criar profile: {e}")
    
    # Testa a sincronização de cliente
    print(f"\n5. Testando sincronização de cliente:")
    try:
        sincronizar_cliente_mikrotik(
            username="test_user",
            password="test_password",
            profile="default",
            host=host,
            user=user,
            secret=password
        )
        print("   ✅ Sincronização de cliente concluída")
        
    except Exception as e:
        print(f"   ❌ Erro na sincronização: {e}")
    
    print("\n=== Teste concluído ===")
    return True

if __name__ == "__main__":
    test_mikrotik_connection()