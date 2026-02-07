#!/usr/bin/env python
"""
Script para criar e rodar o Dashboard Executivo completamente
Executa: migrations → inicialização → servidor
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(text):
    """Print com formatação"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def run_command(cmd, description):
    """Executa comando e mostra resultado"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✓ {description} - SUCESSO")
            if result.stdout and len(result.stdout) < 500:
                print(result.stdout)
            return True
        else:
            print(f"✗ {description} - ERRO")
            print(result.stderr[:500] if result.stderr else result.stdout[:500])
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ {description} - ERRO: {e}")
        return False

def main():
    """Função principal"""
    os.chdir(Path(__file__).parent)
    
    print_header("DASHBOARD EXECUTIVO - SETUP COMPLETO")
    
    # ============= PASSO 1: MIGRATIONS =============
    print_header("PASSO 1: RODANDO MIGRATIONS DO BANCO DE DADOS")
    
    if not run_command("alembic upgrade heads", "Migrations"):
        print("\n✗ Erro ao rodar migrations")
        print("Tente rodar manualmente: alembic upgrade head")
        sys.exit(1)
    
    # ============= PASSO 2: INICIALIZAR DASHBOARD =============
    print_header("PASSO 2: INICIALIZANDO DASHBOARD PADRÃO")
    
    init_script = '''
import sys
sys.path.insert(0, ".")

try:
    print("  Importando módulos...")
    from crm_core.db.base import SessionLocal
    from crm_modules.dashboard.service import DashboardService
    
    print("  Conectando ao banco de dados...")
    db = SessionLocal()
    
    print("  Criando serviço...")
    service = DashboardService(db)
    
    print("  Inicializando dashboard padrão...")
    service.initialize_default_dashboard()
    
    print("  Registrando métricas iniciais...")
    service.record_daily_metrics()
    
    db.close()
    print("  ✓ Dashboard inicializado com sucesso!")
    
except Exception as e:
    print(f"  ✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    if not run_command(f'python -c "{init_script}"', "Inicialização do Dashboard"):
        print("\n✗ Erro ao inicializar dashboard")
        sys.exit(1)
    
    # ============= PASSO 3: EDITAR main.py =============
    print_header("PASSO 3: VERIFICANDO interfaces/api/main.py")
    
    main_file = Path("interfaces/api/main.py")
    
    if main_file.exists():
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "routes_dashboard" not in content:
            print("\n▶ Adicionando rotas do dashboard ao main.py...")
            
            new_content = '''from fastapi import FastAPI
import logging
from interfaces.api.routes_dashboard import router as dashboard_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="CRM Provedor", version="1.0.0")

# Include dashboard routes
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    print("Handling root request")
    return "CRM Provedor API" 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
            
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✓ main.py atualizado com sucesso")
        else:
            print("✓ main.py já possui as rotas do dashboard")
    else:
        print("✗ Arquivo main.py não encontrado")
        sys.exit(1)
    
    # ============= PASSO 4: INICIAR SERVIDOR =============
    print_header("PASSO 4: INICIANDO SERVIDOR FASTAPI")
    
    print("\n⚠️  O servidor será iniciado agora em http://localhost:8000")
    print("\n📊 Endpoints disponíveis:")
    print("  • GET  http://localhost:8000/api/v1/dashboard/executive-summary")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/revenue")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/clients")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/orders-status")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/top-clients")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/support-tickets")
    print("  • GET  http://localhost:8000/api/v1/dashboard/charts/contracts-status")
    
    print("\n📖 Documentação interativa:")
    print("  • http://localhost:8000/docs (Swagger)")
    print("  • http://localhost:8000/redoc (ReDoc)")
    
    print("\n📝 Documentação:")
    print("  • DASHBOARD_INICIO_RAPIDO.md")
    print("  • DASHBOARD_IMPLEMENTACAO.md")
    
    print("\n⌨️  Pressione CTRL+C para parar o servidor")
    print("\n" + "="*70)
    
    time.sleep(2)
    
    # Iniciar servidor
    try:
        os.system("python -m uvicorn interfaces.api.main:app --reload --host 0.0.0.0 --port 8000")
    except KeyboardInterrupt:
        print("\n\n✓ Servidor parado")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelado")
        sys.exit(1)
