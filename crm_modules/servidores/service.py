from crm_modules.servidores.repository import ServidorRepository
from crm_modules.servidores.domain import Servidor
from crm_modules.servidores.schemas import ServidorCreate, ServidorUpdate
from crm_modules.servidores.models import ServidorModel
from crm_core.utils.exceptions import NotFoundException, ValidationException


class ServidorService:
    def __init__(self, repository: ServidorRepository = None, repository_session=None):
        if repository is not None:
            self.repository = repository
        else:
            self.repository = ServidorRepository(session=repository_session) if repository_session is not None else ServidorRepository()

    def criar_servidor(self, servidor_data: ServidorCreate) -> Servidor:
        # Validate
        if not servidor_data.nome or not servidor_data.ip:
            raise ValidationException("Nome e IP são obrigatórios")

        # Check if exists
        if self.repository.get_by_ip(servidor_data.ip):
            raise ValidationException("IP já cadastrado")

        # Create ORM model instance and persist
        model = ServidorModel(
            nome=servidor_data.nome,
            ip=servidor_data.ip,
            tipo_conexao=servidor_data.tipo_conexao,
            tipo_acesso=servidor_data.tipo_acesso,
            usuario=servidor_data.usuario,
            senha=servidor_data.senha,
            alterar_nome=servidor_data.alterar_nome,
            ativo=servidor_data.ativo,
        )

        model = self.repository.create(model)

        # Create domain object to return
        servidor = Servidor(
            id=model.id,
            nome=model.nome,
            ip=model.ip,
            tipo_conexao=model.tipo_conexao,
            tipo_acesso=model.tipo_acesso,
            usuario=model.usuario,
            senha=model.senha,
            alterar_nome=model.alterar_nome,
            ativo=model.ativo,
        )

        return servidor

    def obter_servidor(self, servidor_id: int) -> Servidor:
        model = self.repository.get_by_id(servidor_id)
        if not model:
            raise NotFoundException("Servidor não encontrado")
        return Servidor(
            id=model.id,
            nome=model.nome,
            ip=model.ip,
            tipo_conexao=model.tipo_conexao,
            tipo_acesso=model.tipo_acesso,
            usuario=model.usuario,
            senha=model.senha,
            alterar_nome=model.alterar_nome,
            ativo=model.ativo,
        )

    def atualizar_servidor(self, servidor_id: int, update_data: ServidorUpdate) -> Servidor:
        model = self.repository.get_by_id(servidor_id)
        if not model:
            raise NotFoundException("Servidor não encontrado")

        # Update fields
        if update_data.nome:
            model.nome = update_data.nome
        if update_data.ip:
            model.ip = update_data.ip
        if update_data.tipo_conexao:
            model.tipo_conexao = update_data.tipo_conexao
        if update_data.tipo_acesso:
            model.tipo_acesso = update_data.tipo_acesso
        if update_data.usuario:
            model.usuario = update_data.usuario
        if update_data.senha:
            model.senha = update_data.senha
        if update_data.alterar_nome is not None:
            model.alterar_nome = update_data.alterar_nome
        if update_data.ativo is not None:
            model.ativo = update_data.ativo

        self.repository.update(model)

        return self.obter_servidor(servidor_id)

    def desativar_servidor(self, servidor_id: int) -> Servidor:
        servidor = self.obter_servidor(servidor_id)
        servidor.ativo = False
        model = self.repository.get_by_id(servidor_id)
        model.ativo = False
        self.repository.update(model)
        return servidor

    def listar_servidores(self):
        models = self.repository.get_all()
        return [self.obter_servidor(m.id) for m in models]

    def listar_servidores_ativos(self):
        models = self.repository.get_active_servers()
        return [self.obter_servidor(m.id) for m in models]
