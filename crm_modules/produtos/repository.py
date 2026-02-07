from typing import Optional
from sqlalchemy.orm import Session
from crm_modules.produtos.models import ProdutoModel
from crm_core.db.repositories import BaseRepository
from crm_core.db.base import SessionLocal


class ProdutoRepository(BaseRepository):
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, ProdutoModel)
        else:
            super().__init__(SessionLocal(), ProdutoModel)

    def get_active_produtos(self):
        return self.session.query(ProdutoModel).filter(ProdutoModel.ativo == True).all()

    def get_by_nome(self, nome: str) -> Optional[ProdutoModel]:
        return self.session.query(ProdutoModel).filter(ProdutoModel.nome == nome).first()

    def get_produtos_com_filtros(
        self,
        tipo: Optional[str] = None,
        categoria: Optional[str] = None,
        ativo: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "nome",
        sort_order: Optional[str] = "asc",
        page: int = 1,
        per_page: int = 10
    ):
        from sqlalchemy import or_, desc, asc

        query = self.session.query(ProdutoModel)

        # Aplicar filtros
        if tipo:
            query = query.filter(ProdutoModel.tipo == tipo)
        if categoria:
            query = query.filter(ProdutoModel.categoria == categoria)
        if ativo is not None:
            query = query.filter(ProdutoModel.ativo == ativo)
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    ProdutoModel.nome.ilike(search_term),
                    ProdutoModel.descricao.ilike(search_term)
                )
            )

        # Aplicar ordenação
        if sort_by:
            column = getattr(ProdutoModel, sort_by, ProdutoModel.nome)
            if sort_order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        # Contar total antes da paginação
        total = query.count()

        # Aplicar paginação
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        return query.all(), total