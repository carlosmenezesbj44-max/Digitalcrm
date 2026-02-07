from typing import Optional
from crm_modules.bloqueios.repository import PlanoBloqueioRepository
from crm_modules.bloqueios.domain import PlanoBloqueio
from crm_modules.bloqueios.schemas import PlanoBloqueioCreate, PlanoBloqueioUpdate
from crm_modules.bloqueios.models import PlanoBloqueioModel
from crm_core.utils.exceptions import NotFoundException, ValidationException


class PlanoBloqueioService:
    def __init__(self, repository: Optional[PlanoBloqueioRepository] = None, repository_session=None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = PlanoBloqueioRepository(session=repository_session) if repository_session is not None else PlanoBloqueioRepository()

    def criar_plano_bloqueio(self, plano_data: PlanoBloqueioCreate) -> PlanoBloqueio:
        # Validate
        if not plano_data.nome or not plano_data.ip_privado or plano_data.dias_bloqueio < 0:
            raise ValidationException("Nome, IP privado e dias de bloqueio são obrigatórios")

        # Create ORM model instance and persist
        model = PlanoBloqueioModel(
            nome=plano_data.nome,
            ip_privado=plano_data.ip_privado,
            reduzir_velocidade=plano_data.reduzir_velocidade,
            dias_bloqueio=plano_data.dias_bloqueio,
            tipo_bloqueio=plano_data.tipo_bloqueio,
            ativo=plano_data.ativo,
        )

        model = self.repository.create(model)

        # Create domain object to return
        plano = PlanoBloqueio(
            id=model.id,
            nome=model.nome,
            ip_privado=model.ip_privado,
            reduzir_velocidade=model.reduzir_velocidade,
            dias_bloqueio=model.dias_bloqueio,
            tipo_bloqueio=model.tipo_bloqueio,
            ativo=model.ativo,
        )

        return plano

    def obter_plano_bloqueio(self, plano_id: int) -> PlanoBloqueio:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano de bloqueio não encontrado")
        return PlanoBloqueio(
            id=model.id,
            nome=model.nome,
            ip_privado=model.ip_privado,
            reduzir_velocidade=model.reduzir_velocidade,
            dias_bloqueio=model.dias_bloqueio,
            tipo_bloqueio=model.tipo_bloqueio,
            ativo=model.ativo,
        )

    def atualizar_plano_bloqueio(self, plano_id: int, update_data: PlanoBloqueioUpdate) -> PlanoBloqueio:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano de bloqueio não encontrado")

        # Update fields
        if update_data.nome:
            model.nome = update_data.nome
        if update_data.ip_privado:
            model.ip_privado = update_data.ip_privado
        if update_data.reduzir_velocidade is not None:
            model.reduzir_velocidade = update_data.reduzir_velocidade
        if update_data.dias_bloqueio is not None:
            model.dias_bloqueio = update_data.dias_bloqueio
        if update_data.tipo_bloqueio:
            model.tipo_bloqueio = update_data.tipo_bloqueio
        if update_data.ativo is not None:
            model.ativo = update_data.ativo

        self.repository.update(model)

        return self.obter_plano_bloqueio(plano_id)

    def desativar_plano_bloqueio(self, plano_id: int) -> PlanoBloqueio:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano de bloqueio não encontrado")
        model.ativo = False
        self.repository.update(model)
        return self.obter_plano_bloqueio(plano_id)

    def listar_planos_bloqueio_ativos(self):
        models = self.repository.get_active_planos_bloqueio()
        return [self.obter_plano_bloqueio(int(model.id)) for model in models]