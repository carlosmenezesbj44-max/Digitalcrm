"""Domínio para Contratos"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import enum


class StatusAssinatura(enum.Enum):
    AGUARDANDO = "aguardando"
    ASSINADO = "assinado"
    LIBERADO = "liberado"


class TipoContrato(enum.Enum):
    SERVICO = "servico"
    ASSINATURA = "assinatura"
    MANUTENCAO = "manutencao"
    SUPORTE = "suporte"
    OUTRO = "outro"


@dataclass
class Contrato:
    id: Optional[int]
    cliente_id: int
    titulo: str
    descricao: Optional[str] = None
    status_assinatura: StatusAssinatura = StatusAssinatura.AGUARDANDO
    tipo_contrato: TipoContrato = TipoContrato.SERVICO
    data_criacao: datetime = field(default_factory=datetime.utcnow)
    data_assinatura: Optional[datetime] = None
    arquivo_contrato: Optional[str] = None
    hash_assinatura: Optional[str] = None
    assinatura_digital: Optional[str] = None
    observacoes: Optional[str] = None

    def __post_init__(self):
        if not self.titulo:
            raise ValueError("Título é obrigatório")
        if not self.cliente_id:
            raise ValueError("Cliente ID é obrigatório")

    def assinar(self, hash_assinatura: str, assinatura_digital: Optional[str] = None):
        """Marca o contrato como assinado"""
        self.status_assinatura = StatusAssinatura.ASSINADO
        self.data_assinatura = datetime.utcnow()
        self.hash_assinatura = hash_assinatura
        if assinatura_digital:
            self.assinatura_digital = assinatura_digital

    def liberar(self):
        """Libera o contrato (assinatura verificada ou liberada manualmente)"""
        self.status_assinatura = StatusAssinatura.LIBERADO

    def aguardar_assinatura(self):
        """Define status para aguardando assinatura"""
        self.status_assinatura = StatusAssinatura.AGUARDANDO