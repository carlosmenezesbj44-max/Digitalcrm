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

    def _to_domain(self, model: ServidorModel) -> Servidor:
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

        return self._to_domain(model)

    def obter_servidor(self, servidor_id: int) -> Servidor:
        model = self.repository.get_by_id(servidor_id)
        if not model:
            raise NotFoundException("Servidor não encontrado")
        return self._to_domain(model)

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

        return self._to_domain(model)

    def desativar_servidor(self, servidor_id: int) -> Servidor:
        model = self.repository.get_by_id(servidor_id)
        if not model:
            raise NotFoundException("Servidor não encontrado")
        model.ativo = False
        self.repository.update(model)
        return self._to_domain(model)

    def listar_servidores(self):
        models = self.repository.get_all()
        return [self._to_domain(m) for m in models]

    def listar_servidores_ativos(self, verificar_conexao: bool = True):
        models = self.repository.get_active_servers()
        servidores = []
        for model in models:
            servidor = self._to_domain(model)
            # Adicionar status de conexão apenas se solicitado
            if verificar_conexao:
                servidor.status = self._verificar_status_conexao(servidor)
            else:
                servidor.status = "unknown"
            servidores.append(servidor)
        return servidores
    
    def _verificar_status_conexao(self, servidor) -> str:
        """Verifica o status de conexão com o servidor"""
        if servidor.tipo_conexao.lower() != "mikrotik":
            return "offline"
        
        try:
            import routeros_api
            connection = routeros_api.RouterOsApiPool(
                servidor.ip,
                username=servidor.usuario,
                password=servidor.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Verificar se é possível obter informações do sistema
            system_resource = api.get_resource('/system/resource')
            system_resource.get()[0]
            
            connection.disconnect()
            
            return "online"
            
        except Exception as e:
            return "offline"
    
    def testar_conexao(self, servidor_id: int) -> dict:
        """Testa a conexão com um servidor MikroTik"""
        servidor = self.obter_servidor(servidor_id)
        
        if servidor.tipo_conexao.lower() != "mikrotik":
            return {"success": False, "message": "Tipo de servidor não é MikroTik"}
        
        try:
            import routeros_api
            connection = routeros_api.RouterOsApiPool(
                servidor.ip,
                username=servidor.usuario,
                password=servidor.senha,
                port=8728,
                plaintext_login=True
            )
            api = connection.get_api()
            
            # Obter informações do sistema para verificar a conexão
            system_resource = api.get_resource('/system/resource')
            system_info = system_resource.get()[0]
            
            connection.disconnect()
            
            return {
                "success": True,
                "message": "Conexão bem-sucedida",
                "informacoes": {
                    "device": system_info.get('board-name', 'Desconhecido'),
                    "version": system_info.get('version', 'Desconhecido'),
                    "modelo": system_info.get('model', 'Desconhecido')
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Erro ao conectar: {str(e)}"}
