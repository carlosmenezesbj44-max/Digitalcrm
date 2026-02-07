from fastapi import APIRouter, Depends, HTTPException
from crm_modules.ordens_servico.schemas import OrdemServicoCreate, OrdemServicoUpdate, OrdemServico
from crm_modules.ordens_servico.service import OrdemServicoService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()


@router.post("/", response_model=OrdemServico)
def criar_ordem_servico(ordem: OrdemServicoCreate, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        return service.criar_ordem_servico(ordem)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{ordem_id}", response_model=OrdemServico)
def obter_ordem_servico(ordem_id: int, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        return service.obter_ordem_servico(ordem_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{ordem_id}", response_model=OrdemServico)
def atualizar_ordem_servico(ordem_id: int, ordem: OrdemServicoUpdate, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        return service.atualizar_ordem_servico(ordem_id, ordem)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_id}/iniciar")
def iniciar_ordem_servico(ordem_id: int, tecnico: str, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        service.iniciar_ordem_servico(ordem_id, tecnico)
        return {"message": "Ordem de serviço iniciada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_id}/aguardando-peca")
def aguardando_peca_ordem_servico(ordem_id: int, observacoes: Optional[str] = None, db: Session = Depends(get_db)):
    """Marca a OS como aguardando peça"""
    service = OrdemServicoService(repository_session=db)
    try:
        service.aguardando_peca_ordem_servico(ordem_id, observacoes)
        return {"message": "Ordem de serviço marcada como aguardando peça"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_id}/retomar")
def retomar_ordem_servico(ordem_id: int, db: Session = Depends(get_db)):
    """Retoma a OS de Aguardando Peça para Em Andamento"""
    service = OrdemServicoService(repository_session=db)
    try:
        service.retomar_ordem_servico(ordem_id)
        return {"message": "Ordem de serviço retomada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_id}/concluir")
def concluir_ordem_servico(ordem_id: int, observacoes: Optional[str] = None, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        service.concluir_ordem_servico(ordem_id, observacoes)
        return {"message": "Ordem de serviço concluída"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{ordem_id}/cancelar")
def cancelar_ordem_servico(ordem_id: int, motivo: str, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    try:
        service.cancelar_ordem_servico(ordem_id, motivo)
        return {"message": "Ordem de serviço cancelada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[OrdemServico])
def listar_ordens_servico(status: Optional[str] = None, cliente_id: Optional[int] = None, db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    if cliente_id:
        return service.listar_ordens_por_cliente(cliente_id)
    elif status:
        return service.listar_ordens_por_status(status)
    else:
        return service.listar_todas_ordens()


@router.get("/abertas/", response_model=list[OrdemServico])
def listar_ordens_abertas(db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    return service.listar_ordens_abertas()


@router.get("/em_andamento/", response_model=list[OrdemServico])
def listar_ordens_em_andamento(db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    return service.listar_ordens_em_andamento()


@router.get("/concluidas/", response_model=list[OrdemServico])
def listar_ordens_concluidas(db: Session = Depends(get_db)):
    service = OrdemServicoService(repository_session=db)
    return service.listar_ordens_concluidas()