#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar menu-handler.js a todos os templates HTML
"""
import os
import re
import sys
from pathlib import Path

# Fix encoding on Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TEMPLATES_DIR = Path(__file__).parent / "interfaces" / "web" / "templates"
MENU_HANDLER_SCRIPT = '<script src="/static/js/menu-handler.js"></script>'

def atualizar_template(filepath):
    """Adiciona menu-handler.js ao template se não estiver lá"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem o script
        if '/static/js/menu-handler.js' in content:
            print(f"[JA] {filepath.name} - já possui menu-handler.js")
            return False
        
        # Verificar se é login ou registrar (não precisa de menu handler)
        if 'login.html' in filepath.name or 'registrar.html' in filepath.name:
            print(f"[IGN] {filepath.name} - ignorado (página de autenticação)")
            return False
        
        # Procurar pela tag </body> e adicionar o script antes
        if '</body>' not in content:
            print(f"[ERR] {filepath.name} - tag </body> não encontrada")
            return False
        
        # Adicionar o script antes de </body>
        new_content = content.replace(
            '</body>',
            f'    <script src="/static/js/menu-handler.js"></script>\n</body>'
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"[OK] {filepath.name} - atualizado com sucesso")
        return True
        
    except Exception as e:
        print(f"[ERRO] {filepath.name} - erro: {e}")
        return False

def main():
    print("Atualizando templates com menu-handler.js...\n")
    
    if not TEMPLATES_DIR.exists():
        print(f"Diretório {TEMPLATES_DIR} não encontrado!")
        return
    
    html_files = list(TEMPLATES_DIR.glob("*.html"))
    print(f"Encontrados {len(html_files)} arquivos HTML\n")
    
    updated = 0
    for filepath in sorted(html_files):
        if atualizar_template(filepath):
            updated += 1
    
    print(f"\n[TOTAL] {updated} arquivo(s) atualizado(s)")

if __name__ == "__main__":
    main()
