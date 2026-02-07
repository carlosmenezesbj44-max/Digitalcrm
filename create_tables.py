import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Criar tabela faturas
cursor.execute('''
CREATE TABLE IF NOT EXISTS faturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    numero_fatura TEXT NOT NULL UNIQUE,
    data_emissao DATETIME,
    data_vencimento DATE NOT NULL,
    valor_total REAL NOT NULL,
    status TEXT DEFAULT 'pendente',
    valor_pago REAL DEFAULT 0.0,
    descricao TEXT,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
)
''')

# Criar tabela pagamentos
cursor.execute('''
CREATE TABLE IF NOT EXISTS pagamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fatura_id INTEGER NOT NULL,
    valor_pago REAL NOT NULL,
    data_pagamento DATETIME,
    metodo_pagamento TEXT NOT NULL,
    referencia TEXT,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT 1,
    FOREIGN KEY (fatura_id) REFERENCES faturas (id)
)
''')

conn.commit()
conn.close()

print("Tabelas faturas e pagamentos criadas com sucesso!")