from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class PermissaoResponse(BaseModel):
    id: int
    nome: str
    modulo: str
    descricao: Optional[str] = None
    
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nome_completo: str
    role: str = "cliente"
    foto_url: Optional[str] = None
    preferencias: Optional[Dict[str, Any]] = None

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8, max_length=50)

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome_completo: Optional[str] = None
    ativo: Optional[bool] = None
    foto_url: Optional[str] = None
    preferencias: Optional[Dict[str, Any]] = None

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime
    ultimo_acesso: Optional[datetime]
    permissoes: List[PermissaoResponse] = []
    grupos: List["GrupoResponse"] = []
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    username: str
    senha: str = Field(..., max_length=50)

class UsuarioPasswordUpdate(BaseModel):
    senha_atual: str = Field(..., max_length=50)
    nova_senha: str = Field(..., min_length=8, max_length=50)

class UsuarioPreferenciasUpdate(BaseModel):
    preferencias: Dict[str, Any]

class PermissaoCreate(BaseModel):
    nome: str
    modulo: str
    descricao: Optional[str] = None

class GrupoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class GrupoCreate(GrupoBase):
    permissoes_ids: List[int] = []

class GrupoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    permissoes_ids: Optional[List[int]] = None

class GrupoResponse(GrupoBase):
    id: int
    permissoes: List[PermissaoResponse] = []

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

class AuditoriaLogResponse(BaseModel):
    id: int
    usuario_id: int
    acao: str
    recurso: str
    timestamp: datetime


# Resolve forward references
UsuarioResponse.model_rebuild()
GrupoResponse.model_rebuild()
