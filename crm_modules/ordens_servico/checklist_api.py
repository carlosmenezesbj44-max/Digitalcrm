from fastapi import APIRouter, Depends, HTTPException
from crm_modules.ordens_servico.checklist_schemas import (
    ChecklistResponse,
    ChecklistProgressSummary,
    ToggleItemRequest,
    UpdateObservacoesRequest,
    ChecklistItemWithProgress,
)
from crm_modules.ordens_servico.checklist_service import ChecklistService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()


@router.get("/{ordem_servico_id}", response_model=ChecklistResponse)
def get_checklist(ordem_servico_id: int, tipo_servico: str, db: Session = Depends(get_db)):
    """Busca o checklist completo de uma OS"""
    service = ChecklistService(session=db)
    
    # Buscar itens com progresso
    items = service.get_checklist_with_details(ordem_servico_id, tipo_servico)
    summary = service.get_progress_summary(ordem_servico_id)
    
    return ChecklistResponse(
        ordem_servico_id=ordem_servico_id,
        tipo_servico=tipo_servico,
        items=items,
        summary=summary
    )


@router.get("/{ordem_servico_id}/summary", response_model=ChecklistProgressSummary)
def get_checklist_summary(ordem_servico_id: int, db: Session = Depends(get_db)):
    """Busca apenas o resumo do progresso do checklist"""
    service = ChecklistService(session=db)
    return service.get_progress_summary(ordem_servico_id)


@router.post("/{ordem_servico_id}/items/{item_id}/toggle")
def toggle_checklist_item(
    ordem_servico_id: int,
    item_id: int,
    request: Optional[ToggleItemRequest] = None,
    db: Session = Depends(get_db)
):
    """Marca ou desmarca um item do checklist"""
    service = ChecklistService(session=db)
    
    completado_por = request.completado_por if request else None
    observacoes = request.observacoes if request else None
    
    result = service.toggle_item(ordem_servico_id, item_id, completado_por, observacoes)
    
    if not result:
        raise HTTPException(status_code=404, detail="Item não encontrado no progresso")
    
    # Retornar status atual e resumo
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "success": True,
        "completado": result.completado,
        "summary": summary
    }


@router.post("/{ordem_servico_id}/items/{item_id}/check")
def check_checklist_item(
    ordem_servico_id: int,
    item_id: int,
    request: Optional[ToggleItemRequest] = None,
    db: Session = Depends(get_db)
):
    """Marca um item como completado"""
    service = ChecklistService(session=db)
    
    completado_por = request.completado_por if request else None
    observacoes = request.observacoes if request else None
    
    result = service.check_item(ordem_servico_id, item_id, completado_por, observacoes)
    
    if not result:
        raise HTTPException(status_code=404, detail="Item não encontrado no progresso")
    
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "success": True,
        "completado": True,
        "summary": summary
    }


@router.post("/{ordem_servico_id}/items/{item_id}/uncheck")
def uncheck_checklist_item(ordem_servico_id: int, item_id: int, db: Session = Depends(get_db)):
    """Desmarca um item do checklist"""
    service = ChecklistService(session=db)
    
    result = service.uncheck_item(ordem_servico_id, item_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Item não encontrado no progresso")
    
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "success": True,
        "completado": False,
        "summary": summary
    }


@router.put("/{ordem_servico_id}/items/{item_id}/observacoes")
def update_item_observacoes(
    ordem_servico_id: int,
    item_id: int,
    request: UpdateObservacoesRequest,
    db: Session = Depends(get_db)
):
    """Atualiza as observações de um item"""
    service = ChecklistService(session=db)
    
    result = service.update_item_observacoes(ordem_servico_id, item_id, request.observacoes)
    
    if not result:
        raise HTTPException(status_code=404, detail="Item não encontrado no progresso")
    
    return {
        "success": True,
        "observacoes": result.observacoes
    }


@router.post("/{ordem_servico_id}/initialize")
def initialize_checklist(ordem_servico_id: int, tipo_servico: str, db: Session = Depends(get_db)):
    """Inicializa o checklist para uma OS"""
    service = ChecklistService(session=db)
    
    items = service.initialize_checklist(ordem_servico_id, tipo_servico)
    summary = service.get_progress_summary(ordem_servico_id)
    
    return {
        "success": True,
        "message": "Checklist inicializado",
        "summary": summary
    }


@router.get("/{ordem_servico_id}/is-complete")
def is_checklist_complete(ordem_servico_id: int, db: Session = Depends(get_db)):
    """Verifica se o checklist está completo"""
    service = ChecklistService(session=db)
    is_complete = service.is_checklist_completed(ordem_servico_id)
    
    return {
        "is_complete": is_complete
    }
