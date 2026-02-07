from sqlalchemy.orm import Session
from crm_modules.servidores.models import ServidorModel
from crm_core.db.repositories import BaseRepository


class ServidorRepository(BaseRepository):
    def __init__(self, session: Session = None):
        if session is not None:
            super().__init__(session, ServidorModel)
        else:
            super().__init__(get_db_session(), ServidorModel)

    def get_by_ip(self, ip: str):
        return self.session.query(ServidorModel).filter(ServidorModel.ip == ip).first()

    def get_active_servers(self):
        return self.session.query(ServidorModel).filter(ServidorModel.ativo == True).all()

    def listar_servidores_ativos(self):
        return self.session.query(ServidorModel).filter(ServidorModel.ativo == True).all()