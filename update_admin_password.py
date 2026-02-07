from crm_core.security.auth_utils import obter_hash_senha
import sqlite3

# Conectar ao banco
conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Gerar hash da nova senha
nova_senha = 'senha123456'
hash_senha = obter_hash_senha(nova_senha)

# Atualizar senha do admin
cursor.execute('UPDATE usuario SET senha_hash = ? WHERE username = ?', (hash_senha, 'admin'))

conn.commit()
conn.close()

print(f'Senha do admin atualizada para: {nova_senha}')
print(f'Hash gerado: {hash_senha}')