from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from crm_core.db.repositories import BaseRepository
from crm_modules.clientes.models import ClienteModel
from crm_core.db.base import SessionLocal


class ClienteRepository(BaseRepository[ClienteModel]):
    def __init__(self, session: Optional[Session] = None):
        """If a `session` is provided, the repository will use it and will not
        close it on cleanup. If no session is provided, the repository will
        create its own using `SessionLocal()`.
        """
        self._external_session = session is not None
        session = session or SessionLocal()
        super().__init__(session, ClienteModel)

    def get_by_email(self, email: str) -> ClienteModel:
        return self.session.query(ClienteModel).filter(ClienteModel.email == email).first()

    def get_by_cpf(self, cpf: str) -> ClienteModel:
        return self.session.query(ClienteModel).filter(ClienteModel.cpf == cpf).first()

    def get_active_clients(self):
        return self.session.query(ClienteModel).filter(ClienteModel.ativo == True).all()

    def search_by_name(self, name: str):
        return self.session.query(ClienteModel).filter(ClienteModel.nome.ilike(f'%{name}%')).all()

    def get_filtered_clients(self, q: str, status: str, page: int, per_page: int, field: str = "todos"):
        query = self.session.query(ClienteModel)
        if q:
            term = f"%{q}%"
            if field == "nome":
                query = query.filter(ClienteModel.nome.ilike(term))
            elif field == "email":
                query = query.filter(ClienteModel.email.ilike(term))
            elif field == "cpf/cnpj":
                query = query.filter(ClienteModel.cpf.ilike(term))
            elif field == "endereco":
                query = query.filter(
                    or_(
                        ClienteModel.rua.ilike(term),
                        ClienteModel.endereco.ilike(term),
                        ClienteModel.bairro.ilike(term),
                        ClienteModel.cidade.ilike(term)
                    )
                )
            elif field == "login":
                query = query.filter(ClienteModel.username.ilike(term))
            else: # todos
                    query = query.filter(
                        or_(
                            ClienteModel.nome.ilike(term),
                            ClienteModel.cpf.ilike(term),
                            ClienteModel.rua.ilike(term),
                            ClienteModel.endereco.ilike(term),
                            ClienteModel.bairro.ilike(term),
                            ClienteModel.cidade.ilike(term)
                        )
                    )
        if status:
            query = query.filter(ClienteModel.status_contrato == status)
        total = query.count()
        offset = (page - 1) * per_page
        items = query.order_by(desc(ClienteModel.id)).offset(offset).limit(per_page).all()
        return items, total

    def close(self):
        if not self._external_session:
            try:
                self.session.close()
            except Exception:
                pass
