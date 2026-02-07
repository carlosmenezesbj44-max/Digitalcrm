from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from crm_modules.produtos.schemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from crm_modules.produtos.service import ProdutoService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    service = ProdutoService(repository_session=db)
    try:
        return service.criar_produto(produto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{produto_id}", response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    service = ProdutoService(repository_session=db)
    try:
        return service.obter_produto(produto_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    service = ProdutoService(repository_session=db)
    try:
        return service.atualizar_produto(produto_id, produto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    service = ProdutoService(repository_session=db)
    try:
        service.excluir_produto(produto_id)
        return {"message": "Produto excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    search: Optional[str] = Query(None, description="Buscar por nome ou descrição"),
    sort_by: Optional[str] = Query("nome", description="Campo para ordenação"),
    sort_order: Optional[str] = Query("asc", description="Ordem: asc ou desc"),
    page: int = Query(1, ge=1, description="Página atual"),
    per_page: int = Query(10, ge=1, le=100, description="Itens por página")
):
    service = ProdutoService(repository_session=db)
    try:
        result = service.listar_produtos_com_filtros(
            tipo=tipo,
            categoria=categoria,
            ativo=ativo,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))