#!/usr/bin/env python3
# -*- coding: utf-8 -*-

index_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
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
        <a href="/" class="active">Home</a>
        <a href="/clientes">Clientes</a>
        <a href="/docs" target="_blank">API Docs</a>
    </div>

    <!-- Conteudo Principal -->
    <div class="main-content">
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-12">
                    <h1>Bem-vindo ao CRM Provedor</h1>
                    <p>Sistema de gerenciamento de clientes para provedores de servicos.</p>

                    <div class="row mt-5">
                        <div class="col-md-4">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">API</h5>
                                    <p class="card-text">Documentacao da API.</p>
                                    <a href="/docs" class="btn btn-secondary" target="_blank">Ver Docs</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

with open('interfaces/web/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("index.html atualizado!")
print("   - Menu horizontal convertido para menu vertical (sidebar)")
print("   - Sidebar fixada no lado esquerdo")
