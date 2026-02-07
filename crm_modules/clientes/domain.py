from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, date


@dataclass
class Cliente:
    id: Optional[int]
    nome: str
    email: str
    telefone: str
    cpf: str
    endereco: str
    tipo_cliente: str = "fisico"
    data_cadastro: datetime = field(default_factory=datetime.now)
    ativo: bool = True
    nacionalidade: Optional[str] = None
    rg: Optional[str] = None
    orgao_emissor: Optional[str] = None
    naturalidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    username: Optional[str] = None
    observacoes: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    estado: Optional[str] = None
    apartamento: Optional[str] = None
    complemento: Optional[str] = None
    moradia: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    whatsapp: Optional[str] = None
    telefone_residencial: Optional[str] = None
    telefone_comercial: Optional[str] = None
    telefone_celular: Optional[str] = None
    instagram: Optional[str] = None
    servidor_id: Optional[int] = None
    plano_id: Optional[int] = None
    profile: Optional[str] = None
    tipo_servico: str = "pppoe"
    comentario_login: Optional[str] = None
    status_contrato: str = "nenhum"
    foto_casa: Optional[str] = None
    valor_mensal: Optional[float] = None
    dia_vencimento: Optional[int] = None
    valor_total: Optional[float] = None
    arquivos: list = field(default_factory=list)
    produto_ids: list = field(default_factory=list)

    def __post_init__(self):
        self.nome = self.nome or "Nome não informado"
        self.email = self.email or "email@nao.informado"
        # Add more validations


class ClienteService:
    @staticmethod
    def validar_cliente(cliente: Cliente) -> bool:
        # Business rules
        if len(cliente.nome) < 2:
            return False
        if '@' not in cliente.email:
            return False
        return True

    @staticmethod
    def desativar_cliente(cliente: Cliente) -> Cliente:
        cliente.ativo = False
        return cliente
