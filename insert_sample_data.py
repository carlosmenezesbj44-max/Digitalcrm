from datetime import datetime
import sqlite3

conn = sqlite3.connect('crm.db')
cursor = conn.cursor()

# Inserir clientes
cursor.execute('''
INSERT INTO clientes (nome, email, telefone, cpf, endereco, data_cadastro, ativo, status_servico)
VALUES
('João Silva', 'joao@email.com', '11999999999', '12345678901', 'Rua A, 123', ?, 1, 'ativo'),
('Maria Santos', 'maria@email.com', '11888888888', '23456789012', 'Rua B, 456', ?, 1, 'ativo'),
('Pedro Oliveira', 'pedro@email.com', '11777777777', '34567890123', 'Rua C, 789', ?, 1, 'ativo')
''', (datetime.utcnow(), datetime.utcnow(), datetime.utcnow()))

# Inserir ordens de serviço
cursor.execute('''
INSERT INTO ordens_servico (cliente_id, tipo_servico, titulo, descricao, status, prioridade, data_criacao)
VALUES
(1, 'instalacao', 'Instalação Internet', 'Instalar internet fibra', 'aberta', 'normal', ?),
(2, 'manutencao', 'Manutenção Rede', 'Verificar velocidade', 'em_andamento', 'alta', ?),
(3, 'instalacao', 'Instalação WiFi', 'Configurar roteador', 'concluida', 'normal', ?)
''', (datetime.utcnow(), datetime.utcnow(), datetime.utcnow()))

# Inserir faturas
cursor.execute('''
INSERT INTO faturas (cliente_id, numero_fatura, data_emissao, data_vencimento, valor_total, status)
VALUES
(1, 'FAT-2024-001', ?, '2024-02-15', 150.00, 'pago'),
(2, 'FAT-2024-002', ?, '2024-02-15', 200.00, 'pago'),
(3, 'FAT-2024-003', ?, '2024-02-15', 120.00, 'pendente')
''', (datetime.utcnow(), datetime.utcnow(), datetime.utcnow()))

conn.commit()
conn.close()

print('Dados de exemplo inseridos com sucesso!')