from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from crm_core.db.base import get_db
from crm_core.security.auth_utils import decodificar_token
from crm_core.security.acl import ACL
from crm_modules.usuarios.models import Usuario
from typing import Optional

security = HTTPBearer()
acl = ACL()

async def obter_usuario_atual(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Usuario:
    """Extrai o usuário atual do token JWT"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais não fornecidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decodificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario_id = payload.get("usuario_id")
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo",
        )
    
    return usuario

def obter_usuario_admin(usuario: Usuario = Depends(obter_usuario_atual)) -> Usuario:
    """Verifica se o usuário é administrador"""
    if usuario.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return usuario

def verificar_permissao(permissao_necessaria: str, recurso: Optional[str] = None):
    """Dependência para verificar permissão específica do usuário"""
    async def verificador(usuario: Usuario = Depends(obter_usuario_atual)):
        if not acl.has_permission(usuario.id, permissao_necessaria, recurso):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Permissão necessária: {permissao_necessaria}",
            )
        return usuario
    return verificador

def verificar_acesso_recurso(acao: str, recurso: str):
    """Dependência para verificar acesso a recurso específico"""
    async def verificador(usuario: Usuario = Depends(obter_usuario_atual)):
        if not acl.check_resource_access(usuario.id, acao, recurso):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Ação: {acao} em {recurso}",
            )
        return usuario
    return verificador

def verificar_role(role_necessario: str):
    """Dependência para verificar role do usuário"""
    async def verificador(usuario: Usuario = Depends(obter_usuario_atual)):
        if usuario.role != role_necessario and usuario.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Role necessário: {role_necessario}",
            )
        return usuario
    return verificador
