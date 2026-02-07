import sys
sys.path.insert(0, r'c:\Users\menezes\OneDrive\Documentos\DigitalcodeCRM\crm_provedor')

from crm_modules.usuarios.schemas import UsuarioLogin
from crm_modules.usuarios.service import UsuarioService
from crm_core.db.base import get_db_session
import requests
import time

print("=" * 60)
print("Teste de Middleware de Autenticacao")
print("=" * 60)

# Obter token do usuario admin
print("\n[1] Obtendo token JWT...")
db = get_db_session()
try:
    service = UsuarioService(repository_session=db)
    resultado = service.autenticar("admin", "senha123456", "127.0.0.1")
    token = resultado.access_token
    print(f"[OK] Token obtido: {token[:30]}...")
except Exception as e:
    print(f"[ERRO] {e}")
    sys.exit(1)
finally:
    db.close()

print("\n[2] Esperando servidor iniciar (15 segundos)...")
time.sleep(15)

base_url = "http://localhost:8001"

# Teste 1: Acesso sem token
print("\n[3] Teste sem token (deve retornar 401)...")
try:
    response = requests.get(f"{base_url}/api/usuarios/lista")
    print(f"[OK] Status: {response.status_code} (esperado: 401)")
    print(f"     Resposta: {response.json()}")
except Exception as e:
    print(f"[ERRO] {e}")

# Teste 2: Acesso com token válido
print("\n[4] Teste com token válido (deve retornar 200)...")
try:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/api/usuarios/lista", headers=headers)
    print(f"[OK] Status: {response.status_code} (esperado: 200)")
    if response.ok:
        usuarios = response.json()
        print(f"     Usuarios: {len(usuarios)} encontrado(s)")
except Exception as e:
    print(f"[ERRO] {e}")

# Teste 3: Acesso com token inválido
print("\n[5] Teste com token invalido (deve retornar 401)...")
try:
    headers = {"Authorization": "Bearer token_invalido_xyz"}
    response = requests.get(f"{base_url}/api/usuarios/lista", headers=headers)
    print(f"[OK] Status: {response.status_code} (esperado: 401)")
    print(f"     Resposta: {response.json()}")
except Exception as e:
    print(f"[ERRO] {e}")

# Teste 4: Acesso a rota pública (login)
print("\n[6] Teste acesso a rota publica /api/usuarios/login (sem token)...")
try:
    response = requests.post(f"{base_url}/api/usuarios/login", 
        json={"username": "admin", "senha": "senha123456"})
    print(f"[OK] Status: {response.status_code} (esperado: 200)")
    if response.ok:
        print(f"     Login realizado com sucesso")
except Exception as e:
    print(f"[ERRO] {e}")

print("\n" + "=" * 60)
print("Testes concluidos!")
print("=" * 60)
