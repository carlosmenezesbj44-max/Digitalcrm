#!/usr/bin/env python3
# -*- coding: utf-8 -*-

clientes_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clientes - CRM Provedor</title>
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
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Clientes</h1>
                <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#modalCadastroCliente">Novo Cliente</button>
            </div>

            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Email</th>
                            <th>Telefone</th>
                            <th>CPF</th>
                            <th>Endereco</th>
                            <th>Data Cadastro</th>
                            <th>Acoes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for cliente in clientes %}
                        <tr>
                            <td>{{ cliente.id }}</td>
                            <td>{{ cliente.nome }}</td>
                            <td>{{ cliente.email }}</td>
                            <td>{{ cliente.telefone }}</td>
                            <td>{{ cliente.cpf }}</td>
                            <td>{{ cliente.endereco }}</td>
                            <td>{{ cliente.data_cadastro.strftime('%d/%m/%Y') }}</td>
                            <td>
                                <a href="/clientes/{{ cliente.id }}/editar" class="btn btn-sm btn-primary">Editar</a>
                                <form method="post" action="/clientes/{{ cliente.id }}/desativar" style="display:inline;">
                                    <button type="submit" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza?')">Desativar</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Modal Cadastro Cliente -->
    <div class="modal fade" id="modalCadastroCliente" tabindex="-1" aria-labelledby="modalCadastroClienteLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalCadastroClienteLabel">Cadastrar Novo Cliente</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div id="alertError" class="alert alert-danger d-none" role="alert"></div>
                    <div id="alertSuccess" class="alert alert-success d-none" role="alert"></div>

                    <form id="formCadastroCliente">
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
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-primary" id="btnSubmitForm">Cadastrar Cliente</button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('btnSubmitForm').addEventListener('click', async function() {
            const form = document.getElementById('formCadastroCliente');
            const formData = new FormData(form);
            const alertError = document.getElementById('alertError');
            const alertSuccess = document.getElementById('alertSuccess');
            
            try {
                const response = await fetch('/clientes/novo', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    alertError.classList.add('d-none');
                    alertSuccess.classList.remove('d-none');
                    alertSuccess.textContent = 'Cliente cadastrado com sucesso!';
                    form.reset();
                    
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                } else {
                    const data = await response.json();
                    alertError.classList.remove('d-none');
                    alertError.textContent = 'Erro: ' + (data.message || 'Erro desconhecido');
                }
            } catch (error) {
                alertError.classList.remove('d-none');
                alertError.textContent = 'Erro: ' + error.message;
            }
        });
    </script>
</body>
</html>'''

with open('interfaces/web/templates/clientes.html', 'w', encoding='utf-8') as f:
    f.write(clientes_html)

print("clientes.html atualizado!")
print("   - Menu horizontal convertido para menu vertical (sidebar)")
print("   - Sidebar fixada no lado esquerdo")
