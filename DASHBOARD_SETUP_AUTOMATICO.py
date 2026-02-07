#!/usr/bin/env python
"""
Script de Setup Automático do Dashboard
Executa todos os passos necessários para integração completa
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Executa comando e mostra status"""
    print(f"\n{'='*70}")
    print(f"▶ {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ SUCESSO: {description}")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"✗ ERRO: {description}")
            print(result.stderr or result.stdout)
            return False
    except Exception as e:
        print(f"✗ ERRO: {e}")
        return False

def edit_main_py():
    """Edita main.py para adicionar rotas do dashboard"""
    print(f"\n{'='*70}")
    print("▶ Editando interfaces/api/main.py")
    print(f"{'='*70}")
    
    main_file = Path("interfaces/api/main.py")
    
    if not main_file.exists():
        print("✗ Arquivo main.py não encontrado")
        return False
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já foi editado
    if "routes_dashboard" in content:
        print("✓ main.py já foi editado")
        return True
    
    # Adicionar import
    import_line = "from interfaces.api.routes_dashboard import router as dashboard_router\n"
    
    # Adicionar include_router depois de criar o app
    router_line = "app.include_router(dashboard_router)\n"
    
    # Encontrar onde adicionar
    if "from fastapi import FastAPI" in content:
        # Adicionar import após os outros imports
        content = content.replace(
            "from fastapi import FastAPI",
            "from fastapi import FastAPI\nfrom interfaces.api.routes_dashboard import router as dashboard_router"
        )
    
    if "app = FastAPI" in content:
        # Adicionar router depois de criar o app
        content = content.replace(
            'app = FastAPI(title="CRM Provedor", version="1.0.0")',
            'app = FastAPI(title="CRM Provedor", version="1.0.0")\n\n# Include dashboard routes\napp.include_router(dashboard_router)'
        )
    
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ main.py editado com sucesso")
    return True

def main():
    """Função principal"""
    print("\n" + "="*70)
    print(" SETUP AUTOMÁTICO - DASHBOARD EXECUTIVO")
    print("="*70)
    
    root_dir = Path.cwd()
    print(f"\nDiretório do projeto: {root_dir}")
    
    # Passo 1: Migrations
    if not run_command("alembic upgrade head", "Rodando migrations do banco de dados"):
        print("\n⚠️  AVISO: Migrations falharam. Tente rodar manualmente:")
        print("   alembic upgrade head")
        return False
    
    # Passo 2: Editar main.py
    if not edit_main_py():
        print("\n⚠️  AVISO: Falha ao editar main.py")
        print("   Edite manualmente e adicione:")
        print("   from interfaces.api.routes_dashboard import router as dashboard_router")
        print("   app.include_router(dashboard_router)")
        return False
    
    # Passo 3: Inicializar Dashboard
    print(f"\n{'='*70}")
    print("▶ Inicializando Dashboard Padrão")
    print(f"{'='*70}")
    
    init_code = '''
import sys
sys.path.insert(0, ".")
from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

try:
    db = SessionLocal()
    service = DashboardService(db)
    service.initialize_default_dashboard()
    print("✓ Dashboard inicializado com sucesso!")
    db.close()
except Exception as e:
    print(f"✗ Erro ao inicializar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    if not run_command(f'python -c "{init_code}"', "Inicializando dashboard padrão"):
        print("\n⚠️  AVISO: Não conseguiu inicializar via script")
        print("   Você pode inicializar depois via API:")
        print("   curl -X POST http://localhost:8000/api/v1/dashboard/initialize")
    
    # Resumo Final
    print(f"\n{'='*70}")
    print("✓ SETUP COMPLETO!")
    print(f"{'='*70}")
    
    print("\n📝 PRÓXIMOS PASSOS:")
    print("\n1. Inicie o servidor:")
    print("   python -m uvicorn interfaces.api.main:app --reload")
    print("\n2. Teste os endpoints:")
    print("   curl http://localhost:8000/api/v1/dashboard/executive-summary")
    print("   curl http://localhost:8000/api/v1/dashboard/charts/revenue")
    print("\n3. Acesse a documentação Swagger:")
    print("   http://localhost:8000/docs")
    print("\n4. Leia a documentação:")
    print("   DASHBOARD_INICIO_RAPIDO.md")
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
