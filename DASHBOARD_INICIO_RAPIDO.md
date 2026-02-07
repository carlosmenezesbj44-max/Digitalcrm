# Dashboard Executivo - Início Rápido

## Instalação em 5 passos

### 1. Rodar Migrations do Banco de Dados

```bash
alembic upgrade head
```

Ou manualmente execute o script de setup:

```bash
python setup_dashboard.py
```

### 2. Adicionar Rotas na API

Edite `interfaces/api/main.py` e adicione:

```python
from interfaces.api.routes_dashboard import router as dashboard_router

# ... existing code ...

app.include_router(dashboard_router)
```

Arquivo completo deverá ficar assim:

```python
from fastapi import FastAPI
import logging
from interfaces.api.routes_dashboard import router as dashboard_router

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="CRM Provedor", version="1.0.0")

# Include routers
app.include_router(dashboard_router)

@app.get("/")
def read_root():
    print("Handling root request")
    return "CRM Provedor API" 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3. Inicializar Dashboard Padrão

```bash
python -c "
from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

db = SessionLocal()
service = DashboardService(db)
service.initialize_default_dashboard()
db.close()
print('Dashboard initialized!')
"
```

Ou via HTTP request após iniciar a API:

```bash
curl -X POST http://localhost:8000/api/v1/dashboard/initialize
```

### 4. Iniciar a API

```bash
python -m uvicorn interfaces.api.main:app --reload
```

Saída esperada:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 5. Testar os Endpoints

#### Resumo Executivo
```bash
curl http://localhost:8000/api/v1/dashboard/executive-summary
```

**Resposta:**
```json
{
  "total_clients": 0,
  "active_contracts": 0,
  "monthly_revenue": 0.0,
  "pending_orders": 0,
  "support_tickets_open": 0,
  "system_uptime_percentage": 99.5,
  "revenue_trend": "up",
  "client_growth_percentage": 0.0,
  "net_revenue": 0.0,
  "avg_ticket_value": 0.0
}
```

#### Gráfico de Receita
```bash
curl http://localhost:8000/api/v1/dashboard/charts/revenue?days=30
```

#### Gráfico de Clientes
```bash
curl http://localhost:8000/api/v1/dashboard/charts/clients?days=30
```

#### Status Pedidos
```bash
curl http://localhost:8000/api/v1/dashboard/charts/orders-status
```

#### Top Clientes
```bash
curl http://localhost:8000/api/v1/dashboard/charts/top-clients?limit=10
```

#### Tickets Suporte
```bash
curl http://localhost:8000/api/v1/dashboard/charts/support-tickets
```

#### Status Contratos
```bash
curl http://localhost:8000/api/v1/dashboard/charts/contracts-status
```

## Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/v1/dashboard/executive-summary` | Resumo executivo com KPIs |
| GET | `/api/v1/dashboard/charts/revenue` | Gráfico de receita |
| GET | `/api/v1/dashboard/charts/clients` | Gráfico de clientes |
| GET | `/api/v1/dashboard/charts/orders-status` | Ordens por status |
| GET | `/api/v1/dashboard/charts/top-clients` | Top clientes |
| GET | `/api/v1/dashboard/charts/support-tickets` | Tickets por status |
| GET | `/api/v1/dashboard/charts/contracts-status` | Contratos por status |
| POST | `/api/v1/dashboard/initialize` | Inicializar dashboard padrão |
| POST | `/api/v1/dashboard/metrics/record` | Registrar métricas diárias |

## Estrutura de Dados

### Executive Summary (Resumo Executivo)

```json
{
  "total_clients": 150,
  "active_contracts": 120,
  "monthly_revenue": 50000.0,
  "pending_orders": 25,
  "support_tickets_open": 12,
  "system_uptime_percentage": 99.5,
  "revenue_trend": "up",
  "client_growth_percentage": 5.2,
  "net_revenue": 37500.0,
  "avg_ticket_value": 1666.67
}
```

### Chart Response (Resposta de Gráfico)

```json
{
  "labels": ["2024-01-01", "2024-01-02", ...],
  "datasets": [
    {
      "label": "Receita Diária",
      "data": [1000, 1500, 1200, ...],
      "borderColor": "#2ecc71",
      "backgroundColor": "rgba(46, 204, 113, 0.1)"
    }
  ],
  "title": "Receita dos Últimos 30 Dias",
  "type": "line"
}
```

## Visualização Frontend

### Exemplo com React + Chart.js

```jsx
import React, { useEffect, useState } from 'react';
import { Line, Doughnut, Bar, Pie } from 'react-chartjs-2';

export function DashboardPage() {
  const [executive, setExecutive] = useState(null);
  const [revenueChart, setRevenueChart] = useState(null);

  useEffect(() => {
    // Fetch executive summary
    fetch('/api/v1/dashboard/executive-summary')
      .then(r => r.json())
      .then(data => setExecutive(data));

    // Fetch revenue chart
    fetch('/api/v1/dashboard/charts/revenue?days=30')
      .then(r => r.json())
      .then(data => setRevenueChart(data));
  }, []);

  if (!executive || !revenueChart) return <div>Carregando...</div>;

  return (
    <div className="dashboard">
      <h1>Dashboard Executivo</h1>
      
      {/* KPI Cards */}
      <div className="kpi-grid">
        <KPICard label="Total Clientes" value={executive.total_clients} />
        <KPICard label="Receita do Mês" value={`R$ ${executive.monthly_revenue.toFixed(2)}`} />
        <KPICard label="Contratos Ativos" value={executive.active_contracts} />
        <KPICard label="Tickets Abertos" value={executive.support_tickets_open} />
      </div>

      {/* Charts */}
      <div className="charts">
        <div className="chart-container">
          <Line 
            data={{
              labels: revenueChart.labels,
              datasets: revenueChart.datasets
            }}
            options={{ responsive: true }}
          />
        </div>
      </div>
    </div>
  );
}

function KPICard({ label, value }) {
  return (
    <div className="kpi-card">
      <p className="kpi-label">{label}</p>
      <p className="kpi-value">{value}</p>
    </div>
  );
}
```

### Exemplo com Vue.js

```vue
<template>
  <div class="dashboard">
    <h1>Dashboard Executivo</h1>
    
    <!-- KPI Cards -->
    <div class="kpi-grid">
      <kpi-card label="Total Clientes" :value="executive.total_clients" />
      <kpi-card label="Receita do Mês" :value="`R$ ${executive.monthly_revenue.toFixed(2)}`" />
      <kpi-card label="Contratos Ativos" :value="executive.active_contracts" />
    </div>

    <!-- Charts -->
    <div class="charts">
      <line-chart :data="revenueChartData" />
      <doughnut-chart :data="ordersChartData" />
      <bar-chart :data="topClientsData" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      executive: {},
      revenueChartData: {},
      ordersChartData: {},
      topClientsData: {}
    };
  },
  mounted() {
    this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      const executive = await fetch('/api/v1/dashboard/executive-summary').then(r => r.json());
      const revenue = await fetch('/api/v1/dashboard/charts/revenue').then(r => r.json());
      const orders = await fetch('/api/v1/dashboard/charts/orders-status').then(r => r.json());
      const topClients = await fetch('/api/v1/dashboard/charts/top-clients').then(r => r.json());

      this.executive = executive;
      this.revenueChartData = revenue;
      this.ordersChartData = orders;
      this.topClientsData = topClients;
    }
  }
};
</script>
```

## Configuração de Agendamento (Opcional)

Para registrar métricas automaticamente a cada dia:

### Com APScheduler

```bash
pip install apscheduler
```

Edite `interfaces/api/main.py`:

```python
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from crm_modules.dashboard.service import DashboardService
from crm_core.db.base import SessionLocal

app = FastAPI(title="CRM Provedor", version="1.0.0")

def record_metrics():
    db = SessionLocal()
    try:
        service = DashboardService(db)
        service.record_daily_metrics()
        print("Daily metrics recorded")
    finally:
        db.close()

# Setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(record_metrics, 'cron', hour=0, minute=0)
scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
```

## Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'crm_modules.dashboard'"

Certifique-se de que:
1. O diretório `crm_modules/dashboard/` foi criado
2. O arquivo `crm_modules/dashboard/__init__.py` existe
3. Você está na raiz do projeto ao rodar os scripts

### Erro: "Dashboard not found"

Execute a inicialização:
```bash
curl -X POST http://localhost:8000/api/v1/dashboard/initialize
```

### Dados vazios nos gráficos

Os gráficos retornam dados vazios quando não há registros na tabela. Isso é esperado em uma instalação nova. Os dados aparecerão quando:
- Clientes forem criados
- Contratos forem registrados
- Pedidos forem gerados
- Faturas forem emitidas

## Documentação Completa

Para detalhes completos sobre models, schemas, endpoints e segurança, consulte:
**DASHBOARD_IMPLEMENTACAO.md**

## Proximos Passos

1. ✓ Implementar Dashboard Executivo (CONCLUÍDO)
2. ⬜ Implementar Sistema de Roles e Permissões
3. ⬜ Implementar Módulo de Faturamento (melhorias)

---

**Status:** ✓ Pronto para Produção
**Último Update:** 2024-01-18
