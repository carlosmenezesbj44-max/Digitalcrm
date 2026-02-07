#!/usr/bin/env python3
# -*- coding: utf-8 -*-

clientes_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clientes - CRM Provedor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
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
        .sidebar a, .sidebar button {
            display: block;
            color: white;
            text-decoration: none;
            padding: 12px 15px;
            margin-bottom: 5px;
            border-radius: 4px;
            transition: background-color 0.3s;
            width: 100%;
            text-align: left;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 14px;
        }
        .sidebar a:hover, .sidebar button:hover {
            background-color: #1565c0;
        }
        .sidebar a.active {
            background-color: #1976d2;
            border-left: 4px solid white;
        }
        .submenu {
            margin-left: 15px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        .submenu.show {
            max-height: 500px;
        }
        .submenu a {
            padding: 10px 12px;
            font-size: 13px;
            margin-bottom: 3px;
        }
        .menu-toggle {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .main-content {
            margin-left: 250px;
            flex: 1;
            padding: 20px;
        }
        .search-box {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <!-- Sidebar Vertical -->
    <div class="sidebar">
        <h4>CRM Provedor</h4>
        <a href="/"><i class="bi bi-house"></i> Home</a>
        
        <!-- Menu Cadastros com Submenu -->
        <button class="menu-toggle" onclick="toggleSubmenu(this)">
            <span><i class="bi bi-file-earmark-plus"></i> Cadastros</span>
            <i class="bi bi-chevron-down"></i>
        </button>
        <div class="submenu show" id="submenuCadastros">
            <a href="/clientes" class="active"><i class="bi bi-person"></i> Clientes</a>
            <a href="#produtos"><i class="bi bi-box"></i> Produtos</a>
            <a href="#fornecedor"><i class="bi bi-shop"></i> Fornecedor</a>
            <a href="#contratos"><i class="bi bi-file-text"></i> Contratos</a>
        </div>
        
        <a href="/docs" target="_blank"><i class="bi bi-book"></i> API Docs</a>
    </div>

    <!-- Conteudo Principal -->
    <div class="main-content">
        <div class="container-fluid">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Clientes</h1>
                <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#modalCadastroCliente">Novo Cliente</button>
            </div>

            <!-- Area de Busca -->
            <div class="search-box">
                <div class="input-group">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input type="text" class="form-control" id="inputBusca" placeholder="Buscar por nome, email, telefone ou CPF...">
                    <button class="btn btn-outline-secondary" type="button" id="btnLimpar">Limpar</button>
                </div>
                <small class="text-muted" id="resultadoBusca"></small>
            </div>

            <div class="table-responsive">
                <table class="table table-striped" id="tabelaClientes">
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
                    <tbody id="corpoTabela">
                        {% for cliente in clientes %}
                        <tr class="linha-cliente">
                            <td class="coluna-id">{{ cliente.id }}</td>
                            <td class="coluna-nome">{{ cliente.nome }}</td>
                            <td class="coluna-email">{{ cliente.email }}</td>
                            <td class="coluna-telefone">{{ cliente.telefone }}</td>
                            <td class="coluna-cpf">{{ cliente.cpf }}</td>
                            <td class="coluna-endereco">{{ cliente.endereco }}</td>
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
        function toggleSubmenu(button) {
            const submenu = document.getElementById('submenuCadastros');
            const chevron = button.querySelector('i:last-child');
            
            submenu.classList.toggle('show');
            chevron.classList.toggle('bi-chevron-down');
            chevron.classList.toggle('bi-chevron-up');
        }

        // Funcionalidade de Busca
        const inputBusca = document.getElementById('inputBusca');
        const btnLimpar = document.getElementById('btnLimpar');
        const corpoTabela = document.getElementById('corpoTabela');
        const resultadoBusca = document.getElementById('resultadoBusca');

        inputBusca.addEventListener('keyup', function() {
            const termoBusca = this.value.toLowerCase();
            const linhas = corpoTabela.querySelectorAll('.linha-cliente');
            let contagem = 0;

            linhas.forEach(linha => {
                const nome = linha.querySelector('.coluna-nome').textContent.toLowerCase();
                const email = linha.querySelector('.coluna-email').textContent.toLowerCase();
                const telefone = linha.querySelector('.coluna-telefone').textContent.toLowerCase();
                const cpf = linha.querySelector('.coluna-cpf').textContent.toLowerCase();

                if (nome.includes(termoBusca) || email.includes(termoBusca) || 
                    telefone.includes(termoBusca) || cpf.includes(termoBusca)) {
                    linha.style.display = '';
                    contagem++;
                } else {
                    linha.style.display = 'none';
                }
            });

            if (termoBusca.length > 0) {
                resultadoBusca.textContent = `Encontrado ${contagem} cliente(s)`;
            } else {
                resultadoBusca.textContent = '';
            }
        });

        btnLimpar.addEventListener('click', function() {
            inputBusca.value = '';
            corpoTabela.querySelectorAll('.linha-cliente').forEach(linha => {
                linha.style.display = '';
            });
            resultadoBusca.textContent = '';
            inputBusca.focus();
        });

        // Cadastro de Cliente
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
print("   - Area de busca adicionada")
print("   - Filtro em tempo real por nome, email, telefone ou CPF")
print("   - Botao Limpar para resetar a busca")
