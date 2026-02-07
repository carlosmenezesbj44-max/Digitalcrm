from crm_modules.ordens_servico.repository import OrdemServicoRepository
from crm_modules.ordens_servico.domain import OrdemServico
from crm_modules.ordens_servico.schemas import OrdemServicoCreate, OrdemServicoUpdate
from crm_modules.ordens_servico.models import OrdemServicoModel
from crm_core.utils.exceptions import NotFoundException, ValidationException
from crm_core.events.bus import EventBus
from crm_core.events.events import OrdemServicoCreatedEvent
from datetime import datetime


class OrdemServicoService:
    def __init__(self, repository: OrdemServicoRepository = None, repository_session=None, event_bus: EventBus = None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = OrdemServicoRepository(session=repository_session) if repository_session is not None else OrdemServicoRepository()
        self.event_bus = event_bus or EventBus()

    def criar_ordem_servico(self, ordem_data: OrdemServicoCreate) -> OrdemServico:
        # Validate
        if not ordem_data.cliente_id or not ordem_data.titulo or not ordem_data.descricao:
            raise ValidationException("Cliente ID, título e descrição são obrigatórios")

        # Create ORM model instance and persist
        model = OrdemServicoModel(
            cliente_id=ordem_data.cliente_id,
            tipo_servico=ordem_data.tipo_servico,
            titulo=ordem_data.titulo,
            descricao=ordem_data.descricao,
            prioridade=ordem_data.prioridade,
            data_agendamento=getattr(ordem_data, 'data_agendamento', None),
            tecnico_responsavel=getattr(ordem_data, 'tecnico_responsavel', None),
            observacoes=getattr(ordem_data, 'observacoes', None),
            valor_servico=getattr(ordem_data, 'valor', None),
            custo_empresa=getattr(ordem_data, 'custo', None),
            endereco_atendimento=getattr(ordem_data, 'endereco_servico', None),
        )

        model = self.repository.create(model)

        # Create domain object to return
        ordem = OrdemServico(
            id=model.id,
            cliente_id=model.cliente_id,
            tipo_servico=model.tipo_servico,
            titulo=model.titulo,
            descricao=model.descricao,
            status=model.status,
            prioridade=model.prioridade,
            data_criacao=model.data_criacao,
            data_agendamento=model.data_agendamento,
            data_inicio=model.data_inicio,
            data_aguardando_peca=model.data_aguardando_peca,
            data_conclusao=model.data_conclusao,
            tecnico_responsavel=model.tecnico_responsavel,
            observacoes=model.observacoes,
            valor=model.valor_servico,
            custo=model.custo_empresa,
            endereco_servico=model.endereco_atendimento,
        )

        # Publish event
        self.event_bus.publish(OrdemServicoCreatedEvent(ordem.id, ordem.cliente_id))

        return ordem

    def obter_ordem_servico(self, ordem_id: int) -> OrdemServico:
        model = self.repository.get_by_id(ordem_id)
        if not model:
            raise NotFoundException("Ordem de serviço não encontrada")
        
        # Buscar nome do cliente
        cliente_nome = None
        try:
            from crm_modules.clientes.models import ClienteModel
            cliente = self.repository.session.query(ClienteModel).filter(ClienteModel.id == model.cliente_id).first()
            if cliente:
                cliente_nome = cliente.nome or f"Cliente {model.cliente_id}"
        except Exception:
            cliente_nome = f"Cliente {model.cliente_id}"
        
        return OrdemServico(
            id=model.id,
            cliente_id=model.cliente_id,
            cliente_nome=cliente_nome,
            tipo_servico=model.tipo_servico,
            titulo=model.titulo,
            descricao=model.descricao,
            status=model.status,
            prioridade=model.prioridade,
            data_criacao=model.data_criacao,
            data_agendamento=model.data_agendamento,
            data_inicio=model.data_inicio,
            data_aguardando_peca=model.data_aguardando_peca,
            data_conclusao=model.data_conclusao,
            tecnico_responsavel=model.tecnico_responsavel,
            observacoes=model.observacoes,
            valor=model.valor_servico,
            custo=model.custo_empresa,
            endereco_servico=model.endereco_atendimento,
        )

    def atualizar_ordem_servico(self, ordem_id: int, update_data: OrdemServicoUpdate) -> OrdemServico:
        model = self.repository.get_by_id(ordem_id)
        if not model:
            raise NotFoundException("Ordem de serviço não encontrada")

        # Update fields
        if update_data.tipo_servico:
            model.tipo_servico = update_data.tipo_servico
        if update_data.titulo:
            model.titulo = update_data.titulo
        if update_data.descricao:
            model.descricao = update_data.descricao
        if update_data.status:
            model.status = update_data.status
            if update_data.status == "concluida":
                model.data_conclusao = datetime.utcnow()
        if update_data.prioridade:
            model.prioridade = update_data.prioridade
        if update_data.data_agendamento is not None:
            model.data_agendamento = update_data.data_agendamento
        if update_data.data_conclusao is not None:
            model.data_conclusao = update_data.data_conclusao
        if update_data.tecnico_responsavel:
            model.tecnico_responsavel = update_data.tecnico_responsavel
        if update_data.observacoes:
            model.observacoes = update_data.observacoes
        if update_data.valor is not None:
            model.valor_servico = update_data.valor
        if update_data.custo is not None:
            model.custo_empresa = update_data.custo
        if update_data.endereco_servico:
            model.endereco_atendimento = update_data.endereco_servico

        self.repository.update(model)

        return self.obter_ordem_servico(ordem_id)

    def iniciar_ordem_servico(self, ordem_id: int, tecnico: str) -> OrdemServico:
        ordem = self.obter_ordem_servico(ordem_id)
        ordem.iniciar_servico(tecnico)
        model = self.repository.get_by_id(ordem_id)
        model.status = ordem.status
        model.data_inicio = ordem.data_inicio
        model.tecnico_responsavel = ordem.tecnico_responsavel
        self.repository.update(model)
        return ordem

    def aguardando_peca_ordem_servico(self, ordem_id: int, observacoes: str = None) -> OrdemServico:
        """Marca a OS como aguardando peça"""
        ordem = self.obter_ordem_servico(ordem_id)
        ordem.aguardando_peca(observacoes)
        model = self.repository.get_by_id(ordem_id)
        model.status = ordem.status
        model.data_aguardando_peca = ordem.data_aguardando_peca
        model.observacoes = ordem.observacoes
        self.repository.update(model)
        return ordem

    def retomar_ordem_servico(self, ordem_id: int) -> OrdemServico:
        """Retoma a OS de Aguardando Peça para Em Andamento"""
        ordem = self.obter_ordem_servico(ordem_id)
        ordem.retomar_servico()
        model = self.repository.get_by_id(ordem_id)
        model.status = ordem.status
        self.repository.update(model)
        return ordem

    def concluir_ordem_servico(self, ordem_id: int, observacoes_conclusao: str = None) -> OrdemServico:
        ordem = self.obter_ordem_servico(ordem_id)
        ordem.concluir_servico(observacoes_conclusao)
        model = self.repository.get_by_id(ordem_id)
        model.status = ordem.status
        model.data_conclusao = ordem.data_conclusao
        model.observacoes = ordem.observacoes
        self.repository.update(model)
        return ordem

    def cancelar_ordem_servico(self, ordem_id: int, motivo: str) -> OrdemServico:
        ordem = self.obter_ordem_servico(ordem_id)
        ordem.cancelar_servico(motivo)
        model = self.repository.get_by_id(ordem_id)
        model.status = ordem.status
        model.observacoes = ordem.observacoes
        self.repository.update(model)
        return ordem

    def listar_ordens_por_cliente(self, cliente_id: int):
        models = self.repository.get_by_cliente_id(cliente_id)
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_por_status(self, status: str):
        models = self.repository.get_by_status(status)
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_abertas(self):
        models = self.repository.get_abertas()
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_em_andamento(self):
        models = self.repository.get_em_andamento()
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_aguardando_peca(self):
        models = self.repository.get_by_status("aguardando_peca")
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_concluidas(self):
        models = self.repository.get_concluidas()
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_todas_ordens(self):
        models = self.repository.session.query(OrdemServicoModel).all()
        return [self.obter_ordem_servico(m.id) for m in models]

    def listar_ordens_servico(self):
        """Alias para listar_todas_ordens()"""
        return self.listar_todas_ordens()

    def obter_estatisticas(self):
        return self.repository.get_stats()

    def listar_ordens_com_filtros(
        self,
        status: str | None = None,
        tipo_servico: str | None = None,
        cliente_id: int | None = None,
        tecnico: str | None = None,
        prioridade: str | None = None,
        endereco: str | None = None,
        search: str | None = None,
        data_inicio: str | None = None,
        data_fim: str | None = None,
        sort_by: str | None = "data_criacao",
        sort_order: str | None = "desc",
        page: int = 1,
        per_page: int = 10
    ):
        models, total = self.repository.get_ordens_com_filtros(
            status=status,
            tipo_servico=tipo_servico,
            cliente_id=cliente_id,
            tecnico=tecnico,
            prioridade=prioridade,
            endereco=endereco,
            search=search,
            data_inicio=data_inicio,
            data_fim=data_fim,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            per_page=per_page,
        )
        ordens = [self.obter_ordem_servico(m.id) for m in models]
        try:
            from crm_modules.clientes.models import ClienteModel
            # Mapear nomes de clientes
            cliente_ids = list({m.cliente_id for m in models})
            if cliente_ids:
                rows = (
                    self.repository.session.query(ClienteModel.id, ClienteModel.nome)
                    .filter(ClienteModel.id.in_(cliente_ids))
                    .all()
                )
                nome_por_id = {row[0]: row[1] for row in rows}
                for ordem in ordens:
                    setattr(ordem, "cliente_nome", nome_por_id.get(ordem.cliente_id, str(ordem.cliente_id)))
        except Exception:
            # Em caso de falha, mantém cliente_id
            pass
        return {
            "ordens": ordens,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        }
