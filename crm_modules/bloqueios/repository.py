from typing import Optional
from sqlalchemy.orm import Session
from crm_modules.bloqueios.models import PlanoBloqueioModel
from crm_core.db.repositories import BaseRepository
from crm_core.db.base import get_db_session


class PlanoBloqueioRepository(BaseRepository):
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, PlanoBloqueioModel)
        else:
            super().__init__(get_db_session(), PlanoBloqueioModel)

    def get_active_planos_bloqueio(self):
        return self.session.query(PlanoBloqueioModel).filter(PlanoBloqueioModel.ativo == True).all()