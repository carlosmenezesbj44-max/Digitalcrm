#!/usr/bin/env python3

clientes_html = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clientes - CRM Provedor</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">CRM Provedor</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link active" href="/clientes">Clientes</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>Clientes</h1>
            <a href="/clientes/novo" class="btn btn-success">Novo Cliente</a>
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
                        <th>Endereço</th>
                        <th>Data Cadastro</th>
                        <th>Ações</th>
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

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

with open('interfaces/web/templates/clientes.html', 'w', encoding='utf-8') as f:
    f.write(clientes_html)

print("Arquivo clientes.html atualizado - botão removido target='_blank'!")
