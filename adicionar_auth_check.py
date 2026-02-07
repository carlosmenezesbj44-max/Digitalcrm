#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar automaticamente auth-check.js em todas as páginas HTML

Uso: python adicionar_auth_check.py
"""

import os
import re
import sys
from pathlib import Path

# Forçar UTF-8 no Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Diretório das templates
TEMPLATES_DIR = "interfaces/web/templates"

# Páginas públicas que NÃO devem ter o script
PAGINAS_PUBLICAS = [
    "login.html",
    "registrar.html",
]

# String que procuramos
SEARCH_STR = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>'

# String que vamos adicionar DEPOIS
AUTH_SCRIPT = '<script src="/static/js/auth-check.js"></script>'

def adicionar_auth_check():
    """Adiciona auth-check.js em todos os HTML protegidos"""
    
    # Validar que auth-check.js existe
    auth_check_path = Path("interfaces/web/static/js/auth-check.js")
    if not auth_check_path.exists():
        print("❌ Arquivo auth-check.js não encontrado!")
        print(f"   Caminho esperado: {auth_check_path}")
        return False
    
    templates_path = Path(TEMPLATES_DIR)
    if not templates_path.exists():
        print(f"❌ Diretório {TEMPLATES_DIR} não encontrado!")
        return False
    
    # Encontrar todos os HTML
    html_files = sorted(templates_path.glob("*.html"))
    
    if not html_files:
        print(f"❌ Nenhum arquivo .html encontrado em {TEMPLATES_DIR}")
        return False
    
    print(f"\n📋 Encontrados {len(html_files)} arquivos HTML\n")
    
    modificados = 0
    pulados = 0
    erros = 0
    
    for html_file in html_files:
        filename = html_file.name
        
        # Pular páginas públicas
        if filename in PAGINAS_PUBLICAS:
            print(f"⏭️  {filename} (página pública - pulado)")
            pulados += 1
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Verificar se já tem o script
            if AUTH_SCRIPT in conteudo:
                print(f"✅ {filename} (já tem auth-check.js)")
                modificados += 1
                continue
            
            # Verificar se encontra a linha do bootstrap
            if SEARCH_STR not in conteudo:
                print(f"⚠️  {filename} (não encontrou bootstrap script)")
                erros += 1
                continue
            
            # Adicionar auth-check.js
            novo_conteudo = conteudo.replace(
                SEARCH_STR,
                f"{SEARCH_STR}\n    {AUTH_SCRIPT}"
            )
            
            # Salvar
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print(f"✅ {filename} (auth-check.js adicionado)")
            modificados += 1
            
        except Exception as e:
            print(f"❌ {filename} (erro: {str(e)})")
            erros += 1
    
    print(f"\n" + "="*60)
    print(f"RESULTADO:")
    print(f"  ✅ Modificados: {modificados}")
    print(f"  ⏭️  Pulados (públicos): {pulados}")
    print(f"  ❌ Erros: {erros}")
    print(f"="*60)
    
    return erros == 0

if __name__ == "__main__":
    print("\n🔒 Adicionando auth-check.js a todas as páginas...\n")
    
    if adicionar_auth_check():
        print("\n✅ SUCESSO! auth-check.js foi adicionado.\n")
    else:
        print("\n⚠️  Houve alguns problemas. Verifique acima.\n")
