import sys
sys.path.append('.')

from crm_core.security.auth_utils import verificar_senha
import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
cursor.execute('SELECT username, senha_hash FROM usuario WHERE username = ?', ('admin',))
user = cursor.fetchone()
conn.close()

if user:
    username, hash = user
    test_passwords = ['senha123456', 'admin', '123456']
    for pwd in test_passwords:
        if verificar_senha(pwd, hash):
            print(f'Senha correta para {username}: {pwd}')
            break
    else:
        print(f'Nenhuma senha testada funciona para {username}')
else:
    print('Usuario nao encontrado')