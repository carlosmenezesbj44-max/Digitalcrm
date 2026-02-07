#!/usr/bin/env python3
"""
Exemplos práticos de uso do módulo de Contratos v2

Demonstra como:
- Criar contratos com PDF
- Assinar digitalmente
- Liberar contratos
- Obter histórico
- Monitorar vencimentos
- Renovar contratos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime, timedelta
from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import ContratoCreate, TipoContrato, StatusRenovacao
from crm_core.db.base import get_db_session

def exemplo_1_criar_contrato():
    """Exemplo 1: Criar contrato com geração automática de PDF"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Criar Contrato com PDF")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db, usuario_id="admin_001")
    
    # Preparar dados
    contrato_data = ContratoCreate(
        cliente_id=1,  # Assumindo que cliente com ID 1 existe
        titulo="Contrato de Prestação de Serviços - Internet Banda Larga",
        descricao="Contrato para prestação de serviço de internet com velocidade de 100 Mbps, suporte técnico 24/7 e SLA de 99.9%",
        tipo_contrato=TipoContrato.SERVICO,
        data_vigencia_inicio=datetime.now(),
        data_vigencia_fim=datetime.now() + timedelta(days=365),
        valor_contrato=99.90,
        moeda="BRL",
        status_renovacao=StatusRenovacao.RENOVACAO_MANUAL,
        incluir_pdf=True  # Gera PDF automaticamente
    )
    
    try:
        contrato = service.criar_contrato(contrato_data, usuario_id="admin_001")
        
        print(f"\n✓ Contrato criado com sucesso!")
        print(f"  ID: {contrato.id}")
        print(f"  Título: {contrato.titulo}")
        print(f"  Status: {contrato.status_assinatura.value}")
        print(f"  Valor: R$ {contrato_data.valor_contrato:.2f}")
        print(f"  Arquivo PDF: {contrato.arquivo_contrato}")
        
        return contrato.id
    except Exception as e:
        print(f"\n✗ Erro ao criar contrato: {e}")
        return None

def exemplo_2_assinar_contrato(contrato_id):
    """Exemplo 2: Assinar contrato digitalmente"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Assinar Contrato Digitalmente")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db, usuario_id="cliente_456")
    
    # Simulação: base64 de uma imagem de assinatura
    # Em produção, isso viria de um canvas de desenho no navegador
    assinatura_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    try:
        contrato = service.assinar_contrato(
            contrato_id=contrato_id,
            assinatura_base64=assinatura_base64,
            hash_documento="abcdef123456789",  # Em produção, hash real do PDF
            usuario_id="cliente_456",
            nome_signatario="João Silva"
        )
        
        print(f"\n✓ Contrato assinado com sucesso!")
        print(f"  Status: {contrato.status_assinatura.value}")
        print(f"  Assinado por: João Silva")
        print(f"  Data: {contrato.data_assinatura}")
        
        return True
    except Exception as e:
        print(f"\n✗ Erro ao assinar: {e}")
        return False

def exemplo_3_liberar_contrato(contrato_id):
    """Exemplo 3: Liberar contrato (admin)"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Liberar Contrato (Admin)")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db, usuario_id="admin_001")
    
    try:
        contrato = service.liberar_contrato(
            contrato_id=contrato_id,
            usuario_id="admin_001",
            motivo="Documentação verificada e aceita pelo departamento jurídico"
        )
        
        print(f"\n✓ Contrato liberado com sucesso!")
        print(f"  ID: {contrato.id}")
        print(f"  Status: {contrato.status_assinatura.value}")
        print(f"  Liberado em: {datetime.now()}")
        
        return True
    except Exception as e:
        print(f"\n✗ Erro ao liberar: {e}")
        return False

def exemplo_4_obter_historico(contrato_id):
    """Exemplo 4: Obter histórico completo do contrato"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Histórico Completo do Contrato")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db)
    
    try:
        historico = service.obter_historico(contrato_id=contrato_id)
        
        print(f"\n✓ Histórico do contrato {contrato_id}:")
        print(f"  Total de eventos: {len(historico)}\n")
        
        for i, evento in enumerate(historico, 1):
            print(f"  [{i}] {evento['alterado_em']}")
            print(f"      Campo: {evento['campo_alterado']}")
            print(f"      Antes: {evento['valor_anterior']}")
            print(f"      Depois: {evento['valor_novo']}")
            print(f"      Por: {evento['alterado_por']}")
            print(f"      Motivo: {evento['motivo']}\n")
        
        return True
    except Exception as e:
        print(f"\n✗ Erro ao obter histórico: {e}")
        return False

def exemplo_5_monitorar_vencimentos():
    """Exemplo 5: Monitorar contratos vencendo"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Monitorar Contratos Vencendo")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db)
    
    try:
        # Contratos vencendo nos próximos 30 dias
        vencendo = service.verificar_contratos_vencendo(dias=30)
        
        print(f"\n✓ Contratos vencendo em 30 dias: {len(vencendo)}")
        for contrato in vencendo[:5]:  # Mostrar apenas os 5 primeiros
            print(f"  - {contrato.titulo}")
            print(f"    ID: {contrato.id}, Vence: {contrato.data_vigencia_fim}")
        
        # Contratos já vencidos
        vencidos = service.verificar_contratos_vencidos()
        
        print(f"\n✓ Contratos já vencidos: {len(vencidos)}")
        for contrato in vencidos[:5]:  # Mostrar apenas os 5 primeiros
            print(f"  - {contrato.titulo}")
            print(f"    ID: {contrato.id}, Venceu em: {contrato.data_vigencia_fim}")
        
        return True
    except Exception as e:
        print(f"\n✗ Erro ao monitorar: {e}")
        return False

def exemplo_6_renovar_contrato(contrato_id):
    """Exemplo 6: Renovar contrato automaticamente"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Renovar Contrato Automaticamente")
    print("="*60)
    
    db = get_db_session()
    service = ContratoService(repository_session=db, usuario_id="sistema")
    
    # Nota: O contrato precisa ter status_renovacao = "renovacao_automatica"
    # Para este exemplo, vamos apenas mostrar como seria feito
    
    print("\n⚠️  Para este exemplo funcionar, o contrato deve ter:")
    print("   status_renovacao = 'renovacao_automatica'")
    print("\nQuando aplicável, execute:")
    
    try:
        novo_contrato = service.renovar_contrato_automatico(
            contrato_id=contrato_id,
            usuario_id="sistema"
        )
        
        print(f"\n✓ Contrato renovado com sucesso!")
        print(f"  Contrato anterior: {contrato_id}")
        print(f"  Novo contrato: {novo_contrato.id}")
        print(f"  Vigência: {novo_contrato.data_vigencia_inicio} até {novo_contrato.data_vigencia_fim}")
        
        return True
    except Exception as e:
        # É esperado que falhe se o contrato não está configurado para renovação automática
        print(f"\n⚠️  Informação: {e}")
        print("  (Isso é esperado se o contrato não está configurado para renovação automática)")
        return False

def exemplo_7_via_api():
    """Exemplo 7: Usar via API HTTP"""
    print("\n" + "="*60)
    print("EXEMPLO 7: Usar via API HTTP")
    print("="*60)
    
    print("""
✓ Você pode usar via HTTP com curl ou qualquer cliente HTTP:

1. CRIAR CONTRATO:
curl -X POST http://localhost:8000/api/v1/contratos \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer SEU_TOKEN" \\
  -d '{
    "cliente_id": 1,
    "titulo": "Novo Contrato",
    "tipo_contrato": "servico",
    "data_vigencia_inicio": "2026-01-20",
    "data_vigencia_fim": "2027-01-20",
    "valor_contrato": 150.00,
    "incluir_pdf": true
  }'

2. ASSINAR:
curl -X POST http://localhost:8000/api/v1/contratos/1/assinar \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer SEU_TOKEN" \\
  -d '{
    "assinatura_base64": "iVBORw0KGgo...",
    "hash_documento": "abc123..."
  }'

3. LIBERAR:
curl -X POST "http://localhost:8000/api/v1/contratos/1/liberar?motivo=Doc%20verificada" \\
  -H "Authorization: Bearer SEU_TOKEN"

4. HISTÓRICO:
curl http://localhost:8000/api/v1/contratos/1/historico \\
  -H "Authorization: Bearer SEU_TOKEN"

5. LISTAR VENCENDO:
curl "http://localhost:8000/api/v1/contratos/vencendo/lista?dias=30" \\
  -H "Authorization: Bearer SEU_TOKEN"

6. RENOVAR:
curl -X POST http://localhost:8000/api/v1/contratos/1/renovar \\
  -H "Authorization: Bearer SEU_TOKEN"
    """)

def main():
    """Executar todos os exemplos"""
    print("\n" + "="*60)
    print("EXEMPLOS PRÁTICOS - Módulo de Contratos v2")
    print("="*60)
    
    # Exemplo 1: Criar contrato
    contrato_id = exemplo_1_criar_contrato()
    
    if contrato_id:
        # Exemplo 2: Assinar contrato
        if exemplo_2_assinar_contrato(contrato_id):
            
            # Exemplo 3: Liberar contrato
            exemplo_3_liberar_contrato(contrato_id)
            
            # Exemplo 4: Obter histórico
            exemplo_4_obter_historico(contrato_id)
    
    # Exemplo 5: Monitorar vencimentos
    exemplo_5_monitorar_vencimentos()
    
    # Exemplo 6: Renovar contrato
    if contrato_id:
        exemplo_6_renovar_contrato(contrato_id)
    
    # Exemplo 7: Via API
    exemplo_7_via_api()
    
    print("\n" + "="*60)
    print("✓ Exemplos concluídos!")
    print("="*60)

if __name__ == "__main__":
    print("""
ATENÇÃO: Este script demonstra os conceitos.
Para usar com dados reais:

1. Configure a conexão com o banco de dados corretamente
2. Certifique-se de que pelo menos 1 cliente existe (ID=1)
3. Execute: python exemplos_contratos_v2.py

Se você vê erros de cliente não encontrado, crie um primeiro:
  - Acesse a interface web
  - Ou execute um script de setup
    """)
    
    # Comentado por padrão para não executar erros
    # main()
    
    print("\n✓ Descomente 'main()' no final do arquivo para executar os exemplos")
