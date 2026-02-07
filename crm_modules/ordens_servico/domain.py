from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class OrdemServico:
    id: Optional[int]
    cliente_id: int
    tipo_servico: str
    titulo: str
    descricao: str
    cliente_nome: Optional[str] = None
    status: str = "aberta"
    prioridade: str = "normal"
    data_criacao: datetime = field(default_factory=datetime.utcnow)
    data_agendamento: Optional[datetime] = None
    data_inicio: Optional[datetime] = None
    data_aguardando_peca: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None
    tecnico_responsavel: Optional[str] = None
    observacoes: Optional[str] = None
    valor: Optional[float] = None
    custo: Optional[float] = None
    endereco_servico: Optional[str] = None

    def __post_init__(self):
        if not self.cliente_id:
            raise ValueError("Cliente ID é obrigatório")
        if not self.titulo:
            raise ValueError("Título é obrigatório")
        if not self.descricao:
            raise ValueError("Descrição é obrigatória")
        if self.status not in ["aberta", "em_andamento", "aguardando_peca", "concluida", "cancelada"]:
            raise ValueError("Status inválido")
        if self.prioridade not in ["baixa", "normal", "alta", "urgente"]:
            raise ValueError("Prioridade inválida")

    def iniciar_servico(self, tecnico: str) -> None:
        """Inicia o serviço, mudando status para em_andamento"""
        self.status = "em_andamento"
        self.tecnico_responsavel = tecnico
        self.data_inicio = datetime.utcnow()

    def aguardando_peca(self, observacoes: Optional[str] = None) -> None:
        """Marca a OS como aguardando peça"""
        self.status = "aguardando_peca"
        self.data_aguardando_peca = datetime.utcnow()
        if observacoes:
            self.observacoes = (self.observacoes or "") + f"\nAguardando Peça: {observacoes}"

    def retomar_servico(self) -> None:
        """Retoma o serviço de Aguardando Peça para Em Andamento"""
        if self.status == "aguardando_peca":
            self.status = "em_andamento"

    def concluir_servico(self, observacoes_conclusao: Optional[str] = None) -> None:
        """Conclui o serviço"""
        self.status = "concluida"
        self.data_conclusao = datetime.utcnow()
        if observacoes_conclusao:
            self.observacoes = (self.observacoes or "") + f"\nConclusão: {observacoes_conclusao}"

    def cancelar_servico(self, motivo: str) -> None:
        """Cancela o serviço"""
        self.status = "cancelada"
        if motivo:
            self.observacoes = (self.observacoes or "") + f"\nCancelamento: {motivo}"


class OrdemServicoService:
    @staticmethod
    def validar_ordem(ordem: OrdemServico) -> bool:
        """Valida regras de negócio da ordem de serviço"""
        if len(ordem.titulo) < 3:
            return False
        if len(ordem.descricao) < 10:
            return False
        if ordem.valor and ordem.valor < 0:
            return False
        if ordem.custo and ordem.custo < 0:
            return False
        return True

    @staticmethod
    def calcular_lucro(ordem: OrdemServico) -> Optional[float]:
        """Calcula o lucro da ordem (valor - custo)"""
        if ordem.valor is not None and ordem.custo is not None:
            return ordem.valor - ordem.custo
        return None