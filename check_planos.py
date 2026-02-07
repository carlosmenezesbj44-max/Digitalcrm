
import sqlite3
conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
cursor.execute("SELECT id, nome, ativo FROM planos")
rows = cursor.fetchall()
print(f"Total planos: {len(rows)}")
for row in rows:
    print(row)
conn.close()
