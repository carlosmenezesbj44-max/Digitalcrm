#!/usr/bin/env python3
"""
Script para executar migração manualmente quando alembic não está disponível
"""

import sys
sys.path.append('.')

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey
from crm_core.config.settings import settings

def run_migration():
    engine = create_engine(settings.database_url)
    metadata = MetaData()

    # Criar tabela faturas
    faturas_table = Table('faturas', metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('cliente_id', Integer, ForeignKey('clientes.id'), nullable=False),
        Column('numero_fatura', String, unique=True, nullable=False),
        Column('data_emissao', DateTime, nullable=True),
        Column('data_vencimento', Date, nullable=False),
        Column('valor_total', Float, nullable=False),
        Column('status', String, default='pendente'),
        Column('valor_pago', Float, default=0.0),
        Column('descricao', String),
        Column('ativo', Boolean, default=True),
    )

    # Criar tabela pagamentos
    pagamentos_table = Table('pagamentos', metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('fatura_id', Integer, ForeignKey('faturas.id'), nullable=False),
        Column('valor_pago', Float, nullable=False),
        Column('data_pagamento', DateTime, nullable=True),
        Column('metodo_pagamento', String, nullable=False),
        Column('referencia', String),
        Column('observacoes', String),
        Column('ativo', Boolean, default=True),
    )

    try:
        metadata.create_all(engine)
        print("✅ Migração executada com sucesso!")
        print("Tabelas criadas: faturas, pagamentos")
    except Exception as e:
        print(f"❌ Erro na migração: {e}")

if __name__ == "__main__":
    run_migration()