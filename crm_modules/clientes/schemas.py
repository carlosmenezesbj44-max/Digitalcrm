from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional, List
from datetime import datetime, date


class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: str
    cpf: str
    endereco: str
    cidade: Optional[str] = None
    rua: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    condominio: Optional[str] = None
    bloco: Optional[str] = None
    estado: Optional[str] = None
    tipo_localidade: Optional[str] = None
    numero: Optional[str] = None
    apartamento: Optional[str] = None
    complemento: Optional[str] = None
    moradia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    tipo_cliente: str = "fisico"
    nacionalidade: Optional[str] = None
    rg: Optional[str] = None
    orgao_emissor: Optional[str] = None
    naturalidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    username: Optional[str] = None
    observacoes: Optional[str] = None
    plano_id: Optional[int] = None
    velocidade: Optional[int] = None
    data_instalacao: Optional[date] = None
    status_servico: str = "ativo"
    valor_mensal: Optional[float] = None
    dia_vencimento: Optional[int] = None
    whatsapp: Optional[str] = None
    telefone_residencial: Optional[str] = None
    telefone_comercial: Optional[str] = None
    telefone_celular: Optional[str] = None
    instagram: Optional[str] = None
    servidor_id: Optional[int] = None
    profile: Optional[str] = None
    tipo_servico: str = "pppoe"
    comentario_login: Optional[str] = None

    # Serviços adicionais
    servico_instalacao_equipamentos: bool = False
    servico_suporte_premium: bool = False
    servico_treinamentos: bool = False
    servico_cortesia: bool = False
    servico_wifi_publico: bool = False
    servico_apps_parceiros: bool = False
    servico_campanhas: bool = False
    servico_personalizados: bool = False
    servico_monitoramento: bool = False
    servico_hospedagem: bool = False
    servico_integracao: bool = False
    servico_vas: bool = False
    servico_streaming: bool = False
    servico_backup: bool = False
    servico_colaboracao: bool = False

    # Histórico de serviços
    historico_chamados: bool = False
    historico_instalacoes: bool = False
    historico_upgrades: bool = False

    # Status do cliente
    status_cliente: str = "conectado"
    foto_casa: Optional[str] = None

    # Plano de bloqueio aplicado (opcional)
    plano_bloqueio_id: Optional[int] = None

    # Produtos vinculados
    produto_ids: Optional[List[int]] = []
    valor_total: Optional[float] = None


class ClienteCreate(ClienteBase):
    ativo: bool = True
    password: Optional[str] = Field(None, max_length=50)


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None
    nacionalidade: Optional[str] = None
    rg: Optional[str] = None
    orgao_emissor: Optional[str] = None
    naturalidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    username: Optional[str] = None
    observacoes: Optional[str] = None
    numero: Optional[str] = None
    apartamento: Optional[str] = None
    complemento: Optional[str] = None
    moradia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status_cliente: Optional[str] = None
    plano_bloqueio_id: Optional[int] = None
    foto_casa: Optional[str] = None
    produto_ids: Optional[List[int]] = None
    valor_total: Optional[float] = None


class Cliente(ClienteBase):
    id: int
    data_cadastro: datetime
    ativo: bool
    nacionalidade: Optional[str] = None
    rg: Optional[str] = None
    orgao_emissor: Optional[str] = None
    naturalidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    username: Optional[str] = None
    observacoes: Optional[str] = None
    numero: Optional[str] = None
    apartamento: Optional[str] = None
    complemento: Optional[str] = None
    moradia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status_cliente: str
    plano_bloqueio_id: Optional[int] = None
    foto_casa: Optional[str] = None
    arquivos: List["ClienteArquivo"] = []

    model_config = ConfigDict(from_attributes=True)


class ClienteArquivoBase(BaseModel):
    filename: str
    filepath: str
    cliente_id: int


class ClienteArquivoCreate(ClienteArquivoBase):
    pass


class ClienteArquivo(ClienteArquivoBase):
    id: int
    data_upload: datetime

    model_config = ConfigDict(from_attributes=True)
