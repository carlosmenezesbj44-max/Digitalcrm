from crm_provedor.tasks.worker import celery_app
from crm_modules.faturamento.service import FaturamentoService
from datetime import datetime


@celery_app.task
def processar_faturamento():
    """Processa faturamento mensal."""
    service = FaturamentoService()
    now = datetime.now()
    mes = now.month
    ano = now.year
    faturas = service.gerar_faturas_mensais(mes, ano)
    return f"Faturamento processado: {len(faturas)} faturas geradas"


@celery_app.task
def enviar_notificacoes_faturamento():
    """Envia notificações de faturamento."""
    # Lógica para enviar notificações
    return "Notificações enviadas"
