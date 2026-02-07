#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de multiplos servidores MikroTik
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_modules.mikrotik.integration import get_mikrotik_server

print("=== Teste de Multiplos Servidores MikroTik ===")
print("")

# Testar get_mikrotik_server sem ID
print("1. Servidor padrao (primeiro ativo):")
server1 = get_mikrotik_server()
if server1:
    print("   OK: " + str(server1.nome) + " (" + str(server1.ip) + ")")
else:
    print("   ERRO: Nenhum servidor encontrado")

# Testar get_mikrotik_server com ID=3 (sede)
print("")
print("2. Servidor ID 3 (sede):")
server2 = get_mikrotik_server(servidor_id=3)
if server2:
    print("   OK: " + str(server2.nome) + " (" + str(server2.ip) + ")")
else:
    print("   ERRO: Servidor nao encontrado")

# Testar get_mikrotik_server com ID=1 (vip)
print("")
print("3. Servidor ID 1 (vip):")
server3 = get_mikrotik_server(servidor_id=1)
if server3:
    print("   OK: " + str(server3.nome) + " (" + str(server3.ip) + ")")
else:
    print("   ERRO: Servidor nao encontrado")

# Testar ID inexistente
print("")
print("4. Servidor ID 999 (inexistente):")
server4 = get_mikrotik_server(servidor_id=999)
if server4:
    print("   ERRO: Servidor encontrado (nao deveria)")
else:
    print("   OK: Servidor nao encontrado (esperado)")

print("")
print("=== Teste Concluido ===")
