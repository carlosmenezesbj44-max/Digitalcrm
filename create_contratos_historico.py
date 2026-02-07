#!/usr/bin/env python3
"""
Script para criar a tabela contratos_historico
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crm_core.db.base import engine
from crm_core.db.models_base import Base
from crm_modules.contratos.models import ContratoHistoricoModel

def create_historico_table():
    """Cria a tabela contratos_historico"""
    try:
        print("Criando tabela contratos_historico...")

        # Criar tabela contratos_historico
        ContratoHistoricoModel.__table__.create(engine, checkfirst=True)

        print("Tabela contratos_historico criada com sucesso!")

    except Exception as e:
        print(f"Erro ao criar tabela: {e}")
        return False

    return True

if __name__ == "__main__":
    create_historico_table()
