import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
cursor.execute('SELECT username, email FROM usuario')
users = cursor.fetchall()
print('Usuarios:')
for user in users:
    print(f'  - {user[0]} ({user[1]})')
conn.close()