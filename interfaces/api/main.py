from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
import os
from interfaces.api.routes_dashboard import router as dashboard_router
from interfaces.api.dashboard_ui import router as dashboard_ui_router
from interfaces.api.routers import api_router
from crm_modules.faturamento.api import router as faturamento_router
from crm_modules.faturamento.carne_api import router as carne_router
from crm_modules.dashboard.api import router as dashboard_api_router
from crm_modules.clientes.api import router as clientes_router
from crm_modules.usuarios.api import router as usuarios_router
from crm_modules.configuracoes.api import router as configuracoes_router
from crm_modules.contratos.api import router as contratos_router
from crm_modules.mikrotik.api import router as mikrotik_router
from crm_modules.servidores.api import router as servidores_router
from interfaces.web.app import app as web_app

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="CRM Provedor", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="interfaces/web/templates")

# Include all API routers before mounting the web app
app.include_router(dashboard_router)
app.include_router(dashboard_ui_router, prefix="/dashboard")
app.include_router(dashboard_api_router)
app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")
app.include_router(faturamento_router, prefix="/api/v1/faturamento")
app.include_router(carne_router, prefix="/api/v1/faturamento")
app.include_router(contratos_router)
app.include_router(mikrotik_router, prefix="/api/v1")
app.include_router(configuracoes_router)
app.mount("/", web_app)


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Retorna o dashboard com menu integrado"""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - CRM Provedor</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {
                display: flex;
                min-height: 100vh;
                background: #f5f7fa;
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
                padding: 30px;
            }
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .kpi-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 4px solid #667eea;
            }
            .kpi-label {
                color: #666;
                font-size: 12px;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            .kpi-value {
                color: #333;
                font-size: 24px;
                font-weight: bold;
            }
            .charts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
            }
            .chart-container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                height: 350px;
            }
            .chart-container h3 {
                color: #333;
                margin-bottom: 15px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <!-- Sidebar -->
        <div class="sidebar">
            <h4>CRM Provedor</h4>
            <a href="/" class="active"><i class="bi bi-house"></i> Home</a>
            
            <!-- Cadastros -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-file-earmark-plus"></i> Cadastros</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu" id="submenuCadastros">
                <a href="/clientes/novo"><i class="bi bi-person"></i> Novo Cliente</a>
                <a href="/clientes"><i class="bi bi-list"></i> Listar Clientes</a>
                <a href="/tecnicos/novo"><i class="bi bi-hammer"></i> Novo Técnico</a>
                <a href="/tecnicos"><i class="bi bi-list"></i> Listar Técnicos</a>
            </div>

            <!-- Usuários -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-people"></i> Usuários</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu" id="submenuUsuarios">
                <a href="/usuarios"><i class="bi bi-person-gear"></i> Gerenciar Usuários</a>
                <a href="/login" onclick="logout()"><i class="bi bi-box-arrow-right"></i> Logout</a>
            </div>

            <!-- Produtos -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-box"></i> Produtos</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu show" id="submenuProdutos">
                <a href="/produtos/novo"><i class="bi bi-plus-circle"></i> Novo Produto</a>
                <a href="/produtos"><i class="bi bi-list"></i> Listar Produtos</a>
            </div>

            <!-- Planos -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-wifi"></i> Planos</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu show" id="submenuPlanos">
                <a href="/planos/novo"><i class="bi bi-plus-circle"></i> Novo Plano</a>
                <a href="/planos"><i class="bi bi-list"></i> Listar Planos</a>
            </div>

            <!-- Ordens de Serviço -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-clipboard-check"></i> Ordens de Serviço</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu" id="submenuOrdens">
                <a href="/ordens-servico/nova"><i class="bi bi-plus-circle"></i> Nova Ordem</a>
                <a href="/ordens-servico"><i class="bi bi-list"></i> Listar Ordens</a>
            </div>

            <!-- Provedor -->
            <button class="menu-toggle" onclick="toggleSubmenu(this)">
                <span><i class="bi bi-server"></i> Provedor</span>
                <i class="bi bi-chevron-down"></i>
            </button>
            <div class="submenu show" id="submenuProvedor">
                <a href="/servidores/novo"><i class="bi bi-plus-circle"></i> Novo Servidor</a>
                <a href="/servidores"><i class="bi bi-list"></i> Listar Servidores</a>
                <a href="/mikrotik/logs"><i class="bi bi-journal-text"></i> Logs Mikrotik</a>
                <a href="/mikrotik/sessions"><i class="bi bi-eye"></i> Sessões Mikrotik</a>
                <a href="/huawei/logs"><i class="bi bi-journal-text"></i> Logs Huawei</a>
                <a href="/huawei/sessions"><i class="bi bi-eye"></i> Sessões Huawei</a>
            </div>
            
            <a href="/docs" target="_blank"><i class="bi bi-book"></i> API Docs</a>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <h1>Dashboard Executivo</h1>
            <p style="color: #666; margin-bottom: 30px;">Visão geral de KPIs e métricas</p>

            <!-- KPIs -->
            <div class="kpi-grid" id="kpiContainer">
                <div class="alert alert-info">Carregando dados...</div>
            </div>

            <!-- Charts -->
            <div class="charts-grid">
                <div class="chart-container">
                    <h3>Receita</h3>
                    <canvas id="revenueChart"></canvas>
                </div>
                <div class="chart-container">
                    <h3>Ordens por Status</h3>
                    <canvas id="ordersChart"></canvas>
                </div>
            </div>
        </div>

        <script>
            // Remover hash da URL se existir
            if (window.location.hash) {
                window.history.replaceState({}, document.title, window.location.pathname + window.location.search);
            }

            function toggleSubmenu(button) {
                const submenu = button.nextElementSibling;
                const chevron = button.querySelector('i:last-child');
                
                submenu.classList.toggle('show');
                chevron.classList.toggle('bi-chevron-down');
                chevron.classList.toggle('bi-chevron-up');
            }

            function logout() {
                localStorage.removeItem('access_token');
                window.location.replace('/login');
            }



            async function loadData() {
                try {
                    // Get auth token
                    const token = localStorage.getItem('access_token');

                    // Load KPIs
                    const summaryResponse = await fetch('/api/dashboard/summary', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (summaryResponse.ok) {
                        const summary = await summaryResponse.json();
                        const html = `
                            <div class="kpi-card">
                                <div class="kpi-label">Total Clientes</div>
                                <div class="kpi-value">${summary.total_clients}</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-label">Contratos Ativos</div>
                                <div class="kpi-value">${summary.active_contracts}</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-label">Receita do Mês</div>
                                <div class="kpi-value">R$ ${summary.monthly_revenue.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
                            </div>
                            <div class="kpi-card">
                                <div class="kpi-label">Pedidos Pendentes</div>
                                <div class="kpi-value">${summary.pending_orders}</div>
                            </div>
                        `;
                        document.getElementById('kpiContainer').innerHTML = html;
                    } else {
                        document.getElementById('kpiContainer').innerHTML = '<div class="alert alert-warning">Erro ao carregar dados. Faça login novamente.</div>';
                    }

                    // Load revenue chart
                    const revenueResponse = await fetch('/api/dashboard/charts/revenue', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (revenueResponse.ok) {
                        const revenueData = await revenueResponse.json();
                        new Chart(document.getElementById('revenueChart'), {
                            type: 'line',
                            data: revenueData,
                            options: {responsive: true, maintainAspectRatio: false}
                        });
                    }

                    // Load orders chart
                    const ordersResponse = await fetch('/api/dashboard/charts/orders', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (ordersResponse.ok) {
                        const ordersData = await ordersResponse.json();
                        new Chart(document.getElementById('ordersChart'), {
                            type: 'doughnut',
                            data: ordersData,
                            options: {responsive: true, maintainAspectRatio: false}
                        });
                    }

                } catch (error) {
                    console.error('Erro ao carregar dados:', error);
                    document.getElementById('kpiContainer').innerHTML = '<div class="alert alert-danger">Erro ao carregar dados do dashboard.</div>';
                }
            }

            loadData();
        </script>
    </body>
    </html>
    """ 


# Rotas para páginas de Carnês e Boletos
@app.get("/carnes", response_class=HTMLResponse)
def pagina_carnes():
    """Página para gerenciar carnês"""
    template_path = os.path.join(os.path.dirname(__file__), "../web/templates/carnes.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <body style="display: flex; align-items: center; justify-content: center; height: 100vh; font-family: Arial;">
            <div style="text-align: center;">
                <h1>⚠️ Erro 404</h1>
                <p>Página de carnês não encontrada.</p>
                <p>Arquivo esperado em: {}</p>
                <a href="/">Voltar ao Dashboard</a>
            </div>
        </body>
        </html>
        """.format(template_path)

@app.get("/boletos", response_class=HTMLResponse)
def pagina_boletos():
    """Página para gerenciar boletos"""
    template_path = os.path.join(os.path.dirname(__file__), "../web/templates/boletos.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <body style="display: flex; align-items: center; justify-content: center; height: 100vh; font-family: Arial;">
            <div style="text-align: center;">
                <h1>⚠️ Erro 404</h1>
                <p>Página de boletos não encontrada.</p>
                <p>Arquivo esperado em: {}</p>
                <a href="/">Voltar ao Dashboard</a>
            </div>
        </body>
        </html>
        """.format(template_path)

@app.get("/configuracoes", response_class=HTMLResponse)
def pagina_configuracoes():
    """Página para gerenciar configurações"""
    template_path = os.path.join(os.path.dirname(__file__), "../web/templates/configuracoes.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <body style="display: flex; align-items: center; justify-content: center; height: 100vh; font-family: Arial;">
            <div style="text-align: center;">
                <h1>⚠️ Erro 404</h1>
                <p>Página de configurações não encontrada.</p>
                <p>Arquivo esperado em: {}</p>
                <a href="/">Voltar ao Dashboard</a>
            </div>
        </body>
        </html>
        """.format(template_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
