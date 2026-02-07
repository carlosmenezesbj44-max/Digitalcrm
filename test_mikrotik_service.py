#!/usr/bin/env python3
"""
Teste do serviço MikroTik para operações em tempo real
"""

import sys
import os

# Adiciona o caminho do projeto ao Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_modules.mikrotik.services import MikrotikService

def test_mikrotik_service():
    """Testa o serviço MikroTik"""
    print("=== Teste do Serviço MikroTik ===\n")
    
    service = MikrotikService()
    
    # 1. Testar obtenção de configurações
    print("1. Testando obtenção de configurações:")
    config = service.obter_configuracoes()
    if config['status'] == 'success':
        print(f"   ✅ Servidor: {config['server']['name']} ({config['server']['ip']})")
        print(f"   ✅ Dispositivo: {config['server']['device']}")
        print(f"   ✅ Versão: {config['server']['version']}")
        print(f"   ✅ Total de secrets: {config['total_secrets']}")
    else:
        print(f"   ❌ Erro: {config['message']}")
        return False
    
    # 2. Testar criação de profile
    print("\n2. Testando criação de profile:")
    profile_result = service.criar_profile_real_time(
        name="test_service_profile",
        download_limit=100,
        upload_limit=50
    )
    print(f"   {profile_result['message']}")
    
    # 3. Testar sincronização de cliente
    print("\n3. Testando sincronização de cliente:")
    # Simular um cliente e contrato
    class MockCliente:
        def __init__(self):
            self.id = 1
            self.nome = "Teste Cliente"
    
    class MockContrato:
        def __init__(self):
            self.senha_pppoe = "test123"
            self.plano_internet = "test_service_profile"
    
    cliente = MockCliente()
    contrato = MockContrato()
    
    sync_result = service.sincronizar_cliente_real_time(cliente, contrato)
    print(f"   {sync_result['message']}")
    if sync_result['status'] == 'success':
        print(f"   Credenciais geradas: {sync_result['credentials']}")
    
    # 4. Testar bloqueio de cliente
    print("\n4. Testando bloqueio de cliente:")
    username = f"{cliente.nome.replace(' ', '_').lower()}_{cliente.id}"
    block_result = service.bloquear_cliente_real_time(username)
    print(f"   {block_result['message']}")
    
    # 5. Testar desbloqueio de cliente
    print("\n5. Testando desbloqueio de cliente:")
    unblock_result = service.desbloquear_cliente_real_time(username)
    print(f"   {unblock_result['message']}")
    
    # 6. Testar obtenção de sessões ativas
    print("\n6. Testando obtenção de sessões ativas:")
    sessions_result = service.obter_sessoes_ativas()
    if sessions_result['status'] == 'success':
        print(f"   ✅ Sessões ativas: {sessions_result['total']}")
    else:
        print(f"   ❌ Erro: {sessions_result['message']}")
    
    # 7. Testar obtenção de logs
    print("\n7. Testando obtenção de logs:")
    logs_result = service.obter_logs_recentes(limit=5)
    if logs_result['status'] == 'success':
        print(f"   ✅ Logs coletados: {logs_result['total']}")
        if logs_result['logs']:
            print("   Últimos logs:")
            for log in logs_result['logs'][:3]:
                print(f"     - {log.get('time', '')}: {log.get('message', '')}")
    else:
        print(f"   ❌ Erro: {logs_result['message']}")
    
    # 8. Testar atualização de credenciais
    print("\n8. Testando atualização de credenciais:")
    update_result = service.atualizar_credential_cliente(
        username=username,
        new_password="nova_senha_123",
        new_profile="test_service_profile"
    )
    print(f"   {update_result['message']}")
    
    print("\n=== Teste do serviço concluído ===")
    return True

if __name__ == "__main__":
    test_mikrotik_service()