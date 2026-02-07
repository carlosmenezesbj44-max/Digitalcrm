#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cria o Dashboard Executivo completamente
Sem usar Alembic - cria as tabelas diretamente
"""

import sys
import os
from pathlib import Path

# Fix encoding for Windows
if os.name == 'nt':
    os.system('chcp 65001 > nul')

sys.path.insert(0, str(Path.cwd()))

print("\n" + "="*70)
print(" CRIANDO DASHBOARD EXECUTIVO")
print("="*70)

# ============= PASSO 1: CRIAR TABELAS =============
print("\nPASSO 1: Criando tabelas do banco de dados...")

try:
    from crm_core.db.base import engine
    from crm_modules.dashboard.models import (
        Dashboard, DashboardKPI, DashboardWidget, MetricHistory
    )
    
    print("  Importando modelos...")
    
    print("  Criando tabelas...")
    Dashboard.__table__.create(engine, checkfirst=True)
    print("    ✓ Tabela: dashboard")
    
    DashboardKPI.__table__.create(engine, checkfirst=True)
    print("    ✓ Tabela: dashboard_kpi")
    
    DashboardWidget.__table__.create(engine, checkfirst=True)
    print("    ✓ Tabela: dashboard_widget")
    
    MetricHistory.__table__.create(engine, checkfirst=True)
    print("    ✓ Tabela: metric_history")
    
    print("\n✓ Todas as tabelas criadas com sucesso!")
    
except Exception as e:
    print(f"\n✗ Erro ao criar tabelas: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============= PASSO 2: INICIALIZAR DASHBOARD =============
print("\nPASSO 2: Inicializando dashboard padrao...")

try:
    from crm_core.db.base import SessionLocal
    from crm_modules.dashboard.service import DashboardService
    
    db = SessionLocal()
    service = DashboardService(db)
    
    print("  Criando dashboard...")
    service.initialize_default_dashboard()
    print("    ✓ Dashboard padrão criado")
    
    print("  Registrando métricas iniciais...")
    service.record_daily_metrics()
    print("    ✓ Métricas registradas")
    
    db.close()
    print("\n✓ Dashboard inicializado com sucesso!")
    
except Exception as e:
    print(f"\n✗ Erro ao inicializar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============= PASSO 3: EDITAR MAIN.PY =============
print("\nPASSO 3: Atualizando main.py...")

try:
    main_file = Path("interfaces/api/main.py")
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "routes_dashboard" not in content:
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
        
        print("  ✓ main.py atualizado")
    else:
        print("  ✓ main.py já está atualizado")
    
except Exception as e:
    print(f"\n✗ Erro ao editar main.py: {e}")
    sys.exit(1)

# ============= PASSO 4: RESUMO =============
print("\n" + "="*70)
print(" DASHBOARD CRIADO COM SUCESSO!")
print("="*70)

print("\nENDPOINTS DISPONÍVEIS:")
print("\n  Executive Summary:")
print("    curl http://localhost:8000/api/v1/dashboard/executive-summary")

print("\n  Graficos:")
print("    curl http://localhost:8000/api/v1/dashboard/charts/revenue")
print("    curl http://localhost:8000/api/v1/dashboard/charts/clients")
print("    curl http://localhost:8000/api/v1/dashboard/charts/orders-status")
print("    curl http://localhost:8000/api/v1/dashboard/charts/top-clients")
print("    curl http://localhost:8000/api/v1/dashboard/charts/support-tickets")
print("    curl http://localhost:8000/api/v1/dashboard/charts/contracts-status")

print("\n  Gerenciamento:")
print("    curl http://localhost:8000/api/v1/dashboard")

print("\nDOCUMENTACAO INTERATIVA:")
print("    http://localhost:8000/docs")

print("\nINICIANDO SERVIDOR...")
print("\n" + "="*70)

import time
time.sleep(2)

import os
os.system("python -m uvicorn interfaces.api.main:app --reload --host 0.0.0.0 --port 8000")
