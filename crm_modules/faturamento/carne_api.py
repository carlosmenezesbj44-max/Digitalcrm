"""
API endpoints para gerenciar carnês e boletos
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from crm_modules.faturamento.carne_service import CarneService
from crm_modules.faturamento.boleto_service import BoletoService
from crm_modules.faturamento.carne_schemas import (
    CarneCreate, CarneUpdate, CarneResponse, BoletoCreate, BoletoResponse
)
from crm_modules.faturamento.carne_models import CarneModel, BoletoModel
from crm_core.db.base import get_db
from crm_core.utils.exceptions import NotFoundException, ValidationException

router = APIRouter(
    prefix="",
    tags=["faturamento"]
)


# ==================== CARNÊS ====================

@router.post("/carnes", response_model=CarneResponse)
def criar_carne(
    carne_data: CarneCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo carnê (plano de pagamento parcelado)"""
    try:
        service = CarneService(session=db)
        return service.criar_carne(carne_data)
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar carnê: {str(e)}")


@router.get("/carnes/{carne_id}", response_model=CarneResponse)
def obter_carne(
    carne_id: int,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um carnê"""
    try:
        service = CarneService(session=db)
        return service.obter_carne(carne_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/carnes", response_model=List[CarneResponse])
def listar_carnes(
    db: Session = Depends(get_db)
):
    """Lista todos os carnês"""
    try:
        from sqlalchemy.orm import joinedload
        service = CarneService(session=db)
        carnes = db.query(CarneModel).options(joinedload(CarneModel.cliente), joinedload(CarneModel.parcelas)).filter(CarneModel.ativo == True).order_by(CarneModel.data_criacao.desc()).all()
        return [service._model_to_response(c) for c in carnes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carnes/cliente/{cliente_id}", response_model=List[CarneResponse])
def listar_carnes_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """Lista todos os carnês de um cliente"""
    try:
        service = CarneService(session=db)
        return service.listar_carnes_cliente(cliente_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/carnes/{carne_id}", response_model=CarneResponse)
def atualizar_carne(
    carne_id: int,
    update_data: CarneUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um carnê"""
    try:
        service = CarneService(session=db)
        return service.atualizar_carne(carne_id, update_data)
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/carnes/{carne_id}/cancelar", response_model=CarneResponse)
def cancelar_carne(
    carne_id: int,
    db: Session = Depends(get_db)
):
    """Cancela um carnê"""
    try:
        service = CarneService(session=db)
        return service.cancelar_carne(carne_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/carnes/{carne_id}")
def excluir_carne(
    carne_id: int,
    db: Session = Depends(get_db)
):
    """Exclui um carnê permanentemente ou faz soft delete"""
    try:
        service = CarneService(session=db)
        service.excluir_carne(carne_id)
        return {"message": "Carnê excluído com sucesso"}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/carnes/{carne_id}/parcelas")
def listar_parcelas(
    carne_id: int,
    db: Session = Depends(get_db)
):
    """Lista as parcelas de um carnê"""
    try:
        service = CarneService(session=db)
        return service.listar_parcelas_carne(carne_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/parcelas/{parcela_id}/pagar")
def registrar_pagamento_parcela(
    parcela_id: int,
    valor_pago: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """Registra o pagamento de uma parcela"""
    try:
        service = CarneService(session=db)
        service.registrar_pagamento_parcela(parcela_id, valor_pago)
        return {"message": "Pagamento registrado com sucesso"}
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== BOLETOS ====================

@router.post("/boletos", response_model=BoletoResponse)
def gerar_boleto_direto(
    boleto_data: BoletoCreate,
    juros_dia: float = Query(0.0, ge=0),
    multa_atraso: float = Query(0.0, ge=0),
    db: Session = Depends(get_db)
):
    """Gera um boleto diretamente (sem estar vinculado a uma fatura)"""
    try:
        service = BoletoService(session=db)
        return service.gerar_boleto_direto(
            cliente_id=boleto_data.cliente_id,
            valor=boleto_data.valor,
            data_vencimento=boleto_data.data_vencimento,
            descricao=boleto_data.descricao or f"Boleto - R$ {boleto_data.valor}",
            juros_dia=juros_dia,
            multa_atraso=multa_atraso
        )
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar boleto: {str(e)}")


@router.post("/faturas/{fatura_id}/boleto", response_model=BoletoResponse)
def gerar_boleto_fatura(
    fatura_id: int,
    juros_dia: float = Query(0.0, ge=0),
    multa_atraso: float = Query(0.0, ge=0),
    db: Session = Depends(get_db)
):
    """Gera um boleto para uma fatura existente"""
    try:
        service = BoletoService(session=db)
        return service.gerar_boleto_fatura(
            fatura_id=fatura_id,
            juros_dia=juros_dia,
            multa_atraso=multa_atraso
        )
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar boleto: {str(e)}")


@router.get("/boletos/{boleto_id}", response_model=BoletoResponse)
def obter_boleto(
    boleto_id: int,
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um boleto"""
    try:
        service = BoletoService(session=db)
        return service.obter_boleto(boleto_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/boletos", response_model=List[BoletoResponse])
def listar_boletos(
    cliente_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista todos os boletos com filtros opcionais"""
    try:
        service = BoletoService(session=db)
        return service.listar_todos_boletos(cliente_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/boletos/cliente/{cliente_id}", response_model=List[BoletoResponse])
def listar_boletos_cliente(
    cliente_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista boletos de um cliente"""
    try:
        service = BoletoService(session=db)
        return service.listar_boletos_cliente(cliente_id, status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/boletos/vencidos/listar", response_model=List[BoletoResponse])
def listar_boletos_vencidos(
    db: Session = Depends(get_db)
):
    """Lista todos os boletos vencidos não pagos"""
    try:
        service = BoletoService(session=db)
        return service.listar_boletos_vencidos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/boletos/{boleto_id}/cancelar", response_model=BoletoResponse)
def cancelar_boleto(
    boleto_id: int,
    db: Session = Depends(get_db)
):
    """Cancela um boleto"""
    try:
        service = BoletoService(session=db)
        return service.cancelar_boleto(boleto_id)
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/boletos/{boleto_id}/sincronizar", response_model=BoletoResponse)
def sincronizar_boleto(
    boleto_id: int,
    db: Session = Depends(get_db)
):
    """Sincroniza o status de um boleto com o Gerencianet"""
    try:
        service = BoletoService(session=db)
        return service.atualizar_status_gerencianet(boleto_id)
    except (ValidationException, NotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/boletos/sincronizar/todos")
def sincronizar_todos_boletos(
    db: Session = Depends(get_db)
):
    """Sincroniza o status de todos os boletos abertos com o Gerencianet"""
    try:
        service = BoletoService(session=db)
        boletos = service.sincronizar_pagamentos_gerencianet()
        return {
            "message": f"{len(boletos)} boletos sincronizados",
            "boletos_sincronizados": len(boletos)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao sincronizar: {str(e)}")


# ==================== WEBHOOKS ====================

@router.post("/webhooks/gerencianet/boleto")
async def webhook_boleto_gerencianet(
    payload: dict,
    db: Session = Depends(get_db)
):
    """
    Webhook para atualizar status de boletos quando Gerencianet notifica
    
    O Gerencianet envia notificações quando:
    - Boleto é pago
    - Boleto vence
    - Boleto é cancelado
    """
    try:
        # Extrair informações do payload
        charge_id = payload.get("id")
        status = payload.get("status")  # paid, canceled, overdue, etc
        
        # Buscar boleto no nosso banco
        service = BoletoService(session=db)
        
        # Atualizar status baseado no webhook
        from crm_modules.faturamento.carne_models import BoletoModel
        
        boleto = db.query(BoletoModel).filter(
            BoletoModel.gerencianet_charge_id == str(charge_id)
        ).first()
        
        if boleto:
            if status == "paid":
                boleto.status = "pago"
                boleto.gerencianet_status = "pago"
            elif status == "canceled":
                boleto.status = "cancelado"
                boleto.gerencianet_status = "cancelado"
            else:
                boleto.gerencianet_status = status
            
            db.commit()
            
            return {"message": "Webhook processado com sucesso"}
        
        return {"message": "Boleto não encontrado"}
    
    except Exception as e:
        return {"error": str(e)}, 500


@router.post("/webhooks/gerencianet/subscription")
async def webhook_subscription_gerencianet(
    payload: dict,
    db: Session = Depends(get_db)
):
    """
    Webhook para atualizar status de recorrências quando Gerencianet notifica
    """
    try:
        # Extrair informações do payload
        subscription_id = payload.get("id")
        event = payload.get("event")  # payment.success, payment.failure, etc
        
        return {"message": "Webhook de recorrência processado"}
    
    except Exception as e:
        return {"error": str(e)}, 500
