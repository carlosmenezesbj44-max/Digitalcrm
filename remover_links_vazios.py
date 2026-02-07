#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove links vazios (#fornecedor, #contratos) dos templates
"""
import sys
from pathlib import Path

if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TEMPLATES_DIR = Path(__file__).parent / "interfaces" / "web" / "templates"

def remover_links_vazios(filepath):
    """Remove links vazios (#fornecedor, #contratos) do template"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remover links para #fornecedor
        content = content.replace(
            '<a href="#fornecedor"><i class="bi bi-shop"></i> Fornecedor</a>\n',
            ''
        )
        content = content.replace(
            '<a href="#fornecedor"><i class="bi bi-shop"></i> Fornecedor</a>',
            ''
        )
        
        # Remover links para #contratos
        content = content.replace(
            '<a href="#contratos"><i class="bi bi-file-text"></i> Contratos</a>\n',
            ''
        )
        content = content.replace(
            '<a href="#contratos"><i class="bi bi-file-text"></i> Contratos</a>',
            ''
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] {filepath.name} - links vazios removidos")
            return True
        else:
            print(f"[---] {filepath.name} - nenhum link vazio encontrado")
            return False
        
    except Exception as e:
        print(f"[ERR] {filepath.name} - erro: {e}")
        return False

def main():
    print("Removendo links vazios dos templates...\n")
    
    if not TEMPLATES_DIR.exists():
        print(f"Diretorio {TEMPLATES_DIR} nao encontrado!")
        return
    
    html_files = list(TEMPLATES_DIR.glob("*.html"))
    print(f"Encontrados {len(html_files)} arquivos HTML\n")
    
    updated = 0
    for filepath in sorted(html_files):
        if remover_links_vazios(filepath):
            updated += 1
    
    print(f"\n[TOTAL] {updated} arquivo(s) atualizado(s)")

if __name__ == "__main__":
    main()
