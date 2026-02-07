# 🚀 Começo Rápido - Implementar Login

Este guia mostra como implementar o sistema de autenticação em 1 dia.

## Passo 1: Expandir pyproject.toml

```toml
[tool.poetry.dependencies]
# ... dependências existentes ...
python-jose = "^3.3.0"
passlib = {extras = ["bcrypt"], version = "^1.7.4"}
python-multipart = "^0.0.6"
```

Execute: `poetry install`

---

## Passo 2: Criar modelo de Usuário

```python
# crm_modules/usuarios/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base
from datetime import datetime
import enum

# Tabela associativa para many-to-many entre usuários e permissões
usuario_permissao = Table(
    'usuario_permissao',
    Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id')),
    Column('permissao_id', Integer, ForeignKey('permissao.id'))
)

class TipoRole(str, enum.Enum):
    ADMIN = "admin"
    GERENTE = "gerente"
    TECNICO = "tecnico"
    CLIENTE = "cliente"

class Usuario(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nome_completo = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True)
    role = Column(String(20), default=TipoRole.CLIENTE)
    
    # Campos para auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_acesso = Column(DateTime, nullable=True)
    
    # Relacionamentos
    permissoes = relationship("Permissao", secondary=usuario_permissao, back_populates="usuarios")
    logs_auditoria = relationship("AuditoriaLog", back_populates="usuario")
    
    def __repr__(self):
        return f"<Usuario(username='{self.username}', email='{self.email}')>"

class Permissao(Base):
    __tablename__ = "permissao"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    descricao = Column(String(255))
    modulo = Column(String(50))  # clientes, faturamento, etc
    
    usuarios = relationship("Usuario", secondary=usuario_permissao, back_populates="permissoes")

class AuditoriaLog(Base):
    __tablename__ = "auditoria_log"
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    acao = Column(String(100))  # create, update, delete, login
    recurso = Column(String(100))  # clientes, faturas, etc
    detalhes = Column(String(500))
    ip_address = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="logs_auditoria")
```

---

## Passo 3: Schemas Pydantic

```python
# crm_modules/usuarios/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class PermissaoResponse(BaseModel):
    id: int
    nome: str
    modulo: str
    
    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nome_completo: str
    role: str = "cliente"

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome_completo: Optional[str] = None
    ativo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime
    ultimo_acesso: Optional[datetime]
    permissoes: List[PermissaoResponse] = []
    
    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    username: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse

class AuditoriaLogResponse(BaseModel):
    id: int
    usuario_id: int
    acao: str
    recurso: str
    timestamp: datetime
```

---

## Passo 4: Utilitários de Autenticação

```python
# crm_core/security/auth_utils.py
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from crm_core.config.settings import settings

# Configurar contexto de hash de senha
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return pwd_context.verify(senha, senha_hash)

def obter_hash_senha(senha: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(senha)

def criar_access_token(usuario_id: int, duracao: Optional[timedelta] = None) -> str:
    """Cria JWT token"""
    if duracao is None:
        duracao = timedelta(hours=24)
    
    agora = datetime.now(timezone.utc)
    expira_em = agora + duracao
    
    payload = {
        "sub": str(usuario_id),
        "exp": expira_em,
        "iat": agora,
        "type": "access"
    }
    
    token = jwt.encode(
        payload,
        settings.secret_key,
        algorithm="HS256"
    )
    return token

def decodificar_token(token: str) -> dict:
    """Decodifica e valida JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"]
        )
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            return None
        return {"usuario_id": int(usuario_id)}
    except JWTError:
        return None
```

---

## Passo 5: Service de Usuário

```python
# crm_modules/usuarios/service.py
from crm_modules.usuarios.models import Usuario, AuditoriaLog
from crm_modules.usuarios.schemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from crm_core.security.auth_utils import obter_hash_senha, verificar_senha, criar_access_token
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

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
        
        try:
            self.session.add(novo_usuario)
            self.session.commit()
            self.session.refresh(novo_usuario)
            return novo_usuario
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Erro ao criar usuário")
    
    def autenticar(self, username: str, senha: str, ip_address: str = None):
        """Autentica usuário e retorna token"""
        usuario = self.session.query(Usuario).filter_by(username=username).first()
        
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise ValueError("Username ou senha incorretos")
        
        if not usuario.ativo:
            raise ValueError("Usuário desativado")
        
        # Atualizar último acesso
        usuario.ultimo_acesso = datetime.utcnow()
        
        # Registrar log de auditoria
        log = AuditoriaLog(
            usuario_id=usuario.id,
            acao="login",
            recurso="autenticacao",
            ip_address=ip_address
        )
        
        self.session.add(log)
        self.session.commit()
        
        # Criar token
        token = criar_access_token(usuario.id)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": UsuarioResponse.from_orm(usuario)
        }
    
    def obter_usuario(self, usuario_id: int) -> Usuario:
        """Obtém usuário por ID"""
        return self.session.query(Usuario).filter_by(id=usuario_id).first()
    
    def obter_por_username(self, username: str) -> Usuario:
        """Obtém usuário por username"""
        return self.session.query(Usuario).filter_by(username=username).first()
    
    def listar_usuarios(self) -> list:
        """Lista todos os usuários"""
        return self.session.query(Usuario).all()
    
    def atualizar_usuario(self, usuario_id: int, dados: UsuarioUpdate) -> Usuario:
        """Atualiza dados do usuário"""
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        if dados.email:
            usuario.email = dados.email
        if dados.nome_completo:
            usuario.nome_completo = dados.nome_completo
        if dados.ativo is not None:
            usuario.ativo = dados.ativo
        
        usuario.atualizado_em = datetime.utcnow()
        
        self.session.commit()
        self.session.refresh(usuario)
        return usuario
    
    def desativar_usuario(self, usuario_id: int):
        """Desativa usuário"""
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        usuario.ativo = False
        self.session.commit()
    
    def registrar_auditoria(self, usuario_id: int, acao: str, recurso: str, 
                           detalhes: str = None, ip_address: str = None):
        """Registra ação de auditoria"""
        log = AuditoriaLog(
            usuario_id=usuario_id,
            acao=acao,
            recurso=recurso,
            detalhes=detalhes,
            ip_address=ip_address
        )
        self.session.add(log)
        self.session.commit()
```

---

## Passo 6: Dependências FastAPI

```python
# crm_core/security/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from crm_core.security.auth_utils import decodificar_token
from crm_modules.usuarios.service import UsuarioService
from crm_core.db.base import get_db
from sqlalchemy.orm import Session

security = HTTPBearer()

async def obter_usuario_atual(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dependência para obter usuário autenticado"""
    token = credentials.credentials
    
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    usuario_id = payload.get("usuario_id")
    usuario_service = UsuarioService(repository_session=db)
    usuario = usuario_service.obter_usuario(usuario_id)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado",
        )
    
    return usuario

def verificar_role(role_necessario: str):
    """Dependência para verificar role do usuário"""
    async def verificador(usuario = Depends(obter_usuario_atual)):
        if usuario.role != role_necessario and usuario.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Role necessário: {role_necessario}",
            )
        return usuario
    return verificador
```

---

## Passo 7: Rotas de Autenticação

```python
# crm_modules/usuarios/api.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from crm_core.db.base import get_db
from crm_modules.usuarios.schemas import UsuarioCreate, UsuarioLogin, UsuarioResponse, TokenResponse
from crm_modules.usuarios.service import UsuarioService
from crm_core.security.dependencies import obter_usuario_atual

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """Registra novo usuário"""
    try:
        service = UsuarioService(repository_session=db)
        usuario = service.criar_usuario(usuario_data)
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(
    credenciais: UsuarioLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Autentica usuário"""
    try:
        service = UsuarioService(repository_session=db)
        ip_address = request.client.host
        resultado = service.autenticar(credenciais.username, credenciais.senha, ip_address)
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UsuarioResponse)
def obter_perfil(usuario = Depends(obter_usuario_atual)):
    """Obtém dados do usuário autenticado"""
    return usuario

@router.get("/logout")
def logout(usuario = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    """Logout do usuário (apenas marca no client)"""
    return {"mensagem": "Logout realizado com sucesso"}
```

---

## Passo 8: Adicionar Rotas ao app.py

```python
# No arquivo interfaces/web/app.py, adicione no topo:
from crm_modules.usuarios.api import router as usuarios_router

# Adicione após app = FastAPI(...):
app.include_router(usuarios_router)
```

---

## Passo 9: Template de Login

```html
<!-- interfaces/web/templates/login.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - CRM Provedor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
        }
        .login-container {
            width: 100%;
            max-width: 400px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            padding: 40px;
        }
        .login-container h2 {
            text-align: center;
            margin-bottom: 30px;
            color: #0d47a1;
        }
        .btn-login {
            background-color: #0d47a1;
            border: none;
            padding: 10px;
            font-weight: bold;
        }
        .btn-login:hover {
            background-color: #1565c0;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>CRM Provedor</h2>
        
        <form id="loginForm">
            <div class="mb-3">
                <label for="username" class="form-label">Usuário</label>
                <input 
                    type="text" 
                    class="form-control" 
                    id="username" 
                    name="username"
                    placeholder="Digite seu usuário"
                    required
                >
            </div>
            
            <div class="mb-3">
                <label for="senha" class="form-label">Senha</label>
                <input 
                    type="password" 
                    class="form-control" 
                    id="senha" 
                    name="senha"
                    placeholder="Digite sua senha"
                    required
                >
            </div>
            
            <div id="erro" class="alert alert-danger" style="display:none;"></div>
            
            <button type="submit" class="btn btn-login btn-primary w-100">Login</button>
        </form>
        
        <hr>
        
        <p class="text-center">
            Não tem conta? <a href="/registrar">Criar conta</a>
        </p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const senha = document.getElementById('senha').value;
            
            try {
                const response = await fetch('/api/usuarios/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, senha })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    document.getElementById('erro').textContent = error.detail;
                    document.getElementById('erro').style.display = 'block';
                    return;
                }
                
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                window.location.href = '/';
            } catch (error) {
                document.getElementById('erro').textContent = 'Erro ao fazer login';
                document.getElementById('erro').style.display = 'block';
            }
        });
    </script>
</body>
</html>
```

---

## Passo 10: Migração do Banco

```bash
# Gerar migração
poetry run alembic revision --autogenerate -m "Add usuario tables"

# Executar migração
poetry run alembic upgrade head
```

---

## Testando

```bash
# Registrar novo usuário
curl -X POST "http://localhost:8001/api/usuarios/registrar" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "nome_completo": "Administrador",
    "senha": "senha123456",
    "role": "admin"
  }'

# Fazer login
curl -X POST "http://localhost:8001/api/usuarios/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "senha": "senha123456"
  }'

# Obter perfil (usando token)
curl -X GET "http://localhost:8001/api/usuarios/me" \
  -H "Authorization: Bearer {seu_token_aqui}"
```

---

## Checklist

- [ ] Expandir pyproject.toml
- [ ] Criar modelos em `crm_modules/usuarios/models.py`
- [ ] Criar schemas em `crm_modules/usuarios/schemas.py`
- [ ] Criar `crm_core/security/auth_utils.py`
- [ ] Criar `crm_modules/usuarios/service.py`
- [ ] Criar `crm_core/security/dependencies.py`
- [ ] Criar `crm_modules/usuarios/api.py`
- [ ] Integrar rotas em `app.py`
- [ ] Criar template `login.html`
- [ ] Executar migração do banco
- [ ] Testar fluxo completo

**Tempo estimado: 4-6 horas**

---

## Próximos Passos

Após implementar login:
1. Adicionar middleware para verificar token em cada requisição
2. Implementar dashboard executivo
3. Adicionar sistema de roles e permissões
4. Implementar faturamento
