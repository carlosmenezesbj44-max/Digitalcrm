from crm_provedor.tasks.worker import celery_app


@celery_app.task
def enviar_notificacao_email(destinatario: str, assunto: str, mensagem: str):
    """Envia notificação por email."""
    # Lógica para enviar email
    return f"Email enviado para {destinatario}"


@celery_app.task
def enviar_notificacao_sms(destinatario: str, mensagem: str):
    """Envia notificação por SMS."""
    # Lógica para enviar SMS
    return f"SMS enviado para {destinatario}"
