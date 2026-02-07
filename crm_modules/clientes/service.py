from crm_modules.clientes.repository import ClienteRepository
from crm_modules.clientes.domain import Cliente
from crm_modules.clientes.schemas import ClienteCreate, ClienteUpdate, ClienteArquivo
from crm_modules.clientes.models import ClienteModel
from crm_modules.clientes.models_arquivos import ClienteArquivoModel
from crm_core.utils.exceptions import NotFoundException, ValidationException
from crm_core.events.bus import EventBus
from crm_core.events.events import ClientCreatedEvent
from datetime import datetime
import os
import shutil
from pathlib import Path
from sqlalchemy.orm import Session as SASession


class ClienteService:
    def __init__(self, repository: ClienteRepository = None, repository_session=None, event_bus: EventBus = None):
        # Allow passing a raw SQLAlchemy session in the first position (tests)
        if repository is not None and isinstance(repository, SASession):
            repository_session = repository
            repository = None
        # If a repository is provided, use it. Otherwise construct one using
        # an optional `repository_session` to allow request-scoped sessions.
        if repository is not None:
            self.repository = repository
        else:
            self.repository = ClienteRepository(session=repository_session) if repository_session is not None else ClienteRepository()
        self.event_bus = event_bus or EventBus()

    def criar_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        # Validate
        if not cliente_data.nome or not cliente_data.email:
            raise ValidationException("Nome e email são obrigatórios")

        # Check if exists
        if self.repository.get_by_email(cliente_data.email):
            raise ValidationException("Email já cadastrado")

        # Create ORM model instance and persist
        model = ClienteModel(
            nome=cliente_data.nome,
            email=cliente_data.email,
            telefone=cliente_data.telefone,
            cpf=cliente_data.cpf,
            endereco=getattr(cliente_data, 'endereco', None) or getattr(cliente_data, 'rua', None),
            rua=getattr(cliente_data, 'rua', None),
            numero=getattr(cliente_data, 'numero', None),
            bairro=getattr(cliente_data, 'bairro', None),
            cidade=getattr(cliente_data, 'cidade', None),
            cep=getattr(cliente_data, 'cep', None),
            apartamento=getattr(cliente_data, 'apartamento', None),
            complemento=getattr(cliente_data, 'complemento', None),
            moradia=getattr(cliente_data, 'moradia', None),
            tipo_localidade=getattr(cliente_data, 'tipo_localidade', None),
            latitude=getattr(cliente_data, 'latitude', None),
            longitude=getattr(cliente_data, 'longitude', None),
            tipo_cliente=cliente_data.tipo_cliente,
            data_cadastro=datetime.utcnow(),
            ativo=cliente_data.ativo,
            nacionalidade=getattr(cliente_data, 'nacionalidade', None),
            rg=getattr(cliente_data, 'rg', None),
            orgao_emissor=getattr(cliente_data, 'orgao_emissor', None),
            naturalidade=getattr(cliente_data, 'naturalidade', None),
            data_nascimento=getattr(cliente_data, 'data_nascimento', None),
            username=getattr(cliente_data, 'username', None),
            observacoes=getattr(cliente_data, 'observacoes', None),
            whatsapp=getattr(cliente_data, 'whatsapp', None),
            telefone_residencial=getattr(cliente_data, 'telefone_residencial', None),
            telefone_comercial=getattr(cliente_data, 'telefone_comercial', None),
            telefone_celular=getattr(cliente_data, 'telefone_celular', None),
            instagram=getattr(cliente_data, 'instagram', None),
            servidor_id=getattr(cliente_data, 'servidor_id', None),
            plano_id=getattr(cliente_data, 'plano_id', None),
            profile=getattr(cliente_data, 'profile', None),
            tipo_servico=getattr(cliente_data, 'tipo_servico', 'pppoe'),
            comentario_login=getattr(cliente_data, 'comentario_login', None),
            valor_total=getattr(cliente_data, 'valor_total', None),
        )

        # Vincular produtos se fornecidos
        if hasattr(cliente_data, 'produto_ids') and cliente_data.produto_ids:
            from crm_modules.produtos.models import ProdutoModel
            produtos = self.repository.session.query(ProdutoModel).filter(ProdutoModel.id.in_(cliente_data.produto_ids)).all()
            model.produtos = produtos

        model = self.repository.create(model)

        # Sincronizar com MikroTik se username e password fornecidos
        if getattr(cliente_data, 'username', None) and getattr(cliente_data, 'password', None):
            from crm_modules.mikrotik.integration import sincronizar_cliente_mikrotik
            from crm_modules.servidores.service import ServidorService
            
            profile = getattr(cliente_data, 'plano', 'default') or 'default'
            
            host, user, secret = None, None, None
            if model.servidor_id:
                try:
                    servidor_service = ServidorService(repository_session=self.repository.session)
                    servidor = servidor_service.obter_servidor(model.servidor_id)
                    host = servidor.ip
                    user = servidor.usuario
                    secret = servidor.senha
                except Exception as e:
                    print(f"Erro ao obter dados do servidor {model.servidor_id}: {e}")
            
            sincronizar_cliente_mikrotik(
                cliente_data.username, 
                cliente_data.password, 
                profile,
                host=host,
                user=user,
                secret=secret
            )

        # Create domain object to return
        cliente = Cliente(
            id=model.id,
            nome=model.nome,
            email=model.email,
            telefone=model.telefone,
            cpf=model.cpf,
            endereco=model.endereco,
            tipo_cliente=model.tipo_cliente,
            data_cadastro=model.data_cadastro,
            ativo=model.ativo,
            nacionalidade=model.nacionalidade,
            rg=model.rg,
            orgao_emissor=model.orgao_emissor,
            naturalidade=model.naturalidade,
            data_nascimento=model.data_nascimento,
            username=model.username,
            observacoes=model.observacoes,
            rua=model.rua,
            numero=model.numero,
            bairro=model.bairro,
            cidade=model.cidade,
            cep=model.cep,
            estado=model.estado,
            apartamento=model.apartamento,
            complemento=model.complemento,
            whatsapp=model.whatsapp,
            telefone_residencial=model.telefone_residencial,
            telefone_comercial=model.telefone_comercial,
            telefone_celular=model.telefone_celular,
            instagram=model.instagram,
            servidor_id=model.servidor_id,
            plano_id=model.plano_id,
            profile=model.profile,
            tipo_servico=model.tipo_servico,
            comentario_login=model.comentario_login,
            foto_casa=model.foto_casa,
            valor_mensal=model.valor_mensal,
            dia_vencimento=model.dia_vencimento,
            arquivos=[],
            produto_ids=[p.id for p in model.produtos] if hasattr(model, 'produtos') else [],
            valor_total=model.valor_total,
        )

        # Publish event
        self.event_bus.publish(ClientCreatedEvent(cliente.id, cliente.email))

        return cliente

    def obter_cliente(self, cliente_id: int) -> Cliente:
        model = self.repository.get_by_id(cliente_id)
        if not model:
            raise NotFoundException("Cliente não encontrado")
        
        # Se o valor mensal do cliente for nulo ou zero, tenta buscar o valor do plano
        valor_mensal = model.valor_mensal
        if (valor_mensal is None or valor_mensal == 0) and model.plano_id:
            try:
                from crm_modules.planos.models import PlanoModel
                plano = self.repository.session.query(PlanoModel).filter(PlanoModel.id == model.plano_id).first()
                if plano:
                    valor_mensal = plano.valor_mensal
            except Exception as e:
                print(f"Erro ao buscar valor do plano para o cliente {cliente_id}: {e}")
        # NÃ£o faz fallback para valor de contrato aqui; somente plano ou valor_mensal direto

        return Cliente(
            id=model.id,
            nome=model.nome,
            email=model.email,
            telefone=model.telefone,
            cpf=model.cpf,
            endereco=model.endereco,
            tipo_cliente=model.tipo_cliente,
            data_cadastro=model.data_cadastro,
            ativo=model.ativo,
            nacionalidade=model.nacionalidade,
            rg=model.rg,
            orgao_emissor=model.orgao_emissor,
            naturalidade=model.naturalidade,
            data_nascimento=model.data_nascimento,
            username=model.username,
            observacoes=model.observacoes,
            rua=model.rua,
            numero=model.numero,
            bairro=model.bairro,
            cidade=model.cidade,
            cep=model.cep,
            estado=model.estado,
            apartamento=model.apartamento,
            complemento=model.complemento,
            whatsapp=model.whatsapp,
            telefone_residencial=model.telefone_residencial,
            telefone_comercial=model.telefone_comercial,
            telefone_celular=model.telefone_celular,
            instagram=model.instagram,
            servidor_id=model.servidor_id,
            plano_id=model.plano_id,
            profile=model.profile,
            tipo_servico=model.tipo_servico,
            comentario_login=model.comentario_login,
            status_contrato=model.status_contrato or "nenhum",
            foto_casa=model.foto_casa,
            valor_mensal=valor_mensal,
            dia_vencimento=model.dia_vencimento,
            arquivos=list(model.arquivos) if hasattr(model, 'arquivos') else [],
            produto_ids=[p.id for p in model.produtos] if hasattr(model, 'produtos') else [],
            valor_total=model.valor_total,
        )

    def atualizar_cliente(self, cliente_id: int, update_data: ClienteUpdate) -> Cliente:
        model = self.repository.get_by_id(cliente_id)
        if not model:
            raise NotFoundException("Cliente não encontrado")

        # Update fields
        if update_data.nome:
            model.nome = update_data.nome
        if update_data.email:
            model.email = update_data.email
        if update_data.telefone:
            model.telefone = update_data.telefone
        if update_data.endereco:
            model.endereco = update_data.endereco
        if update_data.ativo is not None:
            model.ativo = update_data.ativo
        if update_data.valor_total is not None:
            model.valor_total = update_data.valor_total

        # Atualizar produtos vinculados
        if hasattr(update_data, 'produto_ids') and update_data.produto_ids is not None:
            from crm_modules.produtos.models import ProdutoModel
            produtos = self.repository.session.query(ProdutoModel).filter(ProdutoModel.id.in_(update_data.produto_ids)).all()
            model.produtos = produtos

        self.repository.update(model)

        return self.obter_cliente(cliente_id)

    def desativar_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.obter_cliente(cliente_id)
        cliente.ativo = False
        model = self.repository.get_by_id(cliente_id)
        model.ativo = False
        self.repository.update(model)
        return cliente

    def listar_clientes_ativos(self):
        models = self.repository.get_active_clients()
        return [self.obter_cliente(m.id) for m in models]

    def listar_clientes(self):
        """Lista todos os clientes (ativos e inativos)"""
        models = self.repository.session.query(ClienteModel).order_by(ClienteModel.id.desc()).all()
        clientes = []
        for m in models:
            try:
                clientes.append(self.obter_cliente(m.id))
            except Exception as e:
                print(f"DEBUG: Erro ao obter cliente {m.id}: {e}")
        return clientes

    def buscar_clientes_por_nome(self, nome: str):
        """Busca clientes por nome"""
        models = self.repository.search_by_name(nome)
        return [self.obter_cliente(m.id) for m in models]

    def atualizar_status_contrato(self, cliente_id: int, status: str):
        """Atualiza status de contrato do cliente"""
        model = self.repository.get_by_id(cliente_id)
        if not model:
            raise NotFoundException("Cliente não encontrado")

        if status not in ["nenhum", "aguardando_assinatura", "assinado"]:
            raise ValidationException("Status de contrato inválido")

        model.status_contrato = status
        self.repository.update(model)

    def listar_clientes_filtrados(self, q: str = "", status: str = "", page: int = 1, per_page: int = 50, field: str = "todos"):
        """Lista clientes com filtros e paginação"""
        models, total = self.repository.get_filtered_clients(q, status, page, per_page, field)
        clientes = [self.obter_cliente(m.id) for m in models]
        return clientes, total

    def _get_upload_dir(self, cliente_id: int) -> Path:
        """Retorna o diretório de uploads para o cliente"""
        base_dir = Path(__file__).parent.parent.parent
        upload_dir = base_dir / 'interfaces' / 'web' / 'static' / 'uploads' / 'clientes' / str(cliente_id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        return upload_dir

    def upload_arquivo_cliente(self, cliente_id: int, file_content: bytes, filename: str) -> ClienteArquivoModel:
        """Faz upload de um documento para o cliente"""
        model = self.repository.get_by_id(cliente_id)
        if not model:
            raise NotFoundException("Cliente não encontrado")

        upload_dir = self._get_upload_dir(cliente_id)
        file_path = upload_dir / filename

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Salvar metadados
        relative_path = f"/static/uploads/clientes/{cliente_id}/{filename}"
        arquivo = ClienteArquivoModel(
            cliente_id=cliente_id,
            filename=filename,
            filepath=relative_path
        )
        self.repository.session.add(arquivo)
        self.repository.session.commit()
        self.repository.session.refresh(arquivo)
        return arquivo

    def upload_foto_casa(self, cliente_id: int, file_content: bytes, filename: str) -> str:
        """Faz upload da foto da casa do cliente"""
        model = self.repository.get_by_id(cliente_id)
        if not model:
            raise NotFoundException("Cliente não encontrado")

        upload_dir = self._get_upload_dir(cliente_id)
        # Usar um nome padrão para a foto da casa ou preservar original
        ext = filename.split('.')[-1]
        photo_filename = f"foto_casa_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = upload_dir / photo_filename

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Atualizar campo no modelo do cliente
        relative_path = f"/static/uploads/clientes/{cliente_id}/{photo_filename}"
        model.foto_casa = relative_path
        self.repository.update(model)
        return relative_path

    def listar_arquivos(self, cliente_id: int):
        """Lista todos os arquivos de um cliente"""
        return self.repository.session.query(ClienteArquivoModel).filter_by(cliente_id=cliente_id).all()

    def excluir_arquivo(self, arquivo_id: int):
        """Exclui um arquivo do cliente"""
        arquivo = self.repository.session.query(ClienteArquivoModel).get(arquivo_id)
        if not arquivo:
            raise NotFoundException("Arquivo não encontrado")

        # Remover arquivo físico
        base_dir = Path(__file__).parent.parent.parent
        # filepath is like "/static/uploads/clientes/1/doc.pdf"
        # we need to map it to local filesystem
        relative_path = arquivo.filepath.lstrip('/')
        full_path = base_dir / 'interfaces' / 'web' / relative_path

        if full_path.exists():
            full_path.unlink()

        self.repository.session.delete(arquivo)
        self.repository.session.commit()
        return True
