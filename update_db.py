#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from crm_core.db.base import get_db_session
from crm_modules.clientes.models import ClienteModel
from crm_modules.bloqueios.models import PlanoBloqueioModel

def update_database():
    try:
        session = get_db_session()

        # Adicionar coluna status_cliente à tabela clientes se não existir
        from sqlalchemy import text

        # Verificar se as colunas existem
        result = session.execute(text("PRAGMA table_info(clientes)")).fetchall()
        column_names = [row[1] for row in result]

        columns_to_add = {
            'whatsapp': "ALTER TABLE clientes ADD COLUMN whatsapp VARCHAR(255)",
            'telefone_residencial': "ALTER TABLE clientes ADD COLUMN telefone_residencial VARCHAR(255)",
            'telefone_comercial': "ALTER TABLE clientes ADD COLUMN telefone_comercial VARCHAR(255)",
            'telefone_celular': "ALTER TABLE clientes ADD COLUMN telefone_celular VARCHAR(255)",
            'cidade': "ALTER TABLE clientes ADD COLUMN cidade VARCHAR(255)",
            'rua': "ALTER TABLE clientes ADD COLUMN rua VARCHAR(255)",
            'bairro': "ALTER TABLE clientes ADD COLUMN bairro VARCHAR(255)",
            'cep': "ALTER TABLE clientes ADD COLUMN cep VARCHAR(255)",
            'condominio': "ALTER TABLE clientes ADD COLUMN condominio VARCHAR(255)",
            'bloco': "ALTER TABLE clientes ADD COLUMN bloco VARCHAR(255)",
            'estado': "ALTER TABLE clientes ADD COLUMN estado VARCHAR(255)",
            'tipo_localidade': "ALTER TABLE clientes ADD COLUMN tipo_localidade VARCHAR(255)",
            'tipo_cliente': "ALTER TABLE clientes ADD COLUMN tipo_cliente VARCHAR(255) DEFAULT 'fisico'",
            'ativo': "ALTER TABLE clientes ADD COLUMN ativo BOOLEAN DEFAULT 1",
            'nacionalidade': "ALTER TABLE clientes ADD COLUMN nacionalidade VARCHAR(255)",
            'rg': "ALTER TABLE clientes ADD COLUMN rg VARCHAR(255)",
            'orgao_emissor': "ALTER TABLE clientes ADD COLUMN orgao_emissor VARCHAR(255)",
            'naturalidade': "ALTER TABLE clientes ADD COLUMN naturalidade VARCHAR(255)",
            'data_nascimento': "ALTER TABLE clientes ADD COLUMN data_nascimento DATE",
            'username': "ALTER TABLE clientes ADD COLUMN username VARCHAR(255)",
            'observacoes': "ALTER TABLE clientes ADD COLUMN observacoes TEXT",
            'instagram': "ALTER TABLE clientes ADD COLUMN instagram VARCHAR(255)",
            'numero': "ALTER TABLE clientes ADD COLUMN numero VARCHAR(255)",
            'apartamento': "ALTER TABLE clientes ADD COLUMN apartamento VARCHAR(255)",
            'complemento': "ALTER TABLE clientes ADD COLUMN complemento VARCHAR(255)",
            'moradia': "ALTER TABLE clientes ADD COLUMN moradia VARCHAR(255)",
            'latitude': "ALTER TABLE clientes ADD COLUMN latitude FLOAT",
            'longitude': "ALTER TABLE clientes ADD COLUMN longitude FLOAT",
            'plano_id': "ALTER TABLE clientes ADD COLUMN plano_id INTEGER",
            'velocidade': "ALTER TABLE clientes ADD COLUMN velocidade INTEGER",
            'data_instalacao': "ALTER TABLE clientes ADD COLUMN data_instalacao DATE",
            'status_servico': "ALTER TABLE clientes ADD COLUMN status_servico VARCHAR(255) DEFAULT 'ativo'",
            'valor_mensal': "ALTER TABLE clientes ADD COLUMN valor_mensal FLOAT",
            'dia_vencimento': "ALTER TABLE clientes ADD COLUMN dia_vencimento INTEGER",
            'servidor_id': "ALTER TABLE clientes ADD COLUMN servidor_id INTEGER",
            'profile': "ALTER TABLE clientes ADD COLUMN profile VARCHAR(255)",
            'tipo_servico': "ALTER TABLE clientes ADD COLUMN tipo_servico VARCHAR(255) DEFAULT 'pppoe'",
            'comentario_login': "ALTER TABLE clientes ADD COLUMN comentario_login TEXT",
            'servico_instalacao_equipamentos': "ALTER TABLE clientes ADD COLUMN servico_instalacao_equipamentos BOOLEAN DEFAULT 0",
            'servico_suporte_premium': "ALTER TABLE clientes ADD COLUMN servico_suporte_premium BOOLEAN DEFAULT 0",
            'servico_treinamentos': "ALTER TABLE clientes ADD COLUMN servico_treinamentos BOOLEAN DEFAULT 0",
            'servico_cortesia': "ALTER TABLE clientes ADD COLUMN servico_cortesia BOOLEAN DEFAULT 0",
            'servico_wifi_publico': "ALTER TABLE clientes ADD COLUMN servico_wifi_publico BOOLEAN DEFAULT 0",
            'servico_apps_parceiros': "ALTER TABLE clientes ADD COLUMN servico_apps_parceiros BOOLEAN DEFAULT 0",
            'servico_campanhas': "ALTER TABLE clientes ADD COLUMN servico_campanhas BOOLEAN DEFAULT 0",
            'servico_personalizados': "ALTER TABLE clientes ADD COLUMN servico_personalizados BOOLEAN DEFAULT 0",
            'servico_monitoramento': "ALTER TABLE clientes ADD COLUMN servico_monitoramento BOOLEAN DEFAULT 0",
            'servico_hospedagem': "ALTER TABLE clientes ADD COLUMN servico_hospedagem BOOLEAN DEFAULT 0",
            'servico_integracao': "ALTER TABLE clientes ADD COLUMN servico_integracao BOOLEAN DEFAULT 0",
            'servico_vas': "ALTER TABLE clientes ADD COLUMN servico_vas BOOLEAN DEFAULT 0",
            'servico_streaming': "ALTER TABLE clientes ADD COLUMN servico_streaming BOOLEAN DEFAULT 0",
            'servico_backup': "ALTER TABLE clientes ADD COLUMN servico_backup BOOLEAN DEFAULT 0",
            'servico_colaboracao': "ALTER TABLE clientes ADD COLUMN servico_colaboracao BOOLEAN DEFAULT 0",
            'historico_chamados': "ALTER TABLE clientes ADD COLUMN historico_chamados BOOLEAN DEFAULT 0",
            'historico_instalacoes': "ALTER TABLE clientes ADD COLUMN historico_instalacoes BOOLEAN DEFAULT 0",
            'historico_upgrades': "ALTER TABLE clientes ADD COLUMN historico_upgrades BOOLEAN DEFAULT 0",
            'status_cliente': "ALTER TABLE clientes ADD COLUMN status_cliente VARCHAR(255) DEFAULT 'conectado'",
            'plano_bloqueio_id': "ALTER TABLE clientes ADD COLUMN plano_bloqueio_id INTEGER"
        }

        for col_name, alter_sql in columns_to_add.items():
            if col_name not in column_names:
                session.execute(text(alter_sql))
                print(f"Added {col_name} column")

        # Criar tabela planos_bloqueio se não existir
        result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='planos_bloqueio'")).fetchone()
        if not result:
            from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean
            metadata = MetaData()
            planos_bloqueio_table = Table('planos_bloqueio', metadata,
                Column('id', Integer, primary_key=True, index=True),
                Column('nome', String, nullable=False),
                Column('ip_privado', String, nullable=False),
                Column('reduzir_velocidade', Boolean, default=False),
                Column('dias_bloqueio', Integer, nullable=False),
                Column('tipo_bloqueio', String, nullable=False, default="bloqueio_total"),
                Column('ativo', Boolean, default=True),
            )

            metadata.create_all(session.bind)
            print("Created planos_bloqueio table")

        session.commit()
        print("Database updated successfully!")
    except Exception as e:
        print(f"Error updating database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    update_database()