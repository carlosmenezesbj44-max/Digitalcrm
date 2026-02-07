from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from crm_core.config.settings import settings

# Configurar contexto de hash de senha
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
)

def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return pwd_context.verify(senha, senha_hash)

def obter_hash_senha(senha: str) -> str:
    """Gera hash da senha"""
    # Limitar senha a 72 caracteres para compatibilidade com bcrypt
    senha = senha[:72]
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
