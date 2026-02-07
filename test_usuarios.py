import sys
sys.path.insert(0, r'c:\Users\menezes\OneDrive\Documentos\DigitalcodeCRM\crm_provedor')

from crm_modules.usuarios.schemas import UsuarioCreate, UsuarioLogin
from crm_modules.usuarios.service import UsuarioService
from crm_core.db.base import get_db_session

# Teste 1: Criar um usuário
print("=" * 50)
print("Teste 1: Registrar novo usuario")
print("=" * 50)

usuario_data = UsuarioCreate(
    username="admin",
    email="admin@example.com",
    nome_completo="Administrador",
    senha="senha123456",
    role="admin"
)

db = get_db_session()
try:
    service = UsuarioService(repository_session=db)
    usuario = service.criar_usuario(usuario_data)
    print(f"[OK] Usuario criado: {usuario.username} ({usuario.email})")
    print(f"     Role: {usuario.role}")
    print(f"     ID: {usuario.id}")
except Exception as e:
    print(f"[ERRO] {e}")
finally:
    db.close()

# Teste 2: Fazer login
print("\n" + "=" * 50)
print("Teste 2: Login com credenciais corretas")
print("=" * 50)

db = get_db_session()
try:
    service = UsuarioService(repository_session=db)
    resultado = service.autenticar("admin", "senha123456", "127.0.0.1")
    print(f"[OK] Login realizado com sucesso")
    print(f"     Token: {resultado.access_token[:20]}...")
    print(f"     Usuario: {resultado.usuario.username}")
except Exception as e:
    print(f"[ERRO] {e}")
finally:
    db.close()

# Teste 3: Login com senha incorreta
print("\n" + "=" * 50)
print("Teste 3: Login com senha incorreta")
print("=" * 50)

db = get_db_session()
try:
    service = UsuarioService(repository_session=db)
    resultado = service.autenticar("admin", "senhaerrada", "127.0.0.1")
    print(f"[ERRO] Login nao deveria ter funcionado")
except ValueError as e:
    print(f"[OK] Erro esperado: {e}")
except Exception as e:
    print(f"[ERRO] Erro inesperado: {e}")
finally:
    db.close()

print("\n" + "=" * 50)
print("Testes concluidos!")
print("=" * 50)
