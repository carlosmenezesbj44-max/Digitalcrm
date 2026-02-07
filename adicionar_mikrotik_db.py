#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar servidor MikroTik ao banco de dados
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crm_core.db.base import get_db_session
from crm_modules.servidores.models import ServidorModel
from crm_modules.servidores.repository import ServidorRepository


def adicionar_servidor_mikrotik():
    """Adiciona um servidor MikroTik ao banco de dados"""
    print("=== Adicionar Servidor MikroTik ===")
    print("")
    
    # Dados do servidor
    nome = "MikroTik Principal"
    ip = "200.200.1.1"  # IP DO MIKROTIK
    usuario = "admin"
    senha = "admin"  # SENHA DO MIKROTIK
    tipo_conexao = "mikrotik"
    tipo_acesso = "api"
    ativo = True
    
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        
        # Verificar se ja existe
        existente = repo.get_by_ip(ip)
        if existente:
            print("[JA EXISTE] Servidor ja cadastrado:")
            print(f"  ID: {existente.id}")
            print(f"  Nome: {existente.nome}")
            print(f"  IP: {existente.ip}")
            return False
        
        # Criar novo servidor
        servidor = ServidorModel(
            nome=nome,
            ip=ip,
            tipo_conexao=tipo_conexao,
            tipo_acesso=tipo_acesso,
            usuario=usuario,
            senha=senha,
            ativo=ativo
        )
        
        repo.create(servidor)
        print("[OK] Servidor MikroTik adicionado com sucesso!")
        print(f"  Nome: {nome}")
        print(f"  IP: {ip}")
        print(f"  Usuario: {usuario}")
        return True
        
    except Exception as e:
        print(f"[ERRO] Erro ao adicionar servidor: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # IMPORTANTE: Edite as variaveis acima com os dados corretos!
    print("ANTES DE EXECUTAR: Edite o script e coloque o IP e senha corretos")
    print("")
    adicionar_servidor_mikrotik()
