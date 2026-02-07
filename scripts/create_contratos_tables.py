#!/usr/bin/env python3
"""
Script para criar tabelas de contratos e adicionar campo status_contrato na tabela clientes
Execute este script para criar as tabelas necessárias.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crm_core.db.base import engine
from crm_core.db.models_base import Base
from crm_modules.contratos.models import ContratoModel
from crm_modules.clientes.models import ClienteModel
from sqlalchemy import text

def create_tables():
    """Cria as tabelas necessárias"""
    try:
        print("Criando tabelas de contratos...")

        # Criar tabela contratos
        ContratoModel.__table__.create(engine, checkfirst=True)

        print("Tabela contratos criada com sucesso!")

        # Verificar se coluna status_contrato existe na tabela clientes
        with engine.connect() as conn:
            # Verificar se coluna já existe
            result = conn.execute(text("""
                PRAGMA table_info(clientes)
            """))
            columns = [row[1] for row in result.fetchall()]

            if 'status_contrato' not in columns:
                print("Adicionando coluna status_contrato na tabela clientes...")
                conn.execute(text("""
                    ALTER TABLE clientes ADD COLUMN status_contrato VARCHAR DEFAULT 'nenhum'
                """))
                conn.commit()
                print("Coluna status_contrato adicionada!")
            else:
                print("Coluna status_contrato ja existe!")

        print("Todas as tabelas criadas com sucesso!")

    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        return False

    return True

if __name__ == "__main__":
    create_tables()