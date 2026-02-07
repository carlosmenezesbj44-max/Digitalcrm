#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para debugar a lista de usuários
"""

import requests
import json

BASE_URL = "http://localhost:8001"

# 1. Login
print("Fazendo login...")
login_response = requests.post(f"{BASE_URL}/api/usuarios/login", json={
    "username": "admin",
    "senha": "senha123456"
})

if login_response.status_code != 200:
    print(f"Erro ao fazer login: {login_response.status_code}")
    print(login_response.json())
    exit(1)

token = login_response.json()['access_token']
print(f"Token: {token[:50]}...")

# 2. Listar usuários
print("\nListando usuários...")
headers = {
    "Authorization": f"Bearer {token}"
}

lista_response = requests.get(f"{BASE_URL}/api/usuarios/lista", headers=headers)
print(f"Status: {lista_response.status_code}")
print(f"Response: {json.dumps(lista_response.json(), indent=2, ensure_ascii=False)}")
