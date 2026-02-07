from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12
)

password = "a" * 73
print(f"Testando com senha de {len(password)} caracteres")

try:
    # Simulando o erro que o bcrypt 4.0+ costuma lançar
    hashed = pwd_context.hash(password)
    print("Hash gerado com sucesso")
except Exception as e:
    print(f"Erro ao gerar hash: {e}")

try:
    # Testando o verify
    dummy_hash = pwd_context.hash("short_pass")
    pwd_context.verify(password, dummy_hash)
except Exception as e:
    print(f"Erro ao verificar: {e}")
