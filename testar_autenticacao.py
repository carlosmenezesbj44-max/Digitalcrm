#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar o sistema de autenticação
Execute: python testar_autenticacao.py
"""

import requests
import json
import sys
import io

# Configurar encoding para suportar emojis no Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8001"

def registrar_usuario():
    """Registra um novo usuário"""
    print("\n📝 Registrando novo usuário...")
    
    dados = {
        "username": "admin",
        "email": "admin@example.com",
        "nome_completo": "Administrador",
        "senha": "senha123456",
        "role": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/usuarios/registrar", json=dados)
        if response.status_code == 201:
            usuario = response.json()
            print(f"✅ Usuário criado: {usuario['username']} ({usuario['email']})")
            return usuario
        else:
            erro = response.json()
            print(f"❌ Erro: {erro.get('detail', 'Erro desconhecido')}")
            return None
    except Exception as e:
        print(f"❌ Erro ao registrar: {str(e)}")
        return None

def fazer_login(username: str, senha: str):
    """Faz login e retorna token"""
    print(f"\n🔐 Fazendo login com {username}...")
    
    dados = {
        "username": username,
        "senha": senha
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/usuarios/login", json=dados)
        if response.status_code == 200:
            resultado = response.json()
            token = resultado['access_token']
            usuario = resultado['usuario']
            print(f"✅ Login bem-sucedido!")
            print(f"   Usuario: {usuario['username']}")
            print(f"   Email: {usuario['email']}")
            print(f"   Role: {usuario['role']}")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            erro = response.json()
            print(f"❌ Erro: {erro.get('detail', 'Erro desconhecido')}")
            return None
    except Exception as e:
        print(f"❌ Erro ao fazer login: {str(e)}")
        return None

def obter_perfil(token: str):
    """Obtém dados do usuário autenticado"""
    print(f"\n👤 Obtendo perfil do usuário...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/usuarios/me", headers=headers)
        if response.status_code == 200:
            usuario = response.json()
            print(f"✅ Perfil obtido:")
            print(f"   ID: {usuario['id']}")
            print(f"   Username: {usuario['username']}")
            print(f"   Email: {usuario['email']}")
            print(f"   Nome: {usuario['nome_completo']}")
            print(f"   Role: {usuario['role']}")
            print(f"   Ativo: {usuario['ativo']}")
            return usuario
        else:
            erro = response.json()
            print(f"❌ Erro: {erro.get('detail', 'Erro desconhecido')}")
            return None
    except Exception as e:
        print(f"❌ Erro ao obter perfil: {str(e)}")
        return None

def testar_token_invalido():
    """Testa requisição com token inválido"""
    print(f"\n🔒 Testando token inválido...")
    
    headers = {
        "Authorization": "Bearer token_invalido_123"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/usuarios/me", headers=headers)
        if response.status_code != 200:
            print(f"✅ Token inválido corretamente rejeitado (status {response.status_code})")
        else:
            print(f"❌ Token inválido foi aceito (isso é um problema!)")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def main():
    print("=" * 60)
    print("🚀 Teste do Sistema de Autenticação")
    print("=" * 60)
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code != 200:
            print("\n❌ Servidor não está respondendo em http://localhost:8001")
            print("   Inicie o servidor com: python -m uvicorn interfaces.web.app:app --reload")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao conectar ao servidor: {str(e)}")
        print("   Inicie o servidor com: python -m uvicorn interfaces.web.app:app --reload")
        sys.exit(1)
    
    # 1. Registrar usuário
    usuario = registrar_usuario()
    if not usuario:
        print("\n⚠️ Não foi possível registrar o usuário")
        print("   Pode ser que o usuário já exista. Continuando...")
    
    # 2. Fazer login
    token = fazer_login("admin", "senha123456")
    if not token:
        print("\n❌ Falha ao fazer login")
        sys.exit(1)
    
    # 3. Obter perfil
    perfil = obter_perfil(token)
    if not perfil:
        print("\n❌ Falha ao obter perfil")
        sys.exit(1)
    
    # 4. Testar token inválido
    testar_token_invalido()
    
    print("\n" + "=" * 60)
    print("✅ Todos os testes passaram!")
    print("=" * 60)
    print("\n📱 Acesse: http://localhost:8001/login")
    print("   Username: admin")
    print("   Senha: senha123456")

if __name__ == "__main__":
    main()
