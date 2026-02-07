from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class TecnicoCreate(BaseModel):
    # Básicas
    nome: str
    email: str
    telefone: str
    telefone_secundario: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    
    # Foto
    foto_url: Optional[str] = None
    
    # Endereço
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None
    
    # Profissional
    especialidades: Optional[str] = None
    crea: Optional[str] = None
    formacao: Optional[str] = None
    experiencia_anos: Optional[int] = None
    
    # Financeiro
    salario_taxa: Optional[float] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    tipo_conta: Optional[str] = None
    
    # Emprego
    data_admissao: Optional[datetime] = None
    data_demissao: Optional[datetime] = None
    cargo: Optional[str] = None
    
    # Status
    status: str = "ativo"
    ativo: bool = True
    observacoes: Optional[str] = None


class TecnicoUpdate(BaseModel):
    # Básicas
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    telefone_secundario: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    
    # Foto
    foto_url: Optional[str] = None
    
    # Endereço
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None
    
    # Profissional
    especialidades: Optional[str] = None
    crea: Optional[str] = None
    formacao: Optional[str] = None
    experiencia_anos: Optional[int] = None
    
    # Financeiro
    salario_taxa: Optional[float] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    tipo_conta: Optional[str] = None
    
    # Emprego
    data_admissao: Optional[datetime] = None
    data_demissao: Optional[datetime] = None
    cargo: Optional[str] = None
    
    # Status
    status: Optional[str] = None
    ativo: Optional[bool] = None
    observacoes: Optional[str] = None


class TecnicoResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    telefone_secundario: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    foto_url: Optional[str] = None
    endereco_rua: Optional[str] = None
    endereco_numero: Optional[str] = None
    endereco_complemento: Optional[str] = None
    endereco_bairro: Optional[str] = None
    endereco_cidade: Optional[str] = None
    endereco_estado: Optional[str] = None
    endereco_cep: Optional[str] = None
    especialidades: Optional[str] = None
    crea: Optional[str] = None
    formacao: Optional[str] = None
    experiencia_anos: Optional[int] = None
    salario_taxa: Optional[float] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    tipo_conta: Optional[str] = None
    data_admissao: Optional[datetime] = None
    data_demissao: Optional[datetime] = None
    cargo: Optional[str] = None
    status: str
    ativo: bool
    observacoes: Optional[str] = None
    data_cadastro: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True
