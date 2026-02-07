"""
Dashboard UI - Serve HTML com interface visual
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Executivo - CRM Provedor</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        
        /* Navbar */
        nav {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 60px;
        }
        
        .nav-brand {
            color: white;
            font-size: 20px;
            font-weight: bold;
        }
        
        .nav-links {
            display: flex;
            gap: 0;
            list-style: none;
        }
        
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 20px 15px;
            display: block;
            transition: background 0.3s;
        }
        
        .nav-links a:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .nav-links a.active {
            background: rgba(255,255,255,0.3);
            border-bottom: 3px solid white;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 5px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .kpi-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
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
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .kpi-change {
            font-size: 12px;
            color: #27ae60;
        }
        
        .kpi-change.down {
            color: #e74c3c;
        }
        
        .charts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
            height: 400px;
        }
        
        .chart-container h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .chart-wrapper {
            position: relative;
            height: calc(100% - 40px);
        }
        
        canvas {
            max-height: 350px;
        }
        
        .loading {
            color: #667eea;
            text-align: center;
            padding: 20px;
        }
        
        .error {
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .success {
            background: #27ae60;
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav>
        <div class="nav-container">
            <div class="nav-brand">CRM Provedor</div>
            <ul class="nav-links">
                <li><a href="/" class="active">Dashboard</a></li>
                <li><a href="/docs">API Docs</a></li>
                <li><a href="/redoc">ReDoc</a></li>
            </ul>
        </div>
    </nav>
    
    <div class="container">
        <header>
            <h1>Dashboard Executivo</h1>
            <p class="subtitle">CRM Provedor - Visão Geral de KPIs e Métricas</p>
        </header>
        
        <!-- KPIs -->
        <div class="kpi-grid" id="kpiContainer">
            <div class="loading">Carregando KPIs...</div>
        </div>
        
        <!-- Charts -->
        <div class="charts-grid">
            <div class="chart-container">
                <h3>Receita (Últimos 30 dias)</h3>
                <div class="chart-wrapper">
                    <canvas id="revenueChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Crescimento de Clientes</h3>
                <div class="chart-wrapper">
                    <canvas id="clientsChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Ordens por Status</h3>
                <div class="chart-wrapper">
                    <canvas id="ordersChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Contratos por Status</h3>
                <div class="chart-wrapper">
                    <canvas id="contractsChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Tickets de Suporte</h3>
                <div class="chart-wrapper">
                    <canvas id="ticketsChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Top Clientes</h3>
                <div class="chart-wrapper">
                    <canvas id="topClientsChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const API_BASE = '/api/v1/dashboard';
        let charts = {};
        
        // Dados de exemplo (fallback)
        const MOCK_DATA = {
            summary: {
                total_clients: 150,
                active_contracts: 120,
                monthly_revenue: 50000,
                pending_orders: 25,
                support_tickets_open: 12,
                system_uptime_percentage: 99.5,
                client_growth_percentage: 5.2,
                net_revenue: 37500
            },
            revenue: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Receita',
                    data: [10000, 12000, 15000, 14000, 18000, 20000],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)'
                }]
            },
            clients: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                datasets: [{
                    label: 'Novos Clientes',
                    data: [5, 8, 12, 10, 15, 18],
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)'
                }]
            },
            orders: {
                labels: ['Pendente', 'Em Progresso', 'Concluído', 'Cancelado'],
                datasets: [{
                    label: 'Ordens',
                    data: [25, 40, 120, 8],
                    backgroundColor: ['#e74c3c', '#f39c12', '#2ecc71', '#95a5a6']
                }]
            },
            contracts: {
                labels: ['Ativo', 'Pendente', 'Cancelado', 'Expirado'],
                datasets: [{
                    label: 'Contratos',
                    data: [120, 15, 5, 10],
                    backgroundColor: ['#2ecc71', '#3498db', '#e74c3c', '#95a5a6']
                }]
            },
            tickets: {
                labels: ['Aberto', 'Em Andamento', 'Fechado', 'Pendente'],
                datasets: [{
                    label: 'Tickets',
                    data: [12, 8, 45, 5],
                    backgroundColor: ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
                }]
            },
            topClients: {
                labels: ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
                datasets: [{
                    label: 'Receita',
                    data: [8000, 7000, 6500, 5000, 4500],
                    backgroundColor: '#667eea'
                }]
            }
        };
        
        // Função auxiliar para fazer requisições
        async function fetchAPI(endpoint) {
            try {
                // Temporariamente sem autenticação para debug
                const response = await fetch(API_BASE + endpoint);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                const data = await response.json();
                if (data && Object.keys(data).length > 0) {
                    return data;
                }
                return null;
            } catch (error) {
                console.error(`Erro ao buscar ${endpoint}:`, error);
                return null;
            }
        }
        
        // Carregar resumo executivo (KPIs)
        async function loadExecutiveSummary() {
            let data = await fetchAPI('/executive-summary');
            
            if (!data) {
                data = MOCK_DATA.summary;
            }
            
            const html = `
                <div class="kpi-card">
                    <div class="kpi-label">Total Clientes</div>
                    <div class="kpi-value">${data.total_clients || 0}</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Contratos Ativos</div>
                    <div class="kpi-value">${data.active_contracts || 0}</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Receita do Mês</div>
                    <div class="kpi-value">R$ ${(data.monthly_revenue || 0).toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',')}</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Pedidos Pendentes</div>
                    <div class="kpi-value">${data.pending_orders || 0}</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Tickets Abertos</div>
                    <div class="kpi-value">${data.support_tickets_open || 0}</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Uptime Sistema</div>
                    <div class="kpi-value">${(data.system_uptime_percentage || 0).toFixed(1)}%</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Crescimento Clientes</div>
                    <div class="kpi-value">${(data.client_growth_percentage || 0).toFixed(1)}%</div>
                </div>
                
                <div class="kpi-card">
                    <div class="kpi-label">Receita Líquida</div>
                    <div class="kpi-value">R$ ${(data.net_revenue || 0).toFixed(0).replace(/\\B(?=(\\d{3})+(?!\\d))/g, ',')}</div>
                </div>
            `;
            
            document.getElementById('kpiContainer').innerHTML = html;
        }
        
        // Carregar e desenhar gráfico
        async function loadChart(endpoint, chartId, type, mockKey) {
            let data = await fetchAPI(endpoint);
            
            if (!data || !data.labels) {
                data = MOCK_DATA[mockKey];
                if (!data) return;
            }
            
            const ctx = document.getElementById(chartId).getContext('2d');
            
            // Destruir gráfico anterior se existe
            if (charts[chartId]) {
                charts[chartId].destroy();
            }
            
            // Cores padrão
            const colors = [
                '#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe',
                '#43e97b', '#fa709a', '#fee140', '#30cfd0', '#330867'
            ];
            
            // Criar novo gráfico
            charts[chartId] = new Chart(ctx, {
                type: type || 'line',
                data: {
                    labels: data.labels,
                    datasets: data.datasets.map((dataset, idx) => ({
                        ...dataset,
                        backgroundColor: dataset.backgroundColor || colors[idx % colors.length],
                        borderColor: dataset.borderColor || colors[idx % colors.length],
                        borderWidth: 2,
                        fill: false,
                        tension: 0.4
                    }))
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Inicializar dashboard
        async function initDashboard() {
            await loadExecutiveSummary();
            await loadChart('/charts/revenue?days=30', 'revenueChart', 'line', 'revenue');
            await loadChart('/charts/clients?days=30', 'clientsChart', 'line', 'clients');
            await loadChart('/charts/orders-status', 'ordersChart', 'doughnut', 'orders');
            await loadChart('/charts/contracts-status', 'contractsChart', 'doughnut', 'contracts');
            await loadChart('/charts/support-tickets', 'ticketsChart', 'pie', 'tickets');
            await loadChart('/charts/top-clients?limit=10', 'topClientsChart', 'bar', 'topClients');
        }
        
        // Carregar ao abrir a página
        initDashboard();
        
        // Recarregar a cada 5 minutos
        setInterval(initDashboard, 5 * 60 * 1000);
    </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
def dashboard_page():
    """Serve dashboard page"""
    return DASHBOARD_HTML
