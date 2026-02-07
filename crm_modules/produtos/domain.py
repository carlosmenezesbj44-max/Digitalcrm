from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Produto:
    id: Optional[int]
    nome: str
    tipo: str
    preco: float
    categoria: str
    unidade: str
    descricao: Optional[str] = None
    ativo: bool = True
    preco_custo: Optional[float] = None
    sku: Optional[str] = None
    codigo_barras: Optional[str] = None
    quantidade_estoque: float = 0.0
    estoque_minimo: float = 0.0
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    icms: float = 0.0
    fornecedor: Optional[str] = None
    imagem_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None