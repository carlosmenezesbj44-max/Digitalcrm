#!/usr/bin/env python3
"""
Script para testar os endpoints de checklist
"""

import sys
sys.path.append('.')

from sqlalchemy import create_engine, text
from crm_core.config.settings import settings


def test_endpoints():
    """Testa os endpoints de checklist"""
    engine = create_engine(settings.database_url)
    conn = engine.connect()

    try:
        print("=" * 50)
        print("TESTE DO SISTEMA DE CHECKLIST")
        print("=" * 50)

        # 1. Verificar itens do checklist
        print("\n1. Verificando checklist items...")
        result = conn.execute(text("SELECT * FROM checklist_items ORDER BY tipo_servico, ordem"))
        items = result.fetchall()

        print(f"   Total de itens: {len(items)}")
        for item in items:
            print(f"   - [{item[1]:12}] {item[2]}")

        # 2. Verificar OS existentes para testar
        print("\n2. Verificando ordens de servico...")
        result = conn.execute(text("SELECT id, tipo_servico, titulo FROM ordens_servico LIMIT 5"))
        ordens = result.fetchall()

        if ordens:
            print(f"   Ordens encontradas: {len(ordens)}")
            for os in ordens:
                print(f"   - OS #{os[0]}: {os[2]} ({os[1]})")
        else:
            print("   Nenhuma ordem de servico encontrada")

        # 3. Inicializar checklist para primeira OS
        if ordens:
            os_id = ordens[0][0]
            tipo = ordens[0][1]
            print(f"\n3. Inicializando checklist para OS #{os_id} ({tipo})...")

            # Verificar se ja existe progresso
            result = conn.execute(text(f"SELECT COUNT(*) FROM checklist_progress WHERE ordem_servico_id = {os_id}"))
            exists = result.fetchone()[0]

            if exists == 0:
                # Buscar item IDs para o tipo de servico
                result = conn.execute(text(f"SELECT id FROM checklist_items WHERE tipo_servico = '{tipo}' ORDER BY ordem"))
                item_ids = result.fetchall()

                for item_id in item_ids:
                    conn.execute(text(f"""
                        INSERT INTO checklist_progress (ordem_servico_id, item_id, completado)
                        VALUES ({os_id}, {item_id[0]}, 0)
                    """))
                conn.commit()
                print(f"   Checklist inicializado com {len(item_ids)} tarefas")
            else:
                print("   Checklist ja inicializado anteriormente")

            # 4. Verificar progresso
            print("\n4. Verificando progresso do checklist...")
            result = conn.execute(text(f"""
                SELECT ci.nome_tarefa, cp.completado, cp.completado_por
                FROM checklist_progress cp
                JOIN checklist_items ci ON cp.item_id = ci.id
                WHERE cp.ordem_servico_id = {os_id}
                ORDER BY ci.ordem
            """))
            progress = result.fetchall()

            completed = sum(1 for p in progress if p[1])
            total = len(progress)

            print(f"   Progresso: {completed} de {total} tarefas concluidas")
            for p in progress:
                status = "[X]" if p[1] else "[ ]"
                by = f" (por: {p[2]})" if p[2] else ""
                print(f"   {status} {p[0]}{by}")

            # 5. Simular toggle de item
            print("\n5. Simulando toggle de item...")
            if progress:
                first_incomplete = next((p for p in progress if not p[1]), None)
                if first_incomplete:
                    # Buscar item_id
                    result = conn.execute(text(f"""
                        SELECT cp.id, ci.id FROM checklist_progress cp
                        JOIN checklist_items ci ON cp.item_id = ci.id
                        WHERE cp.ordem_servico_id = {os_id} AND ci.nome_tarefa = '{first_incomplete[0]}'
                    """))
                    item = result.fetchone()
                    
                    if item:
                        conn.execute(text(f"""
                            UPDATE checklist_progress SET completado = 1, 
                            completado_por = 'Teste', 
                            data_completado = datetime('now')
                            WHERE id = {item[0]}
                        """))
                        conn.commit()
                        print(f"   Item '{first_incomplete[0]}' marcado como completado")

        print("\n" + "=" * 50)
        print("TESTE CONCLUIDO COM SUCESSO!")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)
