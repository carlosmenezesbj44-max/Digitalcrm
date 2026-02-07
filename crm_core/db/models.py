"""
Arquivo central para importar todos os modelos do sistema.
Isso garante que todos os modelos sejam registrados no SQLAlchemy.
"""

# Importar Base primeiro
from crm_core.db.models_base import Base

# Importar todos os modelos principais
from crm_modules.clientes.models import ClienteModel, ClienteConexaoLog
from crm_modules.contratos.models import ContratoModel, ContratoHistoricoModel, ContratoTemplate
from crm_modules.faturamento.models import FaturaModel, PagamentoModel
from crm_modules.faturamento.carne_models import CarneModel, BoletoModel, ParcelaModel
from crm_modules.usuarios.models import Usuario, Permissao, AuditoriaLog
from crm_modules.dashboard.models import Dashboard, DashboardKPI, DashboardWidget, MetricHistory
from crm_modules.planos.models import PlanoModel
from crm_modules.bloqueios.models import PlanoBloqueioModel
from crm_modules.produtos.models import ProdutoModel
from crm_modules.servidores.models import ServidorModel
from crm_modules.tecnicos.models import TecnicoModel
from crm_modules.ordens_servico.models import OrdemServicoModel
from crm_modules.ordens_servico.checklist_models import ChecklistItemModel, ChecklistProgressModel
from crm_modules.clientes.models_arquivos import ClienteArquivoModel

# Exportar Base para uso em migrations
__all__ = ['Base']
