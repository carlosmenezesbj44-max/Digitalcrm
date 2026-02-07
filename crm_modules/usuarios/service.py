from crm_modules.usuarios.models import Usuario, AuditoriaLog, Permissao, Grupo
from crm_modules.usuarios.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, TokenResponse
from crm_core.security.auth_utils import obter_hash_senha, verificar_senha, criar_access_token
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from pathlib import Path
import json

class UsuarioService:
    def __init__(self, repository_session: Session = None):
        self.session = repository_session
    
    def criar_usuario(self, usuario_data: UsuarioCreate) -> Usuario:
        """Cria novo usuário"""
        # Verificar se usuário já existe
        existente = self.session.query(Usuario).filter_by(
            username=usuario_data.username
        ).first()
        if existente:
            raise ValueError("Username já existe")
        
        # Verificar email
        existente_email = self.session.query(Usuario).filter_by(
            email=usuario_data.email
        ).first()
        if existente_email:
            raise ValueError("Email já está registrado")
        
        # Criar usuário
        novo_usuario = Usuario(
            username=usuario_data.username,
            email=usuario_data.email,
            nome_completo=usuario_data.nome_completo,
            senha_hash=obter_hash_senha(usuario_data.senha),
            role=usuario_data.role
        )
        
        self.session.add(novo_usuario)
        self.session.commit()
        self.session.refresh(novo_usuario)
        return novo_usuario
    
    def autenticar(self, username: str, senha: str, ip_address: str = None) -> TokenResponse:
        """Autentica usuário e retorna token"""
        usuario = self.session.query(Usuario).filter_by(username=username).first()
        
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        if not verificar_senha(senha, usuario.senha_hash):
            raise ValueError("Senha incorreta")
        
        if not usuario.ativo:
            raise ValueError("Usuário inativo")
        
        # Atualizar último acesso
        usuario.ultimo_acesso = datetime.utcnow()
        self.session.commit()
        
        # Registrar login na auditoria
        if ip_address:
            log = AuditoriaLog(
                usuario_id=usuario.id,
                acao="login",
                recurso="autenticacao",
                ip_address=ip_address,
                detalhes=f"Login realizado de {ip_address}"
            )
            self.session.add(log)
            self.session.commit()
        
        # Criar token
        access_token = criar_access_token(usuario.id)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            usuario=UsuarioResponse.model_validate(usuario)
        )
    
    def obter_usuario_por_id(self, usuario_id: int) -> Usuario:
        """Obtém usuário por ID"""
        return self.session.query(Usuario).filter_by(id=usuario_id).first()
    
    def obter_usuario_por_username(self, username: str) -> Usuario:
        """Obtém usuário por username"""
        return self.session.query(Usuario).filter_by(username=username).first()
    
    def atualizar_usuario(self, usuario_id: int, usuario_data: UsuarioUpdate) -> Usuario:
        """Atualiza dados do usuário"""
        usuario = self.obter_usuario_por_id(usuario_id)
        
        if usuario is None:
            raise ValueError("Usuário não encontrado")
        
        if usuario_data.email:
            # Verificar se email já está em uso
            existente = self.session.query(Usuario).filter(
                Usuario.email == usuario_data.email,
                Usuario.id != usuario_id
            ).first()
            if existente:
                raise ValueError("Email já está registrado")
            usuario.email = usuario_data.email
        
        if usuario_data.nome_completo:
            usuario.nome_completo = usuario_data.nome_completo
        
        if usuario_data.ativo is not None:
            usuario.ativo = usuario_data.ativo

        if usuario_data.foto_url is not None:
            usuario.foto_url = usuario_data.foto_url

        if usuario_data.preferencias is not None:
            usuario.preferencias = json.dumps(usuario_data.preferencias)
        
        usuario.atualizado_em = datetime.utcnow()
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def atualizar_senha(self, usuario_id: int, senha_atual: str, nova_senha: str) -> Usuario:
        """Atualiza senha do usuÃ¡rio"""
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("UsuÃ¡rio nÃ£o encontrado")

        if not verificar_senha(senha_atual, usuario.senha_hash):
            raise ValueError("Senha atual incorreta")

        usuario.senha_hash = obter_hash_senha(nova_senha)
        usuario.atualizado_em = datetime.utcnow()
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def upload_foto_usuario(self, usuario_id: int, file_content: bytes, filename: str) -> str:
        """Faz upload da foto do usuÃ¡rio"""
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("UsuÃ¡rio nÃ£o encontrado")

        ext = filename.split('.')[-1] if '.' in filename else 'png'
        photo_filename = f"avatar_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"

        base_dir = Path("interfaces/web/static/uploads/usuarios") / str(usuario_id)
        base_dir.mkdir(parents=True, exist_ok=True)
        file_path = base_dir / photo_filename

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        relative_path = f"/static/uploads/usuarios/{usuario_id}/{photo_filename}"
        usuario.foto_url = relative_path
        usuario.atualizado_em = datetime.utcnow()
        self.session.commit()
        self.session.refresh(usuario)
        return relative_path

    def obter_preferencias(self, usuario_id: int) -> dict:
        """ObtÃ©m preferÃªncias do usuÃ¡rio"""
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("UsuÃ¡rio nÃ£o encontrado")

        if not usuario.preferencias:
            return {}

        try:
            return json.loads(usuario.preferencias)
        except json.JSONDecodeError:
            return {}

    def atualizar_preferencias(self, usuario_id: int, preferencias: dict) -> dict:
        """Atualiza preferÃªncias do usuÃ¡rio"""
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("UsuÃ¡rio nÃ£o encontrado")

        usuario.preferencias = json.dumps(preferencias)
        usuario.atualizado_em = datetime.utcnow()
        self.session.commit()
        self.session.refresh(usuario)
        return preferencias
    
    def listar_usuarios(self, skip: int = 0, limit: int = 10) -> list:
        """Lista usuários com paginação"""
        return self.session.query(Usuario).offset(skip).limit(limit).all()
    

    def listar_permissoes(self) -> list:
        """Lista todas as permiss?es"""
        return self.session.query(Permissao).order_by(Permissao.modulo, Permissao.nome).all()

    def criar_permissao(self, nome: str, modulo: str, descricao: str | None = None) -> Permissao:
        """Cria permiss?o se n?o existir"""
        existente = self.session.query(Permissao).filter_by(nome=nome, modulo=modulo).first()
        if existente:
            return existente

        permissao = Permissao(nome=nome, modulo=modulo, descricao=descricao)
        self.session.add(permissao)
        self.session.commit()
        self.session.refresh(permissao)
        return permissao

    def listar_grupos(self) -> list:
        """Lista todos os grupos"""
        return self.session.query(Grupo).order_by(Grupo.nome).all()

    def obter_grupo(self, grupo_id: int) -> Grupo | None:
        return self.session.query(Grupo).filter_by(id=grupo_id).first()

    def criar_grupo(self, nome: str, descricao: str | None = None, permissoes_ids: list[int] | None = None) -> Grupo:
        """Cria grupo com permiss?es"""
        existente = self.session.query(Grupo).filter_by(nome=nome).first()
        if existente:
            raise ValueError("Grupo j? existe")

        grupo = Grupo(nome=nome, descricao=descricao)
        if permissoes_ids:
            permissoes = self.session.query(Permissao).filter(Permissao.id.in_(permissoes_ids)).all()
            grupo.permissoes = permissoes

        self.session.add(grupo)
        self.session.commit()
        self.session.refresh(grupo)
        return grupo

    def atualizar_grupo(self, grupo_id: int, nome: str | None = None, descricao: str | None = None, permissoes_ids: list[int] | None = None) -> Grupo:
        """Atualiza grupo"""
        grupo = self.obter_grupo(grupo_id)
        if grupo is None:
            raise ValueError("Grupo n?o encontrado")

        if nome:
            grupo.nome = nome
        if descricao is not None:
            grupo.descricao = descricao
        if permissoes_ids is not None:
            permissoes = self.session.query(Permissao).filter(Permissao.id.in_(permissoes_ids)).all()
            grupo.permissoes = permissoes

        self.session.commit()
        self.session.refresh(grupo)
        return grupo

    def deletar_grupo(self, grupo_id: int) -> None:
        grupo = self.obter_grupo(grupo_id)
        if grupo is None:
            raise ValueError("Grupo n?o encontrado")
        self.session.delete(grupo)
        self.session.commit()

    def definir_permissoes_usuario(self, usuario_id: int, permissoes_ids: list[int]) -> Usuario:
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usu?rio n?o encontrado")
        permissoes = self.session.query(Permissao).filter(Permissao.id.in_(permissoes_ids)).all()
        usuario.permissoes = permissoes
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def definir_grupos_usuario(self, usuario_id: int, grupos_ids: list[int]) -> Usuario:
        usuario = self.obter_usuario_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usu?rio n?o encontrado")
        grupos = self.session.query(Grupo).filter(Grupo.id.in_(grupos_ids)).all()
        usuario.grupos = grupos
        self.session.commit()
        self.session.refresh(usuario)
        return usuario
    def deletar_usuario(self, usuario_id: int) -> bool:
        """Deleta usuário"""
        usuario = self.obter_usuario_por_id(usuario_id)

        if usuario is None:
            raise ValueError("Usuário não encontrado")

        # Remover relacionamentos para evitar erros de FK
        usuario.permissoes.clear()  # Remove associações many-to-many
        usuario.grupos.clear()  # Remove associa??es de grupos
        # Logs de auditoria são mantidos para histórico, mas podemos deletar se necessário
        self.session.query(AuditoriaLog).filter_by(usuario_id=usuario_id).delete()

        self.session.delete(usuario)
        self.session.commit()
        return True
