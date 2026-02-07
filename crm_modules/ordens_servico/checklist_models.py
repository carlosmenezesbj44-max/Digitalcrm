from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from crm_core.db.models import Base
from datetime import datetime


class ChecklistItemModel(Base):
    """Tarefas predefinidas por tipo de serviço"""
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    tipo_servico = Column(String, nullable=False)  # "instalacao", "suporte", "manutencao"
    nome_tarefa = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    ordem = Column(Integer, default=0)  # ordem de exibição
    ativo = Column(Boolean, default=True)  # se está ativo no template
    data_criacao = Column(DateTime, default=datetime.utcnow)


class ChecklistProgressModel(Base):
    """Progresso do checklist de cada OS"""
    __tablename__ = "checklist_progress"

    id = Column(Integer, primary_key=True, index=True)
    ordem_servico_id = Column(Integer, ForeignKey('ordens_servico.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('checklist_items.id'), nullable=False)
    completado = Column(Boolean, default=False)
    data_completado = Column(DateTime, nullable=True)
    completado_por = Column(String, nullable=True)  # nome do técnico/usuário
    observacoes = Column(Text, nullable=True)  # observações específicas da tarefa

    # Campos para controlar criação automática de itens
    criado_automaticamente = Column(Boolean, default=True)


# Templates de checklist por tipo de serviço
CHECKLIST_TEMPLATES = {
    "instalacao": [
        {"nome_tarefa": "Verificar sinal", "ordem": 1, "descricao": "Testar nível de sinal no ponto de instalação"},
        {"nome_tarefa": "Configurar PPPoE", "ordem": 2, "descricao": "Criar e configurar conexão PPPoE no cliente"},
        {"nome_tarefa": "Testar velocidade", "ordem": 3, "descricao": "Realizar teste de velocidade e estabilidade"},
        {"nome_tarefa": "Orientar cliente", "ordem": 4, "descricao": "Explicar uso do serviço e Wi-Fi ao cliente"},
        {"nome_tarefa": "Finalizar", "ordem": 5, "descricao": "Finalizar instalação e coletar assinatura do cliente"},
    ],
    "suporte": [
        {"nome_tarefa": "Diagnosticar problema", "ordem": 1, "descrição": "Identificar causa raiz do problema reportado"},
        {"nome_tarefa": "Verificar cabo", "ordem": 2, "descricao": "Inspecionar e substituir cabos danificados"},
        {"nome_tarefa": "Reiniciar equipamento", "ordem": 3, "descricao": "Reiniciar roteador/ONU conforme procedimento"},
        {"nome_tarefa": "Testar conectividade", "ordem": 4, "descricao": "Verificar conexão após intervenções"},
        {"nome_tarefa": "Solucionar", "ordem": 5, "descricao": "Aplicar solução definitiva ou escalar"},
    ],
    "manutencao": [
        {"nome_tarefa": "Inspecionar equipamentos", "ordem": 1, "descricao": "Verificar estado físico de equipamentos"},
        {"nome_tarefa": "Limpar conexões", "ordem": 2, "descricao": "Limpar conectores e terminais"},
        {"nome_tarefa": "Verificar redundância", "ordem": 3, "descricao": "Testar caminhos redundantes de rede"},
        {"nome_tarefa": "Documentar ações", "ordem": 4, "descricao": "Registrar todas as manutenções realizadas"},
        {"nome_tarefa": "Finalizar", "ordem": 5, "descricao": "Confirmar funcionamento e encerrar OS"},
    ],
}
