#!/usr/bin/env python3
"""
Remove funções toggleSubmenu duplicadas dos templates HTML.
Mantém apenas a importação do menu-handler.js
"""

import re
from pathlib import Path

# Padrão para encontrar e remover a função duplicada
pattern = r'    <script>\s*function toggleSubmenu\(button\) \{[^}]*\}\s*</script>\s*'

templates_dir = Path('interfaces/web/templates')
modified_files = []

for html_file in templates_dir.glob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'function toggleSubmenu' in content:
        new_content = re.sub(pattern, '', content)
        
        # Verificar se realmente removeu algo
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            modified_files.append(html_file.name)
            print(f"✓ {html_file.name} - removido script duplicado")
        else:
            print(f"✗ {html_file.name} - padrão não encontrado")

print(f"\nTotal de arquivos modificados: {len(modified_files)}")
