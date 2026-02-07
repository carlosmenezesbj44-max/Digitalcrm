from fastapi import APIRouter, Depends, HTTPException
from crm_modules.planos.schemas import PlanoCreate, PlanoUpdate, PlanoResponse
from crm_modules.planos.service import PlanoService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=PlanoResponse)
def criar_plano(plano: PlanoCreate, db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    try:
        return service.criar_plano(plano)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{plano_id}", response_model=PlanoResponse)
def obter_plano(plano_id: int, db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    try:
        return service.obter_plano(plano_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{plano_id}", response_model=PlanoResponse)
def atualizar_plano(plano_id: int, plano: PlanoUpdate, db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    try:
        return service.atualizar_plano(plano_id, plano)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{plano_id}")
def desativar_plano(plano_id: int, db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    try:
        service.desativar_plano(plano_id)
        return {"message": "Plano desativado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def listar_planos_ativos(db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    planos = service.listar_planos_ativos()
    return planos


@router.get("/search")
def buscar_planos(q: str = "", db: Session = Depends(get_db)):
    service = PlanoService(repository_session=db)
    try:
        planos = service.buscar_planos_por_nome(q)
        return planos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))