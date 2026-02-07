from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional


class ServidorBase(BaseModel):
    nome: str
    ip: str
    tipo_conexao: str  # mikrotik, accel-ppp, huawei, cisco
    tipo_acesso: str  # ssh, telnet
    usuario: str
    senha: str
    alterar_nome: bool = True
    ativo: bool = True


class ServidorCreate(ServidorBase):
    pass


class ServidorUpdate(BaseModel):
    nome: Optional[str] = None
    ip: Optional[str] = None
    tipo_conexao: Optional[str] = None
    tipo_acesso: Optional[str] = None
    usuario: Optional[str] = None
    senha: Optional[str] = None
    alterar_nome: Optional[bool] = None
    ativo: Optional[bool] = None


class Servidor(ServidorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)