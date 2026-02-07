from pydantic import BaseModel
from typing import Optional


class ProdutoCreate(BaseModel):
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


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    preco: Optional[float] = None
    categoria: Optional[str] = None
    unidade: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None
    preco_custo: Optional[float] = None
    sku: Optional[str] = None
    codigo_barras: Optional[str] = None
    quantidade_estoque: Optional[float] = None
    estoque_minimo: Optional[float] = None
    ncm: Optional[str] = None
    cfop: Optional[str] = None
    icms: Optional[float] = None
    fornecedor: Optional[str] = None
    imagem_url: Optional[str] = None


class ProdutoResponse(BaseModel):
    id: int
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