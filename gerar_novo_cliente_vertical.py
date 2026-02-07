#!/usr/bin/env python3
# -*- coding: utf-8 -*-

novo_cliente_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Novo Cliente - CRM Provedor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            width: 250px;
            background-color: #0d47a1;
            color: white;
            padding: 20px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }
        .sidebar h4 {
            margin-bottom: 30px;
            font-weight: bold;
            border-bottom: 2px solid white;
            padding-bottom: 10px;
        }
        .sidebar a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 12px 15px;
            margin-bottom: 5px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .sidebar a:hover {
            background-color: #1565c0;
        }
        .sidebar a.active {
            background-color: #1976d2;
            border-left: 4px solid white;
        }
        .main-content {
            margin-left: 250px;
            flex: 1;
            padding: 20px;
        }
    </style>
</head>
<body>
    <!-- Sidebar Vertical -->
    <div class="sidebar">
        <h4>CRM Provedor</h4>
        <a href="/">Home</a>
        <a href="/clientes" class="active">Clientes</a>
        <a href="/docs" target="_blank">API Docs</a>
    </div>

    <!-- Conteudo Principal -->
    <div class="main-content">
        <div class="container-fluid">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <h1>Cadastrar Novo Cliente</h1>

                    {% if error %}
                    <div class="alert alert-danger" role="alert">
                        {{ error }}
                    </div>
                    {% endif %}

                    <form method="post" action="/clientes/novo">
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome</label>
                            <input type="text" class="form-control" id="nome" name="nome" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="telefone" class="form-label">Telefone</label>
                            <input type="text" class="form-control" id="telefone" name="telefone" required>
                        </div>
                        <div class="mb-3">
                            <label for="cpf" class="form-label">CPF</label>
                            <input type="text" class="form-control" id="cpf" name="cpf" required>
                        </div>
                        <div class="mb-3">
                            <label for="endereco" class="form-label">Endereco</label>
                            <textarea class="form-control" id="endereco" name="endereco" rows="3" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Cadastrar Cliente</button>
                        <a href="/clientes" class="btn btn-secondary">Voltar</a>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

with open('interfaces/web/templates/novo_cliente.html', 'w', encoding='utf-8') as f:
    f.write(novo_cliente_html)

print("novo_cliente.html atualizado!")
print("   - Menu horizontal convertido para menu vertical (sidebar)")
