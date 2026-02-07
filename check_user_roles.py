import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
cursor.execute('SELECT username, role, ativo FROM usuario')
users = cursor.fetchall()
print('Usuarios com roles:')
for user in users:
    print(f'  - {user[0]}: role={user[1]}, ativo={user[2]}')
conn.close()