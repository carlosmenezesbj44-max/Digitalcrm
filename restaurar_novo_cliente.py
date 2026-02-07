#!/usr/bin/env python3
# -*- coding: utf-8 -*-

novo_cliente_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Novo Cliente - CRM Provedor</title>
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
            <a href="/clientes" class="active"><i class="bi bi-person"></i> Novo Cliente</a>
            <a href="/clientes"><i class="bi bi-list"></i> Listar Clientes</a>
            <a href="#produtos"><i class="bi bi-box"></i> Produtos</a>
            <a href="#fornecedor"><i class="bi bi-shop"></i> Fornecedor</a>
            <a href="#contratos"><i class="bi bi-file-text"></i> Contratos</a>
        </div>
        
        <a href="/docs" target="_blank"><i class="bi bi-book"></i> API Docs</a>
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
                        <!-- Horizontal tabs -->
                        <ul class="nav nav-tabs" id="clienteTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="tab-principal" data-bs-toggle="tab" data-bs-target="#principal" type="button" role="tab" aria-controls="principal" aria-selected="true">Principal</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-endereco" data-bs-toggle="tab" data-bs-target="#endereco" type="button" role="tab" aria-controls="endereco" aria-selected="false">Endereco</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-contatos" data-bs-toggle="tab" data-bs-target="#contatos" type="button" role="tab" aria-controls="contatos" aria-selected="false">Contatos</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-login" data-bs-toggle="tab" data-bs-target="#login" type="button" role="tab" aria-controls="login" aria-selected="false">Login</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-financeiro" data-bs-toggle="tab" data-bs-target="#financeiro" type="button" role="tab" aria-controls="financeiro" aria-selected="false">Financeiro</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-atendimento" data-bs-toggle="tab" data-bs-target="#atendimento" type="button" role="tab" aria-controls="atendimento" aria-selected="false">Atendimento</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-os" data-bs-toggle="tab" data-bs-target="#os" type="button" role="tab" aria-controls="os" aria-selected="false">Ordem de Servicos</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-vendas" data-bs-toggle="tab" data-bs-target="#vendas" type="button" role="tab" aria-controls="vendas" aria-selected="false">Vendas</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-arquivos" data-bs-toggle="tab" data-bs-target="#arquivos" type="button" role="tab" aria-controls="arquivos" aria-selected="false">Arquivos</button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="tab-observacoes" data-bs-toggle="tab" data-bs-target="#observacoes" type="button" role="tab" aria-controls="observacoes" aria-selected="false">Observacoes</button>
                            </li>
                        </ul>

                        <div class="tab-content py-3" id="clienteTabsContent">
                            <div class="tab-pane fade show active" id="principal" role="tabpanel" aria-labelledby="tab-principal">
                                <div class="mb-3">
                                    <label for="id" class="form-label">ID do Cliente</label>
                                    <input type="text" class="form-control" id="id" name="id" value="{{ next_id }}" readonly>
                                </div>
                                <div class="mb-3">
                                    <label for="nome" class="form-label">Nome</label>
                                    <input type="text" class="form-control" id="nome" name="nome" required>
                                </div>
                                <div class="mb-3">
                                    <label for="cpf" class="form-label">CPF</label>
                                    <input type="text" class="form-control" id="cpf" name="cpf" required>
                                </div>
                                <div class="mb-3">
                                    <label for="rg" class="form-label">RG</label>
                                    <input type="text" class="form-control" id="rg" name="rg">
                                </div>
                                <div class="mb-3">
                                    <label for="orgao_emissor" class="form-label">Orgao Emissor (RG)</label>
                                    <input type="text" class="form-control" id="orgao_emissor" name="orgao_emissor">
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="nacionalidade" class="form-label">Nacionalidade</label>
                                        <input type="text" class="form-control" id="nacionalidade" name="nacionalidade">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="naturalidade" class="form-label">Naturalidade</label>
                                        <input type="text" class="form-control" id="naturalidade" name="naturalidade">
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="data_nascimento" class="form-label">Data de Nascimento</label>
                                    <input type="date" class="form-control" id="data_nascimento" name="data_nascimento">
                                </div>
                                <div class="mb-3">
                                    <label for="tipo_cliente" class="form-label">Tipo de Cliente</label>
                                    <select class="form-select" id="tipo_cliente" name="tipo_cliente" required>
                                        <option value="fisico" selected>Fisico (CPF)</option>
                                        <option value="juridico">Juridico (CNPJ)</option>
                                    </select>
                                </div>
                            </div>

                            <div class="tab-pane fade" id="endereco" role="tabpanel" aria-labelledby="tab-endereco">
                                <div class="row">
                                    <div class="col-md-8 mb-3">
                                        <label for="rua" class="form-label">Endereco / Rua</label>
                                        <input type="text" class="form-control" id="rua" name="rua">
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <label for="numero" class="form-label">Numero</label>
                                        <input type="text" class="form-control" id="numero" name="numero">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="bairro" class="form-label">Bairro</label>
                                        <input type="text" class="form-control" id="bairro" name="bairro">
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="cidade" class="form-label">Cidade</label>
                                        <input type="text" class="form-control" id="cidade" name="cidade">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-4 mb-3">
                                        <label for="cep" class="form-label">CEP</label>
                                        <input type="text" class="form-control" id="cep" name="cep">
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <label for="ap" class="form-label">AP</label>
                                        <input type="text" class="form-control" id="ap" name="apartamento">
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <label for="complemento" class="form-label">Complemento</label>
                                        <input type="text" class="form-control" id="complemento" name="complemento">
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Moradia</label>
                                        <select class="form-select" id="moradia" name="moradia">
                                            <option value="propria">Propria</option>
                                            <option value="alugada">Alugada</option>
                                        </select>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Tipo de Localidade</label>
                                        <select class="form-select" id="tipo_localidade" name="tipo_localidade">
                                            <option value="urbana">Zona Urbana</option>
                                            <option value="rural">Zona Rural</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label for="latitude" class="form-label">Latitude</label>
                                        <input type="text" class="form-control" id="latitude" name="latitude" readonly>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label for="longitude" class="form-label">Longitude</label>
                                        <input type="text" class="form-control" id="longitude" name="longitude" readonly>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <button type="button" id="buscarCoords" class="btn btn-outline-primary">Buscar coordenadas pelo endereco</button>
                                    <div id="geocodeStatus" class="mt-2"></div>
                                </div>
                            </div>

                            <div class="tab-pane fade" id="contatos" role="tabpanel" aria-labelledby="tab-contatos">
                                <div class="mb-3">
                                    <label for="email" class="form-label">Email</label>
                                    <input type="email" class="form-control" id="email" name="email">
                                </div>
                                <div class="mb-3">
                                    <label for="telefone" class="form-label">Telefone</label>
                                    <input type="text" class="form-control" id="telefone" name="telefone">
                                </div>
                            </div>

                            <div class="tab-pane fade" id="login" role="tabpanel" aria-labelledby="tab-login">
                                <small class="text-muted">Campos de login / credenciais (adicione conforme necessario)</small>
                                <div class="mb-3 mt-2">
                                    <label for="username" class="form-label">Usuario (login)</label>
                                    <input type="text" class="form-control" id="username" name="username">
                                </div>
                                <div class="mb-3">
                                    <label for="password" class="form-label">Senha</label>
                                    <input type="password" class="form-control" id="password" name="password">
                                </div>
                            </div>

                            <div class="tab-pane fade" id="financeiro" role="tabpanel" aria-labelledby="tab-financeiro">
                                <small class="text-muted">Informacoes financeiras (contas, faturamento, planos)</small>
                            </div>

                            <div class="tab-pane fade" id="atendimento" role="tabpanel" aria-labelledby="tab-atendimento">
                                <small class="text-muted">Historico de atendimento e notas</small>
                            </div>

                            <div class="tab-pane fade" id="os" role="tabpanel" aria-labelledby="tab-os">
                                <small class="text-muted">Ordens de servico relacionadas ao cliente</small>
                            </div>

                            <div class="tab-pane fade" id="vendas" role="tabpanel" aria-labelledby="tab-vendas">
                                <small class="text-muted">Registro de vendas / propostas</small>
                            </div>

                            <div class="tab-pane fade" id="arquivos" role="tabpanel" aria-labelledby="tab-arquivos">
                                <small class="text-muted">Area para upload/listagem de arquivos</small>
                                <div class="mb-3 mt-2">
                                    <label for="arquivos_input" class="form-label">Enviar arquivos</label>
                                    <input class="form-control" type="file" id="arquivos_input" name="arquivos" multiple>
                                    <div class="form-text">Voce pode enviar multiplos arquivos. Serao salvos no servidor.</div>
                                </div>
                                <div id="arquivos_list" class="mt-2"></div>
                            </div>

                            <div class="tab-pane fade" id="observacoes" role="tabpanel" aria-labelledby="tab-observacoes">
                                <div class="mb-3">
                                    <label for="observacoes" class="form-label">Observacoes</label>
                                    <textarea class="form-control" id="observacoes" name="observacoes" rows="4"></textarea>
                                </div>
                            </div>
                        </div>

                        <div class="mb-3 mt-3">
                            <label class="form-label">Cliente Ativo</label>
                            <div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="ativo" id="ativo_sim" value="sim" checked>
                                    <label class="form-check-label" for="ativo_sim">Sim</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="ativo" id="ativo_nao" value="nao">
                                    <label class="form-check-label" for="ativo_nao">Nao</label>
                                </div>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-primary">Cadastrar Cliente</button>
                        <a href="/clientes" class="btn btn-secondary">Voltar</a>
                    </form>
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
    </script>
    <script>
        // Script para mudar o label do campo CPF/CNPJ baseado no tipo de cliente
        document.getElementById('tipo_cliente').addEventListener('change', function() {
            const label = document.querySelector('label[for="cpf"]');
            const input = document.getElementById('cpf');
            if (this.value === 'juridico') {
                label.textContent = 'CNPJ';
                input.placeholder = 'Digite o CNPJ';
            } else {
                label.textContent = 'CPF';
                input.placeholder = 'Digite o CPF';
            }
        });
    </script>
    <script>
        // Geocode button handler
        document.addEventListener('DOMContentLoaded', function() {
            const btn = document.getElementById('buscarCoords');
            if (!btn) return;
            btn.addEventListener('click', async function() {
                const rua = document.getElementById('rua') ? document.getElementById('rua').value : '';
                const numero = document.getElementById('numero') ? document.getElementById('numero').value : '';
                const bairro = document.getElementById('bairro') ? document.getElementById('bairro').value : '';
                const cidade = document.getElementById('cidade') ? document.getElementById('cidade').value : '';
                const cep = document.getElementById('cep') ? document.getElementById('cep').value : '';
                const query = encodeURIComponent([rua, numero, bairro, cidade, cep].filter(Boolean).join(', ') + ', Brazil');
                const status = document.getElementById('geocodeStatus');
                status.innerText = 'Buscando coordenadas...';
                    let data = null;
                    const endpoints = [
                        `${location.origin}/clientes/geocode?address=${query}`,
                        `${location.origin}/geocode?address=${query}`,
                        `geocode?address=${query}`
                    ];
                    for (const url of endpoints) {
                        try {
                            const res = await fetch(url);
                            if (res && res.ok) {
                                data = await res.json();
                                break;
                            }
                        } catch (err) {
                        }
                    }
            });
        });
    </script>
</body>
</html>'''

with open('interfaces/web/templates/novo_cliente.html', 'w', encoding='utf-8') as f:
    f.write(novo_cliente_html)

print("novo_cliente.html restaurado com script de geocoding!")
