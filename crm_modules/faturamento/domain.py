from typing import Optional, List
from datetime import date, datetime


class Fatura:
    def __init__(self, id: int, cliente_id: int, numero_fatura: str, data_emissao: datetime,
                 data_vencimento: date, valor_total: float, status: str = "pendente",
                 valor_pago: float = 0.0, descricao: Optional[str] = None, ativo: bool = True):
        self.id = id
        self.cliente_id = cliente_id
        self.numero_fatura = numero_fatura
        self.data_emissao = data_emissao
        self.data_vencimento = data_vencimento
        self.valor_total = valor_total
        self.status = status
        self.valor_pago = valor_pago
        self.descricao = descricao
        self.ativo = ativo


class Pagamento:
    def __init__(self, id: int, fatura_id: int, valor_pago: float, data_pagamento: datetime,
                 metodo_pagamento: str, referencia: Optional[str] = None,
                 observacoes: Optional[str] = None, ativo: bool = True):
        self.id = id
        self.fatura_id = fatura_id
        self.valor_pago = valor_pago
        self.data_pagamento = data_pagamento
        self.metodo_pagamento = metodo_pagamento
        self.referencia = referencia
        self.observacoes = observacoes
        self.ativo = ativo