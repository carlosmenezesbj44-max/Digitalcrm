from crm_core.db.repositories import BaseRepository
from crm_modules.tecnicos.models import TecnicoModel


class TecnicoRepository(BaseRepository):
    def __init__(self, session=None):
        super().__init__(session, TecnicoModel)

    def listar_ativos(self):
        return self.session.query(TecnicoModel).filter_by(ativo=True).all()

    def obter_por_email(self, email: str):
        return self.session.query(TecnicoModel).filter_by(email=email).first()
