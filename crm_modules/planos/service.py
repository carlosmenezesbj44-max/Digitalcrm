from typing import Optional
from crm_modules.planos.repository import PlanoRepository
from crm_modules.planos.domain import Plano
from crm_modules.planos.schemas import PlanoCreate, PlanoUpdate
from crm_modules.planos.models import PlanoModel
from crm_core.utils.exceptions import NotFoundException, ValidationException


class PlanoService:
    def __init__(self, repository: Optional[PlanoRepository] = None, repository_session=None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = PlanoRepository(session=repository_session) if repository_session is not None else PlanoRepository()

    def criar_plano(self, plano_data: PlanoCreate) -> Plano:
        # Validate
        if not plano_data.nome or plano_data.velocidade_download <= 0 or plano_data.velocidade_upload <= 0 or plano_data.valor_mensal < 0:
            raise ValidationException("Nome, velocidades (>0) e valor mensal (>=0) são obrigatórios")

        # Create ORM model instance and persist
        model = PlanoModel(
            nome=plano_data.nome,
            velocidade_download=plano_data.velocidade_download,
            velocidade_upload=plano_data.velocidade_upload,
            valor_mensal=plano_data.valor_mensal,
            descricao=plano_data.descricao,
            ativo=plano_data.ativo,
        )

        model = self.repository.create(model)

        # Create domain object to return
        plano = Plano(
            id=model.id,
            nome=model.nome,
            velocidade_download=model.velocidade_download,
            velocidade_upload=model.velocidade_upload,
            valor_mensal=model.valor_mensal,
            descricao=model.descricao,
            ativo=model.ativo,
        )

        return plano

    def obter_plano(self, plano_id: int) -> Plano:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano não encontrado")
        return self._to_domain(model)

    def _to_domain(self, model: PlanoModel) -> Plano:
        return Plano(
            id=model.id,
            nome=model.nome,
            velocidade_download=model.velocidade_download,
            velocidade_upload=model.velocidade_upload,
            valor_mensal=model.valor_mensal,
            descricao=model.descricao,
            ativo=model.ativo,
        )

    def atualizar_plano(self, plano_id: int, update_data: PlanoUpdate) -> Plano:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano não encontrado")

        # Update fields
        if update_data.nome:
            model.nome = update_data.nome
        if update_data.velocidade_download is not None:
            model.velocidade_download = update_data.velocidade_download
        if update_data.velocidade_upload is not None:
            model.velocidade_upload = update_data.velocidade_upload
        if update_data.valor_mensal is not None:
            model.valor_mensal = update_data.valor_mensal
        if update_data.descricao is not None:
            model.descricao = update_data.descricao
        if update_data.ativo is not None:
            model.ativo = update_data.ativo

        self.repository.update(model)

        return self._to_domain(model)

    def desativar_plano(self, plano_id: int) -> Plano:
        model = self.repository.get_by_id(plano_id)
        if not model:
            raise NotFoundException("Plano não encontrado")
        model.ativo = False
        self.repository.update(model)
        return self._to_domain(model)

    def listar_planos_ativos(self):
        models = self.repository.get_active_planos()
        return [self._to_domain(model) for model in models]

    def buscar_planos_por_nome(self, nome: str):
        """Busca planos por nome"""
        models = self.repository.search_by_name(nome)
        return [self._to_domain(model) for model in models]