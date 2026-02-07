#!/usr/bin/env python3
"""
Teste para verificar os planos cadastrados e tentar sincronizá-los com MikroTik
"""

from crm_modules.planos.service import PlanoService
from crm_modules.mikrotik.services import MikrotikService

def test_planos():
    """Testa a listagem de planos e sincronização com MikroTik"""
    # Listar planos ativos
    plano_service = PlanoService()
    planos = plano_service.listar_planos_ativos()
    print(f"Planos ativos: {len(planos)}")
    for plano in planos:
        print(f"ID: {plano.id}, Nome: {plano.nome}, Download: {plano.velocidade_download} Mbps, Upload: {plano.velocidade_upload} Mbps")
    
    # Tentar sincronizar
    print("\n=== Tentando sincronizar planos ===")
    mikrotik_service = MikrotikService()
    resultado = mikrotik_service.sincronizar_planos()
    print(f"Status: {resultado['status']}")
    print(f"Mensagem: {resultado['message']}")
    
    if resultado['resultados']:
        print("\nDetalhes dos resultados:")
        for r in resultado['resultados']:
            print(f"Plano {r['plano_nome']}:")
            print(f"  Status: {r['resultado']['status']}")
            print(f"  Mensagem: {r['resultado']['message']}")

if __name__ == "__main__":
    test_planos()