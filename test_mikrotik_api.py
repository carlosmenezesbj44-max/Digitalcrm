#!/usr/bin/env python3
"""
Teste da API REST do MikroTik
"""

import requests
import json

# Configurações
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1/mikrotik"

# Token de autenticação (substitua pelo token real)
TOKEN = "seu_token_aqui"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def test_mikrotik_api():
    """Testa a API REST do MikroTik"""
    print("=== Teste da API REST do MikroTik ===\n")
    
    # 1. Testar status do MikroTik
    print("1. Testando status do MikroTik:")
    try:
        response = requests.get(f"{API_BASE}/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   ✅ Servidor: {data['server']['name']} ({data['server']['ip']})")
            print(f"   ✅ Total de secrets: {data['total_secrets']}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # 2. Testar criação de profile
    print("\n2. Testando criação de profile:")
    try:
        profile_data = {
            "name": "api_test_profile",
            "download_limit": 200,
            "upload_limit": 100
        }
        response = requests.post(f"{API_BASE}/profiles", 
                               headers=headers, 
                               json=profile_data)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ {data['message']}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # 3. Testar obtenção de profiles
    print("\n3. Testando obtenção de profiles:")
    try:
        response = requests.get(f"{API_BASE}/profiles", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Profiles encontrados: {len(data['profiles'])}")
            for profile in data['profiles'][-3:]:  # Mostra os 3 últimos
                print(f"     - {profile['name']}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # 4. Testar obtenção de secrets
    print("\n4. Testando obtenção de secrets:")
    try:
        response = requests.get(f"{API_BASE}/secrets", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Secrets encontrados: {len(data['secrets'])}")
            for secret in data['secrets'][-3:]:  # Mostra os 3 últimos
                print(f"     - {secret['name']}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # 5. Testar obtenção de sessões ativas
    print("\n5. Testando obtenção de sessões ativas:")
    try:
        response = requests.get(f"{API_BASE}/sessions", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Sessões ativas: {data['total']}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    # 6. Testar obtenção de logs
    print("\n6. Testando obtenção de logs:")
    try:
        response = requests.get(f"{API_BASE}/logs?limit=5", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Logs coletados: {data['total']}")
            if data['logs']:
                print("   Últimos logs:")
                for log in data['logs']:
                    print(f"     - {log.get('time', '')}: {log.get('message', '')}")
        else:
            print(f"   ❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")
    
    print("\n=== Teste da API concluído ===")


if __name__ == "__main__":
    test_mikrotik_api()