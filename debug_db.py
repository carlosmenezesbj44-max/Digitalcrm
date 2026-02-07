import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Verificar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()
print("Tabelas no banco:")
for t in tabelas:
    print("  -", t[0])

# Verificar servidores
print("\nServidores:")
cursor.execute("SELECT id, nome, ip, tipo_conexao, ativo FROM servidores")
for row in cursor.fetchall():
    print(f"  ID: {row[0]}, Nome: {row[1]}, IP: {row[2]}, Tipo: {row[3]}, Ativo: {row[4]}")

conn.close()
