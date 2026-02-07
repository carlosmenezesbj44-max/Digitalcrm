from typing import Optional
from sqlalchemy.orm import Session
from crm_modules.planos.models import PlanoModel
from crm_core.db.repositories import BaseRepository
from crm_core.db.base import get_db_session


class PlanoRepository(BaseRepository):
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, PlanoModel)
        else:
            super().__init__(get_db_session(), PlanoModel)

    def get_active_planos(self):
        return self.session.query(PlanoModel).filter(PlanoModel.ativo == True).all()

    def search_by_name(self, name: str):
        return self.session.query(PlanoModel).filter(PlanoModel.nome.ilike(f'%{name}%')).all()