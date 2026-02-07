#!/usr/bin/env python3
"""
Script para migração de contratos - adiciona novos campos e tabela de histórico
Execute este script para atualizar as tabelas de contratos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crm_core.db.base import engine
from crm_modules.contratos.models import ContratoModel, ContratoHistoricoModel
from sqlalchemy import text

def migrate():
    """Executa as migrações necessárias"""
    print("=" * 60)
    print("MIGRAÇÃO DE CONTRATOS - Versão 2")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Verificar se a tabela contratos existe
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='contratos'"))
            
            if not result.fetchone():
                print("✗ Tabela 'contratos' não existe. Criando...")
                ContratoModel.__table__.create(engine, checkfirst=True)
                print("✓ Tabela 'contratos' criada")
            else:
                print("✓ Tabela 'contratos' já existe. Verificando campos...")
                
                # Verificar cada novo campo
                resultado = conn.execute(text("PRAGMA table_info(contratos)"))
                colunas_existentes = {row[1] for row in resultado.fetchall()}
                
                novos_campos = {
                    'tipo_contrato': 'VARCHAR',
                    'data_vigencia_inicio': 'DATETIME',
                    'data_vigencia_fim': 'DATETIME',
                    'data_notificacao_renovacao': 'DATETIME',
                    'valor_contrato': 'FLOAT',
                    'moeda': 'VARCHAR',
                    'assinado_por': 'VARCHAR',
                    'status_renovacao': 'VARCHAR',
                    'proximo_contrato_id': 'INTEGER',
                    'criado_por': 'VARCHAR',
                    'criado_em': 'DATETIME',
                    'atualizado_por': 'VARCHAR',
                    'atualizado_em': 'DATETIME',
                    'deletado_em': 'DATETIME'
                }
                
                for campo, tipo in novos_campos.items():
                    if campo not in colunas_existentes:
                        print(f"  - Adicionando campo '{campo}' ({tipo})...")
                        try:
                            # Define valores padrão apropriados
                            default_value = ""
                            if tipo == "DATETIME":
                                default_value = "CURRENT_TIMESTAMP"
                            elif tipo == "FLOAT":
                                default_value = "0"
                            elif tipo == "INTEGER":
                                default_value = "NULL"
                            elif tipo == "VARCHAR":
                                if campo == "moeda":
                                    default_value = "'BRL'"
                                else:
                                    default_value = "NULL"
                            
                            sql = f"ALTER TABLE contratos ADD COLUMN {campo} {tipo} DEFAULT {default_value}"
                            conn.execute(text(sql))
                            print(f"    ✓ Campo '{campo}' adicionado")
                        except Exception as e:
                            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                                print(f"    ✓ Campo '{campo}' já existe")
                            else:
                                print(f"    ! Erro ao adicionar '{campo}': {e}")
                    else:
                        print(f"  ✓ Campo '{campo}' já existe")
            
            # Criar tabela de histórico
            historico_result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='contratos_historico'"))
            
            if not historico_result.fetchone():
                print("\n✗ Tabela 'contratos_historico' não existe. Criando...")
                ContratoHistoricoModel.__table__.create(engine, checkfirst=True)
                print("✓ Tabela 'contratos_historico' criada com sucesso!")
            else:
                print("\n✓ Tabela 'contratos_historico' já existe")
            
            conn.commit()
            
    except Exception as e:
        print(f"\n✗ Erro durante a migração: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\nProximas etapas:")
    print("1. Instalar reportlab: pip install reportlab")
    print("2. Testar criação de contratos com geração de PDF")
    print("3. Verificar histórico e auditoria nos novos campos")
    
    return True

if __name__ == "__main__":
    success = migrate()
    sys.exit(0 if success else 1)
