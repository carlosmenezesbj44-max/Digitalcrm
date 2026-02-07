# Dashboard Executivo - Implementação Completa

## Visão Geral

Sistema de Dashboard Executivo com KPIs, gráficos e estatísticas em tempo real para o CRM Provedor.

## Arquitetura

```
crm_modules/dashboard/
├── __init__.py          # Exports do módulo
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── repository.py        # Data access layer
└── service.py           # Business logic

interfaces/api/
└── routes_dashboard.py  # API endpoints
```

## Modelos de Dados

### Dashboard
- `id`: Identificador único
- `name`: Nome do dashboard
- `description`: Descrição
- `is_active`: Status ativo/inativo
- `created_at`, `updated_at`: Timestamps
- `kpis`: Relação com KPIs
- `widgets`: Relação com widgets

### DashboardKPI
- `id`: Identificador único
- `dashboard_id`: ID do dashboard
- `name`: Nome do KPI
- `metric_type`: Tipo de métrica (revenue, clients, orders, etc)
- `current_value`: Valor atual
- `previous_value`: Valor anterior
- `target_value`: Meta
- `unit`: Unidade (currency, percentage, count, hours)
- `trend`: Tendência (up, down, stable)
- `percentage_change`: Mudança percentual

### DashboardWidget
- `id`: Identificador único
- `dashboard_id`: ID do dashboard
- `widget_type`: Tipo (chart, kpi_card, table, gauge)
- `title`: Título do widget
- `position`: Ordem no dashboard
- `data_source`: Fonte de dados
- `is_visible`: Visibilidade
- `config`: Configuração JSON

### MetricHistory
- `id`: Identificador único
- `metric_type`: Tipo de métrica
- `value`: Valor
- `timestamp`: Data/hora do registro
- `period`: Período (daily, weekly, monthly)
- `metadata`: Dados adicionais (JSON)

## KPIs Implementados

### 1. Resumo Executivo (Executive Summary)
**Metricados:**
- Total de Clientes
- Contratos Ativos
- Receita do Mês
- Pedidos Pendentes
- Tickets de Suporte Abertos
- Uptime do Sistema
- Tendência de Receita
- Crescimento de Clientes (%)
- Receita Líquida
- Valor Médio por Ticket

### 2. Gráficos Disponíveis

#### Receita (Revenue Chart)
- Tipo: Line Chart
- Período: Últimos 30 dias (configurável)
- Dados: Receita diária
- Análise: Tendência de receita

#### Crescimento de Clientes
- Tipo: Line Chart
- Período: Últimos 30 dias
- Dados: Novos clientes por dia
- Análise: Taxa de crescimento

#### Ordens de Serviço por Status
- Tipo: Doughnut Chart
- Status: Pendente, Em Progresso, Concluído, Cancelado
- Análise: Distribuição de trabalho

#### Top Clientes (por Receita)
- Tipo: Bar Chart
- Limite: Top 10 (configurável)
- Análise: Clientes mais valiosos

#### Tickets de Suporte
- Tipo: Pie Chart
- Status: Aberto, Em Andamento, Fechado, Pendente
- Análise: Distribuição de tickets

#### Contratos por Status
- Tipo: Doughnut Chart
- Status: Ativo, Pendente, Cancelado, Expirado
- Análise: Saúde de contratos

## API Endpoints

### Resumo Executivo
```
GET /api/v1/dashboard/executive-summary
```
Retorna todas as métricas principais em um único endpoint.

**Response:**
```json
{
  "total_clients": 150,
  "active_contracts": 120,
  "monthly_revenue": 50000.00,
  "pending_orders": 25,
  "support_tickets_open": 12,
  "system_uptime_percentage": 99.5,
  "revenue_trend": "up",
  "client_growth_percentage": 5.2,
  "net_revenue": 37500.00,
  "avg_ticket_value": 1666.67
}
```

### Gráficos

#### Receita
```
GET /api/v1/dashboard/charts/revenue?days=30
```

#### Clientes
```
GET /api/v1/dashboard/charts/clients?days=30
```

#### Status Pedidos
```
GET /api/v1/dashboard/charts/orders-status
```

#### Top Clientes
```
GET /api/v1/dashboard/charts/top-clients?limit=10
```

#### Tickets Suporte
```
GET /api/v1/dashboard/charts/support-tickets
```

#### Status Contratos
```
GET /api/v1/dashboard/charts/contracts-status
```

### Gerenciamento de Dashboard

#### Listar Dashboards
```
GET /api/v1/dashboard?skip=0&limit=10
```

#### Obter Dashboard
```
GET /api/v1/dashboard/{dashboard_id}
```

#### Criar Dashboard
```
POST /api/v1/dashboard
Content-Type: application/json

{
  "name": "Nome Dashboard",
  "description": "Descrição",
  "is_active": true
}
```

#### Atualizar Dashboard
```
PUT /api/v1/dashboard/{dashboard_id}
Content-Type: application/json

{
  "name": "Novo Nome",
  "description": "Nova Descrição",
  "is_active": true
}
```

#### Deletar Dashboard
```
DELETE /api/v1/dashboard/{dashboard_id}
```

### Inicialização

#### Inicializar Dashboard Padrão
```
POST /api/v1/dashboard/initialize
```
Cria um dashboard padrão com todos os widgets recomendados.

#### Registrar Métricas Diárias
```
POST /api/v1/dashboard/metrics/record
```
Registra as métricas do dia para histórico.

## Instalação e Configuração

### 1. Criar Migrações de Banco de Dados

```bash
alembic revision --autogenerate -m "Add dashboard tables"
alembic upgrade head
```

### 2. Importar Rotas no Main App

Editar `interfaces/api/main.py`:

```python
from interfaces.api.routes_dashboard import router as dashboard_router

app.include_router(dashboard_router)
```

### 3. Inicializar Dashboard Padrão

```bash
python -c "
from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

db = SessionLocal()
service = DashboardService(db)
service.initialize_default_dashboard()
print('Dashboard initialized successfully!')
"
```

Ou via API:
```bash
curl -X POST http://localhost:8000/api/v1/dashboard/initialize
```

## Agendamento de Tarefas (Background Jobs)

Para registrar métricas diariamente, configure um scheduler (APScheduler ou Celery):

```python
from apscheduler.schedulers.background import BackgroundScheduler
from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

def record_daily_metrics():
    db = SessionLocal()
    service = DashboardService(db)
    service.record_daily_metrics()
    db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(record_daily_metrics, 'cron', hour=0, minute=0)
scheduler.start()
```

## Exemplo de Uso Frontend

### Com Chart.js (Frontend)

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<canvas id="revenueChart"></canvas>

<script>
async function loadRevenueChart() {
    const response = await fetch('/api/v1/dashboard/charts/revenue?days=30');
    const data = await response.json();
    
    new Chart(document.getElementById('revenueChart'), {
        type: data.type,
        data: {
            labels: data.labels,
            datasets: data.datasets
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: data.title
                }
            }
        }
    });
}

loadRevenueChart();
</script>
```

## Cache e Performance

Para grandes volumes de dados, implemente cache:

```python
from crm_core.cache import cache_key, get_cache, set_cache

def get_executive_summary_cached(db: Session):
    cache_key_str = "executive_summary"
    cached = get_cache(cache_key_str)
    
    if cached:
        return cached
    
    summary = DashboardService(db).get_executive_summary()
    set_cache(cache_key_str, summary, ttl=300)  # 5 minutos
    return summary
```

## Segurança e Permissões

Adicionar verificação de permissões nos endpoints:

```python
from crm_core.security import require_role

@router.get("/executive-summary")
@require_role("admin", "gerente")
def get_executive_summary(db: Session = Depends(get_db)):
    service = DashboardService(db)
    return service.get_executive_summary()
```

## Próximas Melhorias

1. **Alertas**: Configurar alertas quando KPIs atingem limites
2. **Comparações**: Comparar períodos diferentes
3. **Customização**: Permitir usuários customizar widgets
4. **Exportação**: Gerar relatórios em PDF/Excel
5. **Notificações**: Push/Email de KPIs críticos
6. **Integração**: Webhooks para integração com ferramentas externas
7. **Análise Preditiva**: ML para previsão de tendências
8. **Drill Down**: Clicar em gráficos para dados detalhados

## Troubleshooting

### Erro: "Dashboard not found"
Certifique-se de que rodou `initialize_default_dashboard()`

### Dados vazios nos gráficos
Verifique se há dados na tabela correspondente. Use:
```sql
SELECT COUNT(*) FROM faturas;
SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM ordens_servico;
```

### Performance lenta
Implemente índices no banco:
```sql
CREATE INDEX idx_fatura_data ON faturas(data_emissao);
CREATE INDEX idx_cliente_data ON clientes(data_criacao);
CREATE INDEX idx_ordem_status ON ordens_servico(status);
```

## Estrutura de Arquivos Criados

```
crm_modules/dashboard/
├── __init__.py
├── models.py
├── schemas.py
├── repository.py
└── service.py

interfaces/api/
└── routes_dashboard.py
```

## Referências

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://www.sqlalchemy.org/
- Chart.js: https://www.chartjs.org/
- Pydantic: https://docs.pydantic.dev/
