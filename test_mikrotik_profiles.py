#!/usr/bin/env python3
"""
Script para testar e corrigir a criação de profiles no MikroTik
"""

import sys
import os

# Adiciona o caminho do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_core.config.settings import settings
from crm_modules.mikrotik.integration import get_mikrotik_server

def test_mikrotik_profiles():
    """Testa a criação de profiles no MikroTik"""
    print("=== Teste de Profiles no MikroTik ===\n")
    
    # Obtém as configurações
    server = get_mikrotik_server()
    if server:
        host = server.ip
        user = server.usuario
        password = server.senha
        print(f"Usando servidor: {server.nome} ({host})")
    else:
        host = settings.mikrotik_host
        user = settings.mikrotik_user
        password = settings.mikrotik_password
        print(f"Usando configurações do .env: {host}")
    
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
        
        # 1. Verificar pools existentes
        print("1. Verificando pools de endereços:")
        try:
            pools = api.get_resource('/ip/pool').get()
            if pools:
                for pool in pools:
                    print(f"   Pool: {pool['name']} - {pool['ranges']}")
            else:
                print("   Nenhum pool encontrado")
        except Exception as e:
            print(f"   Erro ao listar pools: {e}")
        
        # 2. Verificar profiles existentes
        print("\n2. Verificando profiles PPPoE:")
        try:
            profiles = api.get_resource('/ppp/profile').get()
            if profiles:
                for profile in profiles:
                    print(f"   Profile: {profile['name']}")
                    if 'rate-limit' in profile:
                        print(f"     Rate Limit: {profile['rate-limit']}")
                    if 'local-address' in profile:
                        print(f"     Local Address: {profile['local-address']}")
                    if 'remote-address' in profile:
                        print(f"     Remote Address: {profile['remote-address']}")
            else:
                print("   Nenhum profile encontrado")
        except Exception as e:
            print(f"   Erro ao listar profiles: {e}")
        
        # 3. Testar criação de profile com configurações corretas
        print("\n3. Testando criação de profile:")
        
        # Primeiro, vamos criar um pool se não existir
        try:
            pools = api.get_resource('/ip/pool').get()
            pool_name = "pppoe-pool"
            
            if not any(pool['name'] == pool_name for pool in pools):
                print(f"   Criando pool {pool_name}...")
                api.get_resource('/ip/pool').add(
                    name=pool_name,
                    ranges="192.168.1.100-192.168.1.200"
                )
                print(f"   ✅ Pool {pool_name} criado")
            else:
                print(f"   Pool {pool_name} já existe")
        except Exception as e:
            print(f"   Erro ao criar pool: {e}")
        
        # Agora testar a criação do profile
        try:
            profile_name = "test_profile_corrigido"
            ppp_profiles = api.get_resource('/ppp/profile')
            
            # Verificar se já existe
            existing = ppp_profiles.get(name=profile_name)
            if existing:
                print(f"   Profile {profile_name} já existe, atualizando...")
                ppp_profiles.set(
                    id=existing[0]['id'],
                    rate_limit="5M/10M",
                    local_address="192.168.1.1",
                    remote_address=pool_name
                )
                print(f"   ✅ Profile {profile_name} atualizado")
            else:
                print(f"   Criando profile {profile_name}...")
                ppp_profiles.add(
                    name=profile_name,
                    rate_limit="5M/10M",
                    local_address="192.168.1.1",
                    remote_address=pool_name
                )
                print(f"   ✅ Profile {profile_name} criado")
                
        except Exception as e:
            print(f"   ❌ Erro ao criar profile: {e}")
        
        # 4. Testar criação de profile sem pool (usando ranges direto)
        print("\n4. Testando criação de profile sem pool:")
        try:
            profile_name = "test_profile_ranges"
            ppp_profiles = api.get_resource('/ppp/profile')
            
            # Verificar se já existe
            existing = ppp_profiles.get(name=profile_name)
            if existing:
                print(f"   Profile {profile_name} já existe, removendo...")
                ppp_profiles.remove(id=existing[0]['id'])
            
            print(f"   Criando profile {profile_name} com ranges...")
            ppp_profiles.add(
                name=profile_name,
                rate_limit="5M/10M",
                local_address="192.168.1.1",
                remote_address="192.168.1.100-192.168.1.200"
            )
            print(f"   ✅ Profile {profile_name} criado com ranges")
            
        except Exception as e:
            print(f"   ❌ Erro ao criar profile com ranges: {e}")
        
        connection.disconnect()
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False
    
    print("\n=== Teste concluído ===")
    return True

if __name__ == "__main__":
    test_mikrotik_profiles()