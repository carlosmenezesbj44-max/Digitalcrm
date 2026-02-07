from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from crm_core.db.base import get_db
from crm_modules.usuarios.schemas import (
    UsuarioCreate,
    UsuarioLogin,
    UsuarioResponse,
    TokenResponse,
    UsuarioUpdate,
    UsuarioPasswordUpdate,
    UsuarioPreferenciasUpdate,
    PermissaoCreate,
    PermissaoResponse,
    GrupoCreate,
    GrupoUpdate,
    GrupoResponse,
)
from crm_modules.usuarios.models import Usuario
from crm_modules.usuarios.service import UsuarioService
from crm_core.security.dependencies import obter_usuario_atual, obter_usuario_admin

router = APIRouter(prefix="/api/v1/usuarios", tags=["usuarios"])

@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Registra novo usuário"""
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.criar_usuario(usuario_data)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(
    credenciais: UsuarioLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Autentica usuário"""
    try:
        service = UsuarioService(repository_session=db)
        ip_address = request.client.host
        resultado = service.autenticar(credenciais.username, credenciais.senha, ip_address)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UsuarioResponse)
def obter_perfil(usuario = Depends(obter_usuario_atual)):
    """Obtém dados do usuário autenticado"""
    return usuario

@router.put("/me/editar", response_model=UsuarioResponse)
def atualizar_meu_perfil(
    usuario_data: UsuarioUpdate,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Atualiza dados do usuário autenticado"""
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.atualizar_usuario(usuario_atual.id, usuario_data)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/me/senha", response_model=UsuarioResponse)
def atualizar_minha_senha(
    payload: UsuarioPasswordUpdate,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Atualiza senha do usuário autenticado"""
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.atualizar_senha(usuario_atual.id, payload.senha_atual, payload.nova_senha)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/me/foto")
async def atualizar_minha_foto(
    file: UploadFile = File(...),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Atualiza foto do usuário autenticado"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo inválido")

    content = await file.read()
    try:
        service = UsuarioService(repository_session=db)
        foto_url = service.upload_foto_usuario(usuario_atual.id, content, file.filename)
        return {"foto_url": foto_url}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me/preferencias")
def obter_minhas_preferencias(
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """ObtÃ©m preferÃªncias do usuÃ¡rio autenticado"""
    try:
        service = UsuarioService(repository_session=db)
        return {"preferencias": service.obter_preferencias(usuario_atual.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/me/preferencias")
def atualizar_minhas_preferencias(
    payload: UsuarioPreferenciasUpdate,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Atualiza preferÃªncias do usuÃ¡rio autenticado"""
    try:
        service = UsuarioService(repository_session=db)
        preferencias = service.atualizar_preferencias(usuario_atual.id, payload.preferencias)
        return {"preferencias": preferencias}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logout")
def logout(usuario = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    """Logout do usuário (apenas marca no client)"""
    return {"mensagem": "Logout realizado com sucesso"}

@router.get("/lista", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Lista todos os usuários (apenas para admin)"""
    if usuario_atual.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    
    service = UsuarioService(repository_session=db)
    usuarios = service.listar_usuarios(skip=skip, limit=limit)
    return usuarios

@router.get("/permissoes", response_model=List[PermissaoResponse])
def listar_permissoes(
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Lista todas as permiss?es (admin)'''
    service = UsuarioService(repository_session=db)
    return service.listar_permissoes()

@router.post("/permissoes", response_model=PermissaoResponse)
def criar_permissao(
    payload: PermissaoCreate,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Cria permiss?o (admin)'''
    service = UsuarioService(repository_session=db)
    return service.criar_permissao(payload.nome, payload.modulo, payload.descricao)

@router.get("/grupos", response_model=List[GrupoResponse])
def listar_grupos(
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Lista grupos (admin)'''
    service = UsuarioService(repository_session=db)
    return service.listar_grupos()

@router.post("/grupos", response_model=GrupoResponse)
def criar_grupo(
    payload: GrupoCreate,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Cria grupo (admin)'''
    try:
        service = UsuarioService(repository_session=db)
        return service.criar_grupo(payload.nome, payload.descricao, payload.permissoes_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/grupos/{grupo_id}", response_model=GrupoResponse)
def obter_grupo(
    grupo_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Obt?m grupo (admin)'''
    service = UsuarioService(repository_session=db)
    grupo = service.obter_grupo(grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo n?o encontrado")
    return grupo

@router.put("/grupos/{grupo_id}", response_model=GrupoResponse)
def atualizar_grupo(
    grupo_id: int,
    payload: GrupoUpdate,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Atualiza grupo (admin)'''
    try:
        service = UsuarioService(repository_session=db)
        return service.atualizar_grupo(grupo_id, payload.nome, payload.descricao, payload.permissoes_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/grupos/{grupo_id}")
def deletar_grupo(
    grupo_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Deleta grupo (admin)'''
    try:
        service = UsuarioService(repository_session=db)
        service.deletar_grupo(grupo_id)
        return {"message": "Grupo deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}/permissoes")
def definir_permissoes_usuario(
    usuario_id: int,
    payload: dict,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Define permiss?es diretas do usu?rio (admin)'''
    permissoes_ids = payload.get("permissoes_ids", [])
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.definir_permissoes_usuario(usuario_id, permissoes_ids)
        return {"success": True, "permissoes": [p.id for p in usuario.permissoes]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}/grupos")
def definir_grupos_usuario(
    usuario_id: int,
    payload: dict,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    '''Define grupos do usu?rio (admin)'''
    grupos_ids = payload.get("grupos_ids", [])
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.definir_grupos_usuario(usuario_id, grupos_ids)
        return {"success": True, "grupos": [g.id for g in usuario.grupos]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obter_usuario(
    usuario_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Obtém usuário por ID"""
    if usuario_atual.role != "admin" and usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    service = UsuarioService(repository_session=db)
    usuario = service.obter_usuario_por_id(usuario_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario

@router.put("/{usuario_id}/editar", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """Atualiza usuário"""
    if usuario_atual.role != "admin" and usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.atualizar_usuario(usuario_id, usuario_data)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}")
def deletar_usuario(
    usuario_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    """Deleta usuário (apenas admin)"""
    if usuario_id == usuario_atual.id:
        raise HTTPException(status_code=400, detail="Não é possível deletar o próprio usuário")

    try:
        service = UsuarioService(repository_session=db)
        service.deletar_usuario(usuario_id)
        return {"mensagem": "Usuário deletado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar usuário: {str(e)}")

@router.post("/{usuario_id}/alternar-status")
def alternar_status_usuario(
    usuario_id: int,
    usuario_atual: Usuario = Depends(obter_usuario_admin),
    db: Session = Depends(get_db)
):
    """Alterna status ativo/inativo do usu?rio (apenas admin)"""
    if usuario_id == usuario_atual.id:
        raise HTTPException(status_code=400, detail="N?o ? poss?vel desativar o pr?prio usu?rio")

    service = UsuarioService(repository_session=db)
    usuario = service.obter_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usu?rio n?o encontrado")

    novo_status = not usuario.ativo
    atualizado = service.atualizar_usuario(usuario_id, UsuarioUpdate(ativo=novo_status))
    return {"success": True, "ativo": atualizado.ativo}
