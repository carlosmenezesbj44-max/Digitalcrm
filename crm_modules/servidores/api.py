from fastapi import APIRouter, Depends, HTTPException
from typing import List
from crm_modules.servidores.schemas import ServidorCreate, ServidorUpdate, Servidor
from crm_modules.servidores.service import ServidorService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Servidores"])


@router.post("/", response_model=Servidor)
def criar_servidor(servidor: ServidorCreate, db: Session = Depends(get_db)):
    service = ServidorService(repository_session=db)
    try:
        return service.criar_servidor(servidor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{servidor_id}", response_model=Servidor)
def obter_servidor(servidor_id: int, db: Session = Depends(get_db)):
    service = ServidorService(repository_session=db)
    try:
        return service.obter_servidor(servidor_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{servidor_id}", response_model=Servidor)
def atualizar_servidor(servidor_id: int, servidor: ServidorUpdate, db: Session = Depends(get_db)):
    service = ServidorService(repository_session=db)
    try:
        return service.atualizar_servidor(servidor_id, servidor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{servidor_id}")
def desativar_servidor(servidor_id: int, db: Session = Depends(get_db)):
    service = ServidorService(repository_session=db)
    try:
        service.desativar_servidor(servidor_id)
        return {"message": "Servidor desativado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def listar_servidores(db: Session = Depends(get_db)):
    service = ServidorService(repository_session=db)
    try:
        servidores = service.listar_servidores()
        return {"servidores": servidores}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))