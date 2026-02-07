#!/usr/bin/env python3
"""
Script para testar a criação de contratos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import all models to register relationships
from crm_core.db.models_base import Base
from crm_modules.clientes.models import ClienteModel, ClienteConexaoLog
from crm_modules.faturamento.models import FaturaModel
from crm_modules.faturamento.carne_models import CarneModel, BoletoModel
from crm_modules.ordens_servico.models import OrdemServicoModel
from crm_modules.planos.models import PlanoModel
from crm_modules.servidores.models import ServidorModel
from crm_modules.contratos.models import ContratoModel

from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import ContratoCreate

def test_criar_contrato():
    """Testa criação de contrato"""
    try:
        service = ContratoService()

        # Criar contrato para cliente ID 1
        contrato_data = ContratoCreate(
            cliente_id=1,
            titulo="Contrato de Prestação de Serviços de Internet",
            descricao="Contrato padrão para serviços de internet banda larga"
        )

        contrato = service.criar_contrato(contrato_data)
        print(f"Contrato criado com sucesso: ID {contrato.id}")
        print(f"Status: {contrato.status_assinatura}")
        return True

    except Exception as e:
        print(f"Erro ao criar contrato: {e}")
        return False

if __name__ == "__main__":
    test_criar_contrato()
