#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove verificação de autenticação do menu-handler.js
já que auth-check.js agora faz isso
"""

import os
import sys
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TEMPLATES_DIR = "interfaces/web/templates"

# Conteúdo ANTIGO que vamos procurar
ANTIGO = '''// Verificar se usuario esta autenticado ao carregar a pagina
window.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('access_token');
    const currentPath = window.location.pathname;
    
    // Remover hash da URL se existir (https://localhost/#  -> https://localhost/)
    if (window.location.hash) {
        window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
    }
    
    // Se nao tem token e nao esta na tela de login/registrar, redireciona
    if (!token && currentPath !== '/login' && currentPath !== '/registrar') {
        window.location.replace('/login');
    }
    
    // Se tem token e está em login ou registrar, redireciona para dashboard
    if (token && (currentPath === '/login' || currentPath === '/registrar')) {
        window.location.replace('/dashboard');
    }
    
    // Sincronizar estados de chevrons com menus
    syncMenuStates();
});'''

# Conteúdo NOVO
NOVO = '''// Sincronizar menus ao carregar a pagina
// NOTA: Verificação de autenticação agora feita por auth-check.js
window.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    
    // Remover hash da URL se existir (https://localhost/#  -> https://localhost/)
    if (window.location.hash) {
        window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
    }
    
    // Sincronizar estados de chevrons com menus
    syncMenuStates();
});'''

def corrigir_htmls():
    templates_path = Path(TEMPLATES_DIR)
    if not templates_path.exists():
        print(f"❌ Diretório {TEMPLATES_DIR} não encontrado!")
        return False
    
    html_files = sorted(templates_path.glob("*.html"))
    
    if not html_files:
        print(f"❌ Nenhum arquivo .html encontrado em {TEMPLATES_DIR}")
        return False
    
    print(f"\n🔧 Corrigindo {len(html_files)} arquivos HTML...\n")
    
    corrigidos = 0
    
    for html_file in html_files:
        filename = html_file.name
        
        if filename in ["login.html", "registrar.html"]:
            print(f"⏭️  {filename} (página pública - pulado)")
            continue
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # Se não tem o conteúdo antigo, pula
            if ANTIGO not in conteudo:
                print(f"⏭️  {filename} (não precisa de correção)")
                continue
            
            # Substituir
            novo_conteudo = conteudo.replace(ANTIGO, NOVO)
            
            # Salvar
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(novo_conteudo)
            
            print(f"✅ {filename}")
            corrigidos += 1
            
        except Exception as e:
            print(f"❌ {filename} (erro: {str(e)})")
    
    print(f"\n" + "="*60)
    print(f"✅ {corrigidos} arquivo(s) corrigido(s)")
    print(f"="*60)
    
    return True

if __name__ == "__main__":
    print("\n🔧 Removendo verificação duplicada de autenticação...\n")
    
    if corrigir_htmls():
        print("\n✅ SUCESSO! Menu-handler corrigido em todos os arquivos.\n")
    else:
        print("\n⚠️  Houve alguns problemas.\n")
