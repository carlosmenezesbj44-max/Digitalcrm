#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script simples para iniciar o Dashboard
"""

import sys
import os
from pathlib import Path

# Fix encoding
if os.name == 'nt':
    os.system('chcp 65001 > nul')

sys.path.insert(0, str(Path.cwd()))

print("\n" + "="*70)
print(" DASHBOARD EXECUTIVO - INICIALIZANDO")
print("="*70)

# Passo 1: Criar tabelas
print("\nPASSO 1: Criando tabelas...")

try:
    from crm_core.db.base import engine, Base
    from crm_modules.dashboard.models import (
        Dashboard, DashboardKPI, DashboardWidget, MetricHistory
    )
    
    # Create all tables
    Base.metadata.create_all(engine)
    print("  OK - Tabelas criadas")
    
except ImportError as e:
    print(f"  ERRO - Import: {e}")
    print("  Pulando criacao de tabelas...")
except Exception as e:
    print(f"  ERRO: {e}")

# Passo 2: Editar main.py
print("\nPASSO 2: Atualizando main.py...")

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
        
        print("  OK - main.py atualizado")
    else:
        print("  OK - main.py ja tem rotas")
    
except Exception as e:
    print(f"  ERRO: {e}")

# Passo 3: Iniciar servidor
print("\n" + "="*70)
print(" INICIANDO SERVIDOR")
print("="*70)

print("\nEndpoints disponveis:")
print("  http://localhost:8000/api/v1/dashboard/executive-summary")
print("  http://localhost:8000/api/v1/dashboard/charts/revenue")
print("  http://localhost:8000/docs")

print("\nPressione CTRL+C para parar\n")

import time
time.sleep(1)

os.system("python -m uvicorn interfaces.api.main:app --reload --host 0.0.0.0 --port 8000")
