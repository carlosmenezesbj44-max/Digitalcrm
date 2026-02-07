import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

tables = ['clientes', 'ordens_servico', 'faturas']
for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'{table}: {count} registros')

conn.close()