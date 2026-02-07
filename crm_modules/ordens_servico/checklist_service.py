from crm_modules.ordens_servico.checklist_models import ChecklistItemModel, ChecklistProgressModel
from crm_modules.ordens_servico.checklist_models import CHECKLIST_TEMPLATES
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional, Dict, Any


class ChecklistService:
    def __init__(self, session: Session):
        self.session = session

    def get_checklist_items_by_tipo(self, tipo_servico: str) -> List[ChecklistItemModel]:
        """Busca os itens de checklist para um tipo de serviço"""
        return self.session.query(ChecklistItemModel).filter(
            and_(
                ChecklistItemModel.tipo_servico == tipo_servico,
                ChecklistItemModel.ativo == True
            )
        ).order_by(ChecklistItemModel.ordem).all()

    def get_checklist_progress(self, ordem_servico_id: int) -> List[ChecklistProgressModel]:
        """Busca o progresso do checklist de uma OS"""
        return self.session.query(ChecklistProgressModel).filter(
            ChecklistProgressModel.ordem_servico_id == ordem_servico_id
        ).all()

    def initialize_checklist(self, ordem_servico_id: int, tipo_servico: str) -> List[ChecklistProgressModel]:
        """Inicializa o checklist para uma nova OS"""
        # Verificar se já existe checklist inicializado
        existing = self.get_checklist_progress(ordem_servico_id)
        if existing:
            return existing

        # Buscar itens do template
        items = self.get_checklist_items_by_tipo(tipo_servico)
        if not items:
            # Criar progresso vazio
            return []

        # Criar registros de progresso para cada item
        progress_records = []
        for item in items:
            progress = ChecklistProgressModel(
                ordem_servico_id=ordem_servico_id,
                item_id=item.id,
                completado=False,
                criado_automaticamente=True
            )
            self.session.add(progress)
            progress_records.append(progress)

        self.session.commit()
        return progress_records

    def toggle_item(self, ordem_servico_id: int, item_id: int, completado_por: str = None, observacoes: str = None) -> Optional[ChecklistProgressModel]:
        """Marca ou desmarca um item do checklist"""
        progress = self.session.query(ChecklistProgressModel).filter(
            and_(
                ChecklistProgressModel.ordem_servico_id == ordem_servico_id,
                ChecklistProgressModel.item_id == item_id
            )
        ).first()

        if not progress:
            return None

        # Toggle do status
        progress.completado = not progress.completado

        if progress.completado:
            progress.data_completado = datetime.utcnow()
            progress.completado_por = completado_por
        else:
            progress.data_completado = None
            progress.completado_por = None

        if observacoes:
            progress.observacoes = observacoes

        self.session.commit()
        return progress

    def check_item(self, ordem_servico_id: int, item_id: int, completado_por: str = None, observacoes: str = None) -> Optional[ChecklistProgressModel]:
        """Marca um item como completado"""
        progress = self.session.query(ChecklistProgressModel).filter(
            and_(
                ChecklistProgressModel.ordem_servico_id == ordem_servico_id,
                ChecklistProgressModel.item_id == item_id
            )
        ).first()

        if not progress:
            return None

        progress.completado = True
        progress.data_completado = datetime.utcnow()
        progress.completado_por = completado_por

        if observacoes:
            progress.observacoes = observacoes

        self.session.commit()
        return progress

    def uncheck_item(self, ordem_servico_id: int, item_id: int) -> Optional[ChecklistProgressModel]:
        """Desmarca um item do checklist"""
        progress = self.session.query(ChecklistProgressModel).filter(
            and_(
                ChecklistProgressModel.ordem_servico_id == ordem_servico_id,
                ChecklistProgressModel.item_id == item_id
            )
        ).first()

        if not progress:
            return None

        progress.completado = False
        progress.data_completado = None
        progress.completado_por = None

        self.session.commit()
        return progress

    def get_progress_summary(self, ordem_servico_id: int) -> Dict[str, Any]:
        """Retorna o resumo do progresso (X de Y tarefas concluídas)"""
        progress_list = self.get_checklist_progress(ordem_servico_id)
        
        total = len(progress_list)
        completed = sum(1 for p in progress_list if p.completado)
        
        return {
            "total": total,
            "completed": completed,
            "percentage": round((completed / total * 100), 2) if total > 0 else 0,
            "is_complete": completed == total and total > 0
        }

    def get_checklist_with_details(self, ordem_servico_id: int, tipo_servico: str) -> List[Dict[str, Any]]:
        """Retorna o checklist completo com detalhes"""
        # Inicializar checklist se necessário
        self.initialize_checklist(ordem_servico_id, tipo_servico)
        
        # Buscar itens
        items = self.get_checklist_items_by_tipo(tipo_servico)
        
        # Buscar progresso
        progress_dict = {p.item_id: p for p in self.get_checklist_progress(ordem_servico_id)}
        
        result = []
        for item in items:
            progress = progress_dict.get(item.id)
            result.append({
                "id": item.id,
                "nome_tarefa": item.nome_tarefa,
                "descricao": item.descricao,
                "ordem": item.ordem,
                "completado": progress.completado if progress else False,
                "data_completado": progress.data_completado if progress else None,
                "completado_por": progress.completado_por if progress else None,
                "observacoes": progress.observacoes if progress else None
            })
        
        return result

    def update_item_observacoes(self, ordem_servico_id: int, item_id: int, observacoes: str) -> Optional[ChecklistProgressModel]:
        """Atualiza as observações de um item"""
        progress = self.session.query(ChecklistProgressModel).filter(
            and_(
                ChecklistProgressModel.ordem_servico_id == ordem_servico_id,
                ChecklistProgressModel.item_id == item_id
            )
        ).first()

        if not progress:
            return None

        progress.observacoes = observacoes
        self.session.commit()
        return progress

    def is_checklist_completed(self, ordem_servico_id: int) -> bool:
        """Verifica se todos os itens do checklist foram completados"""
        summary = self.get_progress_summary(ordem_servico_id)
        return summary["is_complete"]
