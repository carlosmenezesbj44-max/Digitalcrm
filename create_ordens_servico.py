#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from crm_core.db.base import get_db_session
from sqlalchemy import text, MetaData, Table, Column, Integer, String, DateTime, Boolean, Float, Text, Date, ForeignKey
from datetime import datetime

def create_ordens_servico_table():
    try:
        session = get_db_session()

        # Verificar se a tabela ordens_servico já existe
        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='ordens_servico'")).fetchone()
        if result:
            print("Tabela ordens_servico já existe!")
            return

        # Criar tabela ordens_servico
        metadata = MetaData()
        ordens_servico_table = Table('ordens_servico', metadata,
            Column('id', Integer, primary_key=True, index=True),
            Column('cliente_id', Integer, nullable=False),
            Column('titulo', String(255), nullable=False),
            Column('descricao', Text, nullable=True),
            Column('tipo_servico', String(50), nullable=False),  # 'instalacao', 'manutencao', 'reparo', 'upgrade'
            Column('prioridade', String(20), nullable=False, default='normal'),  # 'baixa', 'normal', 'alta', 'urgente'
            Column('status', String(20), nullable=False, default='aberta'),  # 'aberta', 'em_andamento', 'concluida', 'cancelada'
            Column('data_criacao', DateTime, default=datetime.utcnow),
            Column('data_agendamento', DateTime, nullable=True),
            Column('data_inicio', DateTime, nullable=True),
            Column('data_conclusao', DateTime, nullable=True),
            Column('tecnico_responsavel', String(255), nullable=True),
            Column('valor_servico', Float, nullable=True),
            Column('custo_empresa', Float, nullable=True),
            Column('observacoes', Text, nullable=True),
            Column('endereco_atendimento', String(500), nullable=True),
            Column('contato_cliente', String(255), nullable=True),
            Column('ativo', Boolean, default=True),
        )

        metadata.create_all(session.bind)
        session.commit()
        print("Tabela ordens_servico criada com sucesso!")

    except Exception as e:
        print(f"Erro ao criar tabela ordens_servico: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_ordens_servico_table()