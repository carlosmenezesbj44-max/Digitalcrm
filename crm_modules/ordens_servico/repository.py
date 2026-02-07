from typing import Optional, List
from sqlalchemy.orm import Session
from crm_core.db.repositories import BaseRepository
from crm_modules.ordens_servico.models import OrdemServicoModel
from crm_core.db.base import SessionLocal


class OrdemServicoRepository(BaseRepository[OrdemServicoModel]):
    def __init__(self, session: Optional[Session] = None):
        """If a `session` is provided, the repository will use it and will not
        close it on cleanup. If no session is provided, the repository will
        create its own using `SessionLocal()`.
        """
        self._external_session = session is not None
        session = session or SessionLocal()
        super().__init__(session, OrdemServicoModel)

    def get_by_cliente_id(self, cliente_id: int) -> List[OrdemServicoModel]:
        return self.session.query(OrdemServicoModel).filter(OrdemServicoModel.cliente_id == cliente_id).all()

    def get_by_status(self, status: str) -> List[OrdemServicoModel]:
        return self.session.query(OrdemServicoModel).filter(OrdemServicoModel.status == status).all()

    def get_by_tipo_servico(self, tipo_servico: str) -> List[OrdemServicoModel]:
        return self.session.query(OrdemServicoModel).filter(OrdemServicoModel.tipo_servico == tipo_servico).all()

    def get_abertas(self) -> List[OrdemServicoModel]:
        return self.get_by_status("aberta")

    def get_em_andamento(self) -> List[OrdemServicoModel]:
        return self.get_by_status("em_andamento")

    def get_concluidas(self) -> List[OrdemServicoModel]:
        return self.get_by_status("concluida")

    def get_stats(self) -> dict:
        from sqlalchemy import func
        stats = self.session.query(
            OrdemServicoModel.status, func.count(OrdemServicoModel.id)
        ).group_by(OrdemServicoModel.status).all()
        
        result = {
            "total": self.session.query(OrdemServicoModel).count(),
            "aberta": 0,
            "em_andamento": 0,
            "aguardando_peca": 0,
            "concluida": 0,
            "cancelada": 0
        }
        
        for status, count in stats:
            if status in result:
                result[status] = count
                
        return result

    def get_ordens_com_filtros(
        self,
        status: Optional[str] = None,
        tipo_servico: Optional[str] = None,
        cliente_id: Optional[int] = None,
        tecnico: Optional[str] = None,
        prioridade: Optional[str] = None,
        endereco: Optional[str] = None,
        search: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        sort_by: Optional[str] = "data_criacao",
        sort_order: Optional[str] = "desc",
        page: int = 1,
        per_page: int = 10
    ) -> tuple[list[OrdemServicoModel], int]:
        from sqlalchemy import or_, desc, asc
        from datetime import datetime
        query = self.session.query(OrdemServicoModel)
        if status:
            query = query.filter(OrdemServicoModel.status == status)
        if tipo_servico:
            query = query.filter(OrdemServicoModel.tipo_servico == tipo_servico)
        if cliente_id:
            query = query.filter(OrdemServicoModel.cliente_id == cliente_id)
        if tecnico:
            query = query.filter(OrdemServicoModel.tecnico_responsavel.ilike(f"%{tecnico}%"))
        if prioridade:
            query = query.filter(OrdemServicoModel.prioridade == prioridade)
        if endereco:
            query = query.filter(OrdemServicoModel.endereco_atendimento.ilike(f"%{endereco}%"))
        
        if data_inicio:
            try:
                dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                query = query.filter(OrdemServicoModel.data_criacao >= dt_inicio)
            except ValueError:
                pass
        if data_fim:
            try:
                # Adicionar 23:59:59 para incluir todo o dia final
                dt_fim = datetime.strptime(f"{data_fim} 23:59:59", "%Y-%m-%d %H:%M:%S")
                query = query.filter(OrdemServicoModel.data_criacao <= dt_fim)
            except ValueError:
                pass

        if search:
            term = f"%{search}%"
            query = query.filter(
                or_(
                    OrdemServicoModel.titulo.ilike(term),
                    OrdemServicoModel.descricao.ilike(term),
                    OrdemServicoModel.endereco_atendimento.ilike(term),
                    OrdemServicoModel.tecnico_responsavel.ilike(term),
                )
            )
        if sort_by:
            column = getattr(OrdemServicoModel, sort_by, OrdemServicoModel.data_criacao)
            query = query.order_by(desc(column) if sort_order == "desc" else asc(column))
        total = query.count()
        offset = (page - 1) * per_page
        models = query.offset(offset).limit(per_page).all()
        return models, total

    def close(self):
        if not self._external_session:
            try:
                self.session.close()
            except Exception:
                pass
