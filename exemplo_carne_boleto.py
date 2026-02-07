"""
Exemplo de uso: Como criar carnês e boletos no CRM com integração Gerencianet

Este script demonstra como usar os novos recursos de carnês e boletos
"""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

# ===== IMPORTS =====
from crm_modules.faturamento.carne_service import CarneService
from crm_modules.faturamento.boleto_service import BoletoService
from crm_modules.faturamento.carne_schemas import CarneCreate, BoletoCreate
from crm_modules.faturamento.gerencianet_client import GerencianetClient
from crm_core.db.database import SessionLocal


def exemplo_1_criar_carne_mensal():
    """
    Exemplo 1: Cliente quer pagar R$ 1.200 em 12 parcelas mensais
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: Criar Carnê de 12 parcelas")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        # Dados do carnê
        carne_data = CarneCreate(
            cliente_id=1,  # ID do cliente
            valor_total=1200.00,  # Total
            quantidade_parcelas=12,  # 12x
            data_inicio=date(2024, 1, 1),
            data_primeiro_vencimento=date(2024, 2, 1),
            intervalo_dias=30,  # Mensal
            descricao="Serviços de consultoria - Projeto A",
            gerar_boletos=True  # Gerar boletos automaticamente
        )
        
        # Criar carnê
        service = CarneService(session=db)
        carne = service.criar_carne(carne_data)
        
        print(f"\n✓ Carnê criado com sucesso!")
        print(f"  - Número: {carne.numero_carne}")
        print(f"  - Valor total: R$ {carne.valor_total:.2f}")
        print(f"  - Parcelas: {carne.quantidade_parcelas}x de R$ {carne.valor_parcela:.2f}")
        print(f"  - Status: {carne.status}")
        print(f"  - Primeiro vencimento: {carne.data_primeiro_vencimento}")
        
        # Listar parcelas
        print(f"\n  Parcelas geradas:")
        for parcela in carne.parcelas[:3]:  # Mostrar primeiras 3
            print(f"    {parcela['numero_parcela']}. R$ {parcela['valor']:.2f} - Vence em {parcela['data_vencimento']}")
            if parcela['codigo_barras']:
                print(f"       Código de barras: {parcela['codigo_barras'][:30]}...")
        print(f"    ... ({len(carne.parcelas)} parcelas no total)")
        
        return carne.id
    
    except Exception as e:
        print(f"\n✗ Erro ao criar carnê: {e}")
    
    finally:
        db.close()


def exemplo_2_criar_boleto_fatura():
    """
    Exemplo 2: Gerar boleto para uma fatura existente
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Gerar Boleto para Fatura")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        fatura_id = 1  # Supondo que existe fatura com ID 1
        
        service = BoletoService(session=db)
        
        boleto = service.gerar_boleto_fatura(
            fatura_id=fatura_id,
            juros_dia=0.05,  # 0.05% de juros ao dia
            multa_atraso=2.0  # 2% de multa por atraso
        )
        
        print(f"\n✓ Boleto gerado com sucesso!")
        print(f"  - Número: {boleto.numero_boleto}")
        print(f"  - Valor: R$ {boleto.valor:.2f}")
        print(f"  - Vencimento: {boleto.data_vencimento}")
        print(f"  - Status: {boleto.status}")
        print(f"  - Código de barras: {boleto.codigo_barras}")
        print(f"  - Link para download: {boleto.url_boleto}")
        
        return boleto.id
    
    except Exception as e:
        print(f"\n✗ Erro ao gerar boleto: {e}")
    
    finally:
        db.close()


def exemplo_3_criar_boleto_direto():
    """
    Exemplo 3: Criar um boleto direto (sem estar vinculado a fatura)
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Criar Boleto Direto (Pagamento adicional)")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = BoletoService(session=db)
        
        boleto = service.gerar_boleto_direto(
            cliente_id=1,
            valor=500.00,
            data_vencimento=date.today() + timedelta(days=30),
            descricao="Pagamento de taxa adicional",
            juros_dia=0.05,
            multa_atraso=2.0
        )
        
        print(f"\n✓ Boleto direto criado com sucesso!")
        print(f"  - Número: {boleto.numero_boleto}")
        print(f"  - Valor: R$ {boleto.valor:.2f}")
        print(f"  - Vencimento: {boleto.data_vencimento}")
        print(f"  - Código de barras: {boleto.codigo_barras}")
        print(f"  - Linha digitável: {boleto.linha_digitavel}")
        
        return boleto.id
    
    except Exception as e:
        print(f"\n✗ Erro ao criar boleto direto: {e}")
    
    finally:
        db.close()


def exemplo_4_registrar_pagamento():
    """
    Exemplo 4: Registrar pagamento de uma parcela
    """
    print("\n" + "="*60)
    print("EXEMPLO 4: Registrar Pagamento de Parcela")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = CarneService(session=db)
        
        # Registrar pagamento da parcela ID 1
        service.registrar_pagamento_parcela(
            parcela_id=1,
            valor_pago=100.00
        )
        
        print(f"\n✓ Pagamento registrado com sucesso!")
        print(f"  - Parcela: 1")
        print(f"  - Valor pago: R$ 100.00")
        print(f"  - Data do pagamento: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    except Exception as e:
        print(f"\n✗ Erro ao registrar pagamento: {e}")
    
    finally:
        db.close()


def exemplo_5_listar_parcelas_carne():
    """
    Exemplo 5: Listar parcelas de um carnê
    """
    print("\n" + "="*60)
    print("EXEMPLO 5: Listar Parcelas do Carnê")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = CarneService(session=db)
        
        parcelas = service.listar_parcelas_carne(carne_id=1)
        
        print(f"\n✓ Total de {len(parcelas)} parcelas encontradas:")
        print(f"\n{'#':<3} {'Valor':<12} {'Vencimento':<12} {'Status':<12} {'Pago':<10}")
        print("-" * 50)
        
        for p in parcelas:
            status_emoji = "✓" if p['status'] == 'pago' else "○"
            print(f"{p['numero']:<3} R${p['valor']:<10.2f} {str(p['data_vencimento']):<12} {p['status']:<12} R${p['valor_pago']:<9.2f}")
        
        # Resumo
        total_parcelas = len(parcelas)
        total_pago = sum(p['valor_pago'] for p in parcelas)
        total_valor = sum(p['valor'] for p in parcelas)
        pendentes = sum(1 for p in parcelas if p['status'] == 'pendente')
        
        print("-" * 50)
        print(f"{'Totais':<3} R${total_valor:<10.2f} {'':<12} Pago: R$ {total_pago:.2f}")
        print(f"Parcelas pendentes: {pendentes}/{total_parcelas}")
    
    except Exception as e:
        print(f"\n✗ Erro ao listar parcelas: {e}")
    
    finally:
        db.close()


def exemplo_6_listar_boletos():
    """
    Exemplo 6: Listar boletos de um cliente
    """
    print("\n" + "="*60)
    print("EXEMPLO 6: Listar Boletos de Cliente")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = BoletoService(session=db)
        
        # Listar boletos pendentes
        boletos = service.listar_boletos_cliente(cliente_id=1, status="pendente")
        
        print(f"\n✓ Total de {len(boletos)} boletos pendentes:")
        print(f"\n{'Boleto':<20} {'Valor':<12} {'Vencimento':<12} {'Status':<12}")
        print("-" * 56)
        
        for b in boletos:
            dias_vencimento = (b.data_vencimento - date.today()).days
            status_display = f"{b.status}"
            if dias_vencimento < 0:
                status_display += f" ({abs(dias_vencimento)}d atrasado)"
            
            print(f"{b.numero_boleto:<20} R${b.valor:<10.2f} {str(b.data_vencimento):<12} {status_display:<12}")
    
    except Exception as e:
        print(f"\n✗ Erro ao listar boletos: {e}")
    
    finally:
        db.close()


def exemplo_7_sincronizar_gerencianet():
    """
    Exemplo 7: Sincronizar boletos com Gerencianet
    """
    print("\n" + "="*60)
    print("EXEMPLO 7: Sincronizar Boletos com Gerencianet")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = BoletoService(session=db)
        
        # Sincronizar todos os boletos abertos
        boletos_atualizados = service.sincronizar_pagamentos_gerencianet()
        
        print(f"\n✓ Sincronização concluída!")
        print(f"  - Total sincronizado: {len(boletos_atualizados)} boletos")
        
        if boletos_atualizados:
            print(f"\n  Status dos boletos:")
            for b in boletos_atualizados:
                print(f"    - {b.numero_boleto}: {b.gerencianet_status}")
    
    except Exception as e:
        print(f"\n✗ Erro ao sincronizar: {e}")
    
    finally:
        db.close()


def exemplo_8_cancelar_carne():
    """
    Exemplo 8: Cancelar um carnê
    """
    print("\n" + "="*60)
    print("EXEMPLO 8: Cancelar Carnê")
    print("="*60)
    
    db = SessionLocal()
    
    try:
        service = CarneService(session=db)
        
        # Cancelar carnê
        carne = service.cancelar_carne(carne_id=1)
        
        print(f"\n✓ Carnê cancelado com sucesso!")
        print(f"  - Número: {carne.numero_carne}")
        print(f"  - Status: {carne.status}")
        print(f"  - Todas as parcelas pendentes foram canceladas no Gerencianet")
    
    except Exception as e:
        print(f"\n✗ Erro ao cancelar carnê: {e}")
    
    finally:
        db.close()


def menu_principal():
    """Menu interativo"""
    print("\n" + "="*60)
    print("EXEMPLOS DE USO: CARNÊS E BOLETOS")
    print("="*60)
    print("\n1. Criar carnê de 12 parcelas")
    print("2. Gerar boleto para uma fatura")
    print("3. Criar boleto direto (sem fatura)")
    print("4. Registrar pagamento de parcela")
    print("5. Listar parcelas de um carnê")
    print("6. Listar boletos de cliente")
    print("7. Sincronizar boletos com Gerencianet")
    print("8. Cancelar carnê")
    print("9. Executar todos os exemplos")
    print("0. Sair")
    
    escolha = input("\nEscolha uma opção: ")
    
    if escolha == "1":
        exemplo_1_criar_carne_mensal()
    elif escolha == "2":
        exemplo_2_criar_boleto_fatura()
    elif escolha == "3":
        exemplo_3_criar_boleto_direto()
    elif escolha == "4":
        exemplo_4_registrar_pagamento()
    elif escolha == "5":
        exemplo_5_listar_parcelas_carne()
    elif escolha == "6":
        exemplo_6_listar_boletos()
    elif escolha == "7":
        exemplo_7_sincronizar_gerencianet()
    elif escolha == "8":
        exemplo_8_cancelar_carne()
    elif escolha == "9":
        exemplo_1_criar_carne_mensal()
        exemplo_2_criar_boleto_fatura()
        exemplo_3_criar_boleto_direto()
        exemplo_4_registrar_pagamento()
        exemplo_5_listar_parcelas_carne()
        exemplo_6_listar_boletos()
    elif escolha == "0":
        print("\nAté logo!")
        return
    
    input("\nPressione ENTER para continuar...")
    menu_principal()


if __name__ == "__main__":
    menu_principal()
