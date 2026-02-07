"""Script para verificar tabelas no banco de dados"""
from crm_core.db.base import engine
from sqlalchemy import inspect

inspector = inspect(engine)

print("\n=== TABELAS NO BANCO DE DADOS ===")
tables = inspector.get_table_names()
for table in tables:
    print(f"  ✓ {table}")

print(f"\nTotal: {len(tables)} tabelas")

# Verificar se a tabela contratos existe
if 'contratos' in tables:
    print("\n=== COLUNAS DA TABELA CONTRATOS ===")
    columns = inspector.get_columns('contratos')
    for col in columns:
        print(f"  - {col['name']} ({col['type']})")
else:
    print("\n❌ TABELA 'contratos' NÃO ENCONTRADA!")

# Verificar se a tabela clientes tem relacionamento
if 'clientes' in tables:
    print("\n=== COLUNAS DA TABELA CLIENTES ===")
    columns = inspector.get_columns('clientes')
    for col in columns:
        if 'contrato' in col['name'].lower():
            print(f"  - {col['name']} ({col['type']})")
