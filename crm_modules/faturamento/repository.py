from typing import Optional, List
from sqlalchemy.orm import Session
from crm_modules.faturamento.models import FaturaModel, PagamentoModel
from crm_core.db.repositories import BaseRepository
from crm_core.db.base import get_db_session


class FaturamentoRepository(BaseRepository):
    def __init__(self, session: Optional[Session] = None):
        if session is not None:
            super().__init__(session, FaturaModel)
        else:
            super().__init__(get_db_session(), FaturaModel)

    def get_faturas_by_cliente(self, cliente_id: int) -> List[FaturaModel]:
        return self.session.query(FaturaModel).filter(FaturaModel.cliente_id == cliente_id, FaturaModel.ativo == True).all()

    def get_all_faturas(self) -> List[FaturaModel]:
        return self.session.query(FaturaModel).filter(FaturaModel.ativo == True).order_by(FaturaModel.id.desc()).all()

    def get_faturas_pendentes(self) -> List[FaturaModel]:
        return self.session.query(FaturaModel).filter(FaturaModel.status == "pendente", FaturaModel.ativo == True).all()

    def get_pagamentos_by_fatura(self, fatura_id: int) -> List[PagamentoModel]:
        return self.session.query(PagamentoModel).filter(PagamentoModel.fatura_id == fatura_id, PagamentoModel.ativo == True).all()

    def get_all_pagamentos(self) -> List[PagamentoModel]:
        return self.session.query(PagamentoModel).filter(PagamentoModel.ativo == True).order_by(PagamentoModel.data_pagamento.desc()).all()

    def calcular_total_pago_fatura(self, fatura_id: int) -> float:
        from sqlalchemy import func
        result = self.session.query(func.sum(PagamentoModel.valor_pago)).filter(
            PagamentoModel.fatura_id == fatura_id,
            PagamentoModel.ativo == True
        ).scalar()
        return result if result else 0.0