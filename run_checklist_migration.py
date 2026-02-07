#!/usr/bin/env python3
"""
Script para executar migração de checklist manualmente
"""

import sys
sys.path.append('.')

from sqlalchemy import create_engine, text


def run_migration():
    # Ler settings para obter database_url
    from crm_core.config.settings import settings
    engine = create_engine(settings.database_url)
    conn = engine.connect()

    try:
        # Criar tabela checklist_items
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS checklist_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_servico VARCHAR NOT NULL,
                nome_tarefa VARCHAR NOT NULL,
                descricao TEXT,
                ordem INTEGER DEFAULT 0,
                ativo BOOLEAN DEFAULT 1,
                data_criacao DATETIME
            )
        """))

        # Criar índice
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_checklist_items_id ON checklist_items (id)"))

        # Criar tabela checklist_progress
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS checklist_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ordem_servico_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                completado BOOLEAN DEFAULT 0,
                data_completado DATETIME,
                completado_por VARCHAR,
                observacoes TEXT,
                criado_automaticamente BOOLEAN DEFAULT 1
            )
        """))

        # Criar índice
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_checklist_progress_id ON checklist_progress (id)"))

        conn.commit()
        print("[OK] Tabelas criadas com sucesso!")
        print("     - checklist_items")
        print("     - checklist_progress")

        # Popular checklist_items com templates
        # Verificar se ja existem registros
        result = conn.execute(text("SELECT COUNT(*) FROM checklist_items"))
        count = result.fetchone()[0]

        if count == 0:
            # Instalacao
            conn.execute(text("""
                INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
                ('instalacao', 'Verificar sinal', 'Testar nivel de sinal no ponto de instalacao', 1),
                ('instalacao', 'Configurar PPPoE', 'Criar e configurar conexao PPPoE no cliente', 2),
                ('instalacao', 'Testar velocidade', 'Realizar teste de velocidade e estabilidade', 3),
                ('instalacao', 'Orientar cliente', 'Explicar uso do servico e Wi-Fi ao cliente', 4),
                ('instalacao', 'Finalizar', 'Finalizar instalacao e coletar assinatura do cliente', 5)
            """))

            # Suporte
            conn.execute(text("""
                INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
                ('suporte', 'Diagnosticar problema', 'Identificar causa raiz do problema reportado', 1),
                ('suporte', 'Verificar cabo', 'Inspecionar e substituir cabos danificados', 2),
                ('suporte', 'Reiniciar equipamento', 'Reiniciar roteador/ONU conforme procedimento', 3),
                ('suporte', 'Testar conectividade', 'Verificar conexao apos intervencoes', 4),
                ('suporte', 'Solucionar', 'Aplicar solucao definitiva ou escalar', 5)
            """))

            # Manutencao
            conn.execute(text("""
                INSERT INTO checklist_items (tipo_servico, nome_tarefa, descricao, ordem) VALUES
                ('manutencao', 'Inspecionar equipamentos', 'Verificar estado fisico de equipamentos', 1),
                ('manutencao', 'Limpar conexoes', 'Limpar conectores e terminais', 2),
                ('manutencao', 'Verificar redundancia', 'Testar caminhos redundantes de rede', 3),
                ('manutencao', 'Documentar acoes', 'Registrar todas as manutencoes realizadas', 4),
                ('manutencao', 'Finalizar', 'Confirmar funcionamento e encerrar OS', 5)
            """))

            conn.commit()
            print("[OK] Templates de checklist populados!")
            print("     - Instalacao (5 tarefas)")
            print("     - Suporte (5 tarefas)")
            print("     - Manutencao (5 tarefas)")
        else:
            print("[INFO] Checklist items ja existem, pulando populacao")

        conn.close()
        return True

    except Exception as e:
        print(f"[ERRO] Erro na migracao: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
