#!/usr/bin/env python3

html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">CRM Provedor</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/clientes">Clientes</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row">
            <div class="col-md-12">
                <h1>Bem-vindo ao CRM Provedor</h1>
                <p>Sistema de gerenciamento de clientes para provedores de serviços.</p>

                <div class="row">
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Clientes</h5>
                                <p class="card-text">Gerencie seus clientes.</p>
                                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modalCadastroCliente">Cadastrar Cliente</button>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">API</h5>
                                <p class="card-text">Documentação da API.</p>
                                <a href="/docs" class="btn btn-secondary" target="_blank">Ver Docs</a>
                            </div>
                        </div>
                    </div>
                </div>
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
                            <label for="endereco" class="form-label">Endereço</label>
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
                        const modal = bootstrap.Modal.getInstance(document.getElementById('modalCadastroCliente'));
                        modal.hide();
                        window.location.href = '/clientes';
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

with open('interfaces/web/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Arquivo index.html criado com sucesso!")
