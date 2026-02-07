"""API para Contratos"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crm_modules.contratos.service import ContratoService
from crm_modules.contratos.schemas import (
    ContratoCreate, ContratoUpdate, ContratoResponse, AssinaturaDigitalRequest,
    ContratoHistoricoResponse
)
from crm_core.security.dependencies import obter_usuario_atual, verificar_permissao
from interfaces.api.dependencies import get_db
from crm_core.utils.exceptions import NotFoundException, ValidationException

router = APIRouter(prefix="/api/v1/contratos", tags=["contratos"])


@router.post("", response_model=ContratoResponse)
def criar_contrato(
    contrato: ContratoCreate,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Cria um novo contrato para um cliente com geração automática de PDF"""
    try:
        service = ContratoService(repository_session=db, usuario_id=usuario_atual.id)
        contrato_criado = service.criar_contrato(contrato, usuario_id=usuario_atual.id)
        return contrato_criado
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar contrato: {str(e)}")


@router.get("", response_model=list[ContratoResponse])
def listar_contratos(
    limite: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Lista todos os contratos (com paginação)"""
    try:
        service = ContratoService(repository_session=db)
        return service.listar_todos_contratos(limite=limite, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contrato_id}", response_model=ContratoResponse)
def obter_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Obtém detalhes de um contrato"""
    try:
        service = ContratoService(repository_session=db)
        return service.obter_contrato(contrato_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cliente/{cliente_id}", response_model=list[ContratoResponse])
def listar_contratos_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Lista todos os contratos de um cliente"""
    try:
        service = ContratoService(repository_session=db)
        return service.listar_contratos_por_cliente(cliente_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contrato_id}/historico", response_model=list[ContratoHistoricoResponse])
def obter_historico_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Obtém histórico completo de alterações de um contrato"""
    try:
        service = ContratoService(repository_session=db)
        return service.obter_historico(contrato_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{contrato_id}/assinar")
def assinar_contrato(
    contrato_id: int,
    assinatura: AssinaturaDigitalRequest,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Assina digitalmente um contrato (cliente) com auditoria"""
    try:
        service = ContratoService(repository_session=db, usuario_id=usuario_atual.id)
        contrato = service.assinar_contrato(
            contrato_id,
            assinatura.assinatura_base64,
            assinatura.hash_documento,
            usuario_id=usuario_atual.id,
            nome_signatario=usuario_atual.nome or "Usuário"
        )
        return {"message": "Contrato assinado com sucesso", "contrato": contrato}
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{contrato_id}/liberar")
def liberar_contrato(
    contrato_id: int,
    motivo: str = Query(None),
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Libera contrato manualmente (admin) com auditoria"""
    try:
        # Verificar permissão de admin
        verificar_permissao("manage", "contratos")
        
        service = ContratoService(repository_session=db, usuario_id=usuario_atual.id)
        contrato = service.liberar_contrato(
            contrato_id,
            usuario_id=usuario_atual.id,
            motivo=motivo
        )
        return {"message": "Contrato liberado com sucesso", "contrato": contrato}
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vencendo/lista")
def listar_contratos_vencendo(
    dias: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Lista contratos que vencem nos próximos N dias"""
    try:
        service = ContratoService(repository_session=db)
        contratos = service.verificar_contratos_vencendo(dias=dias)
        return {
            "dias_alerta": dias,
            "total": len(contratos),
            "contratos": contratos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vencidos/lista")
def listar_contratos_vencidos(
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Lista contratos que já venceram"""
    try:
        service = ContratoService(repository_session=db)
        contratos = service.verificar_contratos_vencidos()
        return {
            "total": len(contratos),
            "contratos": contratos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{contrato_id}/renovar")
def renovar_contrato(
    contrato_id: int,
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Renova automaticamente um contrato (se configurado)"""
    try:
        service = ContratoService(repository_session=db, usuario_id=usuario_atual.id)
        novo_contrato = service.renovar_contrato_automatico(
            contrato_id,
            usuario_id=usuario_atual.id
        )
        return {
            "message": "Contrato renovado com sucesso",
            "contrato_anterior": contrato_id,
            "novo_contrato": novo_contrato
        }
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{contrato_id}/pdf")
def gerar_pdf_contrato(
    contrato_id: int,
    empresa_nome: str = Query(None),
    empresa_cnpj: str = Query(None),
    empresa_endereco: str = Query(None),
    empresa_telefone: str = Query(None),
    empresa_email: str = Query(None),
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Gera e retorna PDF de um contrato existente"""
    try:
        service = ContratoService(repository_session=db)

        # Preparar dados da empresa
        empresa_dados = {}
        if empresa_nome:
            empresa_dados['nome'] = empresa_nome
        if empresa_cnpj:
            empresa_dados['cnpj'] = empresa_cnpj
        if empresa_endereco:
            empresa_dados['endereco'] = empresa_endereco
        if empresa_telefone:
            empresa_dados['telefone'] = empresa_telefone
        if empresa_email:
            empresa_dados['email'] = empresa_email

        pdf_bytes = service.gerar_pdf_contrato(contrato_id, empresa_dados or None)

        from fastapi.responses import Response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=contrato_{contrato_id}.pdf"}
        )
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")


@router.delete("/{contrato_id}")
def deletar_contrato(
    contrato_id: int,
    motivo: str = Query(None),
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Deleta um contrato (soft delete) com auditoria"""
    try:
        # Verificar permissão de admin (opcional, mas recomendado)
        verificar_permissao("manage", "contratos")
        
        service = ContratoService(repository_session=db, usuario_id=usuario_atual.id)
        sucesso = service.deletar_contrato(
            contrato_id,
            usuario_id=usuario_atual.id,
            motivo=motivo
        )
        
        if not sucesso:
            raise HTTPException(status_code=400, detail="Não foi possível deletar o contrato")
            
        return {"message": "Contrato deletado com sucesso", "id": contrato_id}
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/realtime")
def obter_estatisticas_tempo_real(
    db: Session = Depends(get_db),
    usuario_atual = Depends(obter_usuario_atual)
):
    """Obtém estatísticas em tempo real para indicadores visuais no menu"""
    try:
        service = ContratoService(repository_session=db)
        stats = service.obter_estatisticas_contratos()

        # Adicionar estatísticas adicionais para o menu
        stats_realtime = {
            'total': stats.get('total', 0),
            'aguardando': stats.get('aguardando', 0),
            'assinado': stats.get('assinado', 0),
            'liberado': stats.get('liberado', 0),
            'vencendo_30_dias': stats.get('vencendo_30_dias', 0),
            'vencidos': stats.get('vencidos', 0),
            'recentes': service.listar_todos_contratos(limite=5, offset=0)  # Últimos 5 contratos
        }

        return stats_realtime
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")
