#!/usr/bin/env python3
"""
API REST para integração com MikroTik
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from pydantic import BaseModel

from crm_modules.mikrotik.services import MikrotikService
from crm_core.middleware.auth_middleware import AuthMiddleware
from crm_core.db.models import Usuario as User

router = APIRouter(prefix="/mikrotik", tags=["MikroTik"])


@router.get("/servers")
async def get_servers():
    """Obtém lista de servidores MikroTik"""
    from crm_core.db.base import get_db_session
    from crm_modules.servidores.repository import ServidorRepository
    
    db = get_db_session()
    try:
        repo = ServidorRepository(db)
        # Usar listar_servidores_ativos() ao invés de listar_todos()
        servidores = repo.listar_servidores_ativos()
        mikrotik_servers = [
            {
                'id': s.id,
                'nome': s.nome,
                'ip': s.ip,
                'tipo_conexao': s.tipo_conexao,
                'ativo': s.ativo
            }
            for s in servidores if s.tipo_conexao and s.tipo_conexao.lower() == 'mikrotik'
        ]
        return {'servidores': mikrotik_servers}
    finally:
        db.close()


class ProfileCreate(BaseModel):
    name: str
    download_limit: int
    upload_limit: int


class ClientSync(BaseModel):
    cliente_id: int
    contrato_id: int


class ClientBlock(BaseModel):
    username: str


class ClientUnblock(BaseModel):
    username: str


class CredentialUpdate(BaseModel):
    username: str
    new_password: str
    new_profile: str = None


class ServerParams(BaseModel):
    servidor_id: int = None


@router.get("/status")
async def get_mikrotik_status(servidor_id: int = None):
    """Obtém o status e configurações do MikroTik"""
    service = MikrotikService(servidor_id=servidor_id)
    result = service.obter_configuracoes()
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.post("/profiles")
async def create_profile(
    profile: ProfileCreate
):
    """Cria um profile PPPoE no MikroTik"""
    service = MikrotikService()
    result = service.criar_profile_real_time(
        name=profile.name,
        download_limit=profile.download_limit,
        upload_limit=profile.upload_limit
    )
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.post("/clients/sync")
async def sync_client(
    client_data: ClientSync
):
    """Sincroniza um cliente com o MikroTik"""
    # Importar aqui para evitar import circular
    from crm_modules.clientes.repository import ClienteRepository
    from crm_modules.contratos.repository import ContratoRepository
    from crm_core.db.base import get_db_session
    
    db = get_db_session()
    try:
        cliente_repo = ClienteRepository(db)
        contrato_repo = ContratoRepository(db)
        
        cliente = cliente_repo.get_by_id(client_data.cliente_id)
        contrato = contrato_repo.get_by_id(client_data.contrato_id)
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        service = MikrotikService()
        result = service.sincronizar_cliente_real_time(cliente, contrato)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        return result
        
    finally:
        db.close()


@router.post("/clients/block")
async def block_client(
    block_data: ClientBlock
):
    """Bloqueia um cliente no MikroTik"""
    service = MikrotikService()
    result = service.bloquear_cliente_real_time(block_data.username)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.post("/clients/unblock")
async def unblock_client(
    unblock_data: ClientUnblock
):
    """Desbloqueia um cliente no MikroTik"""
    service = MikrotikService()
    result = service.desbloquear_cliente_real_time(unblock_data.username)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.put("/clients/credentials")
async def update_client_credentials(
    credential_data: CredentialUpdate
):
    """Atualiza as credenciais de um cliente no MikroTik"""
    service = MikrotikService()
    result = service.atualizar_credential_cliente(
        username=credential_data.username,
        new_password=credential_data.new_password,
        new_profile=credential_data.new_profile
    )
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.get("/sessions")
async def get_active_sessions(servidor_id: int = None):
    """Obtém as sessões PPPoE ativas"""
    service = MikrotikService(servidor_id=servidor_id)
    result = service.obter_sessoes_ativas()
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.post("/sessions/{session_id}/disconnect")
async def disconnect_session(session_id: str, servidor_id: int = None):
    """Desconecta uma sessão ativa"""
    service = MikrotikService(servidor_id=servidor_id)
    result = service.desconectar_sessao(session_id)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.get("/logs")
async def get_logs(
    servidor_id: int = None,
    limit: int = 50
):
    """Obtém logs recentes do MikroTik"""
    service = MikrotikService(servidor_id=servidor_id)
    result = service.obter_logs_recentes(limit=limit)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


@router.get("/profiles")
async def get_profiles():
    """Obtém todos os profiles PPPoE"""
    service = MikrotikService()
    result = service.obter_configuracoes()
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return {"profiles": result['profiles']}


@router.get("/secrets")
async def get_secrets():
    """Obtém todos os secrets PPPoE"""
    service = MikrotikService()
    result = service.obter_configuracoes()
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return {"secrets": result['secrets']}


@router.post("/sync-plans")
async def sync_plans(servidor_id: int = None):
    """Sincroniza todos os planos do CRM com profiles PPPoE no MikroTik"""
    service = MikrotikService(servidor_id=servidor_id)
    result = service.sincronizar_planos()
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['message'])
    
    return result


# Integração com o módulo de contratos
@router.post("/contratos/{contrato_id}/sync")
async def sync_contract_with_mikrotik(
    contrato_id: int
):
    """Sincroniza um contrato com o MikroTik"""
    from crm_modules.contratos.repository import ContratoRepository
    from crm_modules.mikrotik.services import sincronizar_contrato_com_mikrotik
    from crm_core.db.base import get_db_session
    
    db = get_db_session()
    try:
        contrato_repo = ContratoRepository(db)
        contrato = contrato_repo.get_by_id(contrato_id)
        
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        result = sincronizar_contrato_com_mikrotik(contrato)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        return result
        
    finally:
        db.close()


@router.post("/contratos/{contrato_id}/block")
async def block_contract_on_mikrotik(
    contrato_id: int
):
    """Bloqueia um contrato no MikroTik"""
    from crm_modules.contratos.repository import ContratoRepository
    from crm_modules.mikrotik.services import bloquear_contrato_no_mikrotik
    from crm_core.db.base import get_db_session
    
    db = get_db_session()
    try:
        contrato_repo = ContratoRepository(db)
        contrato = contrato_repo.get_by_id(contrato_id)
        
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        result = bloquear_contrato_no_mikrotik(contrato)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        return result
        
    finally:
        db.close()


@router.post("/contratos/{contrato_id}/unblock")
async def unblock_contract_on_mikrotik(
    contrato_id: int
):
    """Desbloqueia um contrato no MikroTik"""
    from crm_modules.contratos.repository import ContratoRepository
    from crm_modules.mikrotik.services import desbloquear_contrato_no_mikrotik
    from crm_core.db.base import get_db_session
    
    db = get_db_session()
    try:
        contrato_repo = ContratoRepository(db)
        contrato = contrato_repo.get_by_id(contrato_id)
        
        if not contrato:
            raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
        result = desbloquear_contrato_no_mikrotik(contrato)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        return result
        
    finally:
        db.close()