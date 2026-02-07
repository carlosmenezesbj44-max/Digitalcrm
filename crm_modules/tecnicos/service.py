from crm_modules.tecnicos.repository import TecnicoRepository
from crm_modules.tecnicos.schemas import TecnicoCreate, TecnicoUpdate
from crm_modules.tecnicos.models import TecnicoModel


class TecnicoService:
    def __init__(self, repository_session=None):
        self.repository = TecnicoRepository(repository_session)

    def listar_tecnicos(self):
        return self.repository.listar_ativos()

    def listar_todos(self):
        return self.repository.get_all()

    def obter_tecnico(self, tecnico_id: int):
        return self.repository.get_by_id(tecnico_id)

    def criar_tecnico(self, tecnico_create: TecnicoCreate) -> TecnicoModel:
        # Verificar se email já existe
        existente = self.repository.obter_por_email(tecnico_create.email)
        if existente:
            raise ValueError(f"Email {tecnico_create.email} já cadastrado")

        tecnico = TecnicoModel(**tecnico_create.dict())
        return self.repository.create(tecnico)

    def atualizar_tecnico(self, tecnico_id: int, tecnico_update: TecnicoUpdate) -> TecnicoModel:
        tecnico = self.repository.get_by_id(tecnico_id)
        if not tecnico:
            raise ValueError(f"Técnico {tecnico_id} não encontrado")

        update_data = tecnico_update.dict(exclude_unset=True)

        # Verificar se novo email já existe (se estiver sendo atualizado)
        if 'email' in update_data and update_data['email'] != tecnico.email:
            existente = self.repository.obter_por_email(update_data['email'])
            if existente:
                raise ValueError(f"Email {update_data['email']} já cadastrado")

        for field, value in update_data.items():
            setattr(tecnico, field, value)

        self.repository.update(tecnico)
        return tecnico

    def desativar_tecnico(self, tecnico_id: int):
        tecnico = self.repository.get_by_id(tecnico_id)
        if not tecnico:
            raise ValueError(f"Técnico {tecnico_id} não encontrado")

        tecnico.ativo = False
        self.repository.update(tecnico)
        return tecnico

    def deletar_tecnico(self, tecnico_id: int):
        tecnico = self.repository.get_by_id(tecnico_id)
        if tecnico:
            self.repository.delete(tecnico)
