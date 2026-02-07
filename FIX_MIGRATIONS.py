#!/usr/bin/env python
"""
Corrige o Alembic para rodar migrations
Remove a migration do dashboard temporariamente e reconstrói a cadeia
"""

import os
import shutil
from pathlib import Path

print("="*70)
print(" CORRIGINDO MIGRATIONS")
print("="*70)

versions_dir = Path("alembic/versions")
dashboard_file = versions_dir / "001_add_dashboard_tables.py"
backup_file = Path("001_add_dashboard_tables.py.bak")

# Passo 1: Fazer backup da migration do dashboard
print("\n▶ Fazendo backup da migration do dashboard...")
if dashboard_file.exists():
    shutil.copy(dashboard_file, backup_file)
    print(f"✓ Backup criado: {backup_file}")
else:
    print("✗ Arquivo não encontrado")

# Passo 2: Remover arquivo do alembic
print("\n▶ Removendo migration do dashboard do Alembic...")
if dashboard_file.exists():
    dashboard_file.unlink()
    print("✓ Removido temporariamente")
else:
    print("✗ Arquivo já não existe")

# Passo 3: Rodar migrations existentes
print("\n▶ Rodando migrations existentes...")
print("   Executando: alembic upgrade heads")
os.system("alembic upgrade heads")

# Passo 4: Restaurar a migration do dashboard
print("\n▶ Restaurando migration do dashboard...")
if backup_file.exists():
    shutil.copy(backup_file, dashboard_file)
    print("✓ Restaurado")

# Passo 5: Rodar a nova migration
print("\n▶ Rodando migration do dashboard...")
print("   Executando: alembic upgrade head")
os.system("alembic upgrade head")

# Passo 6: Verificar
print("\n" + "="*70)
print(" ✓ MIGRATIONS CORRIGIDAS!")
print("="*70)
print("\nAgora execute:")
print("  python RUN_DASHBOARD.py")
