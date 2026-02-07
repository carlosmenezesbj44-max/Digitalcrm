# Dashboard Executivo - Arquitetura

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend/Client                          │
│  (React, Vue, Angular, ou HTML + Chart.js)                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP/REST API Calls
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                     FastAPI Application                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              interfaces/api/routes_dashboard.py             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │ /dashboard   │  │ /charts/*    │  │ /metrics/record  │ │ │
│  │  │ /executive-  │  │ /orders-     │  │ /initialize      │ │ │
│  │  │  summary     │  │  status      │  │                  │ │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────▼─────────────────────────────┐   │
│  │  crm_modules/dashboard/                                 │   │
│  │  ┌──────────────────────────────────────────────────┐  │   │
│  │  │        DashboardService                          │  │   │
│  │  │ - get_executive_summary()                        │  │   │
│  │  │ - get_revenue_chart(days)                        │  │   │
│  │  │ - get_clients_chart(days)                        │  │   │
│  │  │ - get_orders_status_chart()                      │  │   │
│  │  │ - get_top_clients_chart(limit)                   │  │   │
│  │  │ - get_support_tickets_chart()                    │  │   │
│  │  │ - get_contracts_status_chart()                   │  │   │
│  │  │ - record_daily_metrics()                         │  │   │
│  │  │ - initialize_default_dashboard()                 │  │   │
│  │  └──────────────────────────────────────────────────┘  │   │
│  │                      │                                   │   │
│  │  ┌───────────────────▼──────────────────────────────┐  │   │
│  │  │    DashboardRepository                           │  │   │
│  │  │ - get_dashboard(db, id)                          │  │   │
│  │  │ - create_kpi(db, ...)                            │  │   │
│  │  │ - update_kpi(db, kpi_id, current_value)         │  │   │
│  │  │ - record_metric(db, metric_type, value)         │  │   │
│  │  │ - get_metric_history(db, metric_type, days)     │  │   │
│  │  │ - create_widget(db, ...)                         │  │   │
│  │  │ - (+ 14 mais métodos CRUD)                       │  │   │
│  │  └──────────────┬──────────────────────────────────┘  │   │
│  └─────────────────┼──────────────────────────────────────┘   │
│                    │ SQLAlchemy ORM                             │
│                    │ (Queries parametrizadas)                   │
└────────────────────┼──────────────────────────────────────────┘
                     │
┌────────────────────▼──────────────────────────────────────────┐
│                   SQLite/PostgreSQL                            │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ dashboard               │ dashboard_kpi                │   │
│  │ ┌──────────────────┐    │ ┌──────────────────────────┐ │   │
│  │ │ id               │    │ │ id                       │ │   │
│  │ │ name             │───┼┼│ dashboard_id (FK)        │ │   │
│  │ │ description      │    │ │ name                     │ │   │
│  │ │ is_active        │    │ │ metric_type              │ │   │
│  │ │ created_at       │    │ │ current_value            │ │   │
│  │ │ updated_at       │    │ │ previous_value           │ │   │
│  │ └──────────────────┘    │ │ trend (up/down/stable)   │ │   │
│  │                         │ │ percentage_change        │ │   │
│  │ dashboard_widget        │ │ created_at               │ │   │
│  │ ┌──────────────────┐    │ └──────────────────────────┘ │   │
│  │ │ id               │    │                              │   │
│  │ │ dashboard_id(FK) │    │ metric_history               │   │
│  │ │ widget_type      │    │ ┌──────────────────────────┐ │   │
│  │ │ title            │    │ │ id                       │ │   │
│  │ │ position         │    │ │ metric_type              │ │   │
│  │ │ data_source      │    │ │ value                    │ │   │
│  │ │ is_visible       │    │ │ timestamp (indexed)      │ │   │
│  │ └──────────────────┘    │ │ period                   │ │   │
│  │                         │ │ metadata                 │ │   │
│  │                         │ └──────────────────────────┘ │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Related Tables (Queries Join)                          │   │
│  │ ├─ clientes                (get_executive_summary)     │   │
│  │ ├─ contratos               (get_executive_summary)     │   │
│  │ ├─ ordens_servico          (get_executive_summary)     │   │
│  │ ├─ tickets                 (get_executive_summary)     │   │
│  │ ├─ faturas                 (get_executive_summary)     │   │
│  │ └─ usuarios                (permissions - TODO)        │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

### 1. Requisição de Executive Summary

```
Client                API Router              Service            Repository           Database
  │                      │                      │                   │                   │
  ├─ GET /executive-    │                      │                   │                   │
  │   summary           │                      │                   │                   │
  │────────────────────►│                      │                   │                   │
  │                     │  get_executive_      │                   │                   │
  │                     │  summary()           │                   │                   │
  │                     ├─────────────────────►│                   │                   │
  │                     │                      │  query clientes   │                   │
  │                     │                      ├──────────────────►│                   │
  │                     │                      │                   │  COUNT(*)         │
  │                     │                      │                   ├──────────────────►│
  │                     │                      │                   │  return count     │
  │                     │                      │                   │◄──────────────────┤
  │                     │  return               │                   │                   │
  │                     │  ExecutiveSummary    │                   │                   │
  │◄─ ExecutiveSummary ─┤◄─────────────────────┤                   │                   │
  │                     │                      │                   │                   │
  └─────────────────────┘                      └────────────────────────────────────────┘

Response:
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

### 2. Requisição de Gráfico

```
Client                API Router              Service            Repository           Database
  │                      │                      │                   │                   │
  ├─ GET /charts/       │                      │                   │                   │
  │   revenue?days=30   │                      │                   │                   │
  │────────────────────►│                      │                   │                   │
  │                     │  get_revenue_chart   │                   │                   │
  │                     │  (days=30)           │                   │                   │
  │                     ├─────────────────────►│                   │                   │
  │                     │                      │  query last 30    │                   │
  │                     │                      │  days             │                   │
  │                     │                      ├──────────────────►│                   │
  │                     │                      │                   │  SELECT date,     │
  │                     │                      │                   │  SUM(valor)       │
  │                     │                      │                   │  GROUP BY date    │
  │                     │                      │                   ├──────────────────►│
  │                     │                      │                   │  return results   │
  │                     │                      │                   │◄──────────────────┤
  │                     │  ChartDataResponse   │                   │                   │
  │◄─ Chart JSON ───────┤◄─────────────────────┤                   │                   │
  │                     │                      │                   │                   │
  └─────────────────────┘                      └────────────────────────────────────────┘

Response:
{
  "labels": ["2024-01-01", "2024-01-02", ...],
  "datasets": [
    {
      "label": "Receita Diária",
      "data": [1000, 1500, 1200, ...],
      "borderColor": "#2ecc71"
    }
  ],
  "title": "Receita dos Últimos 30 Dias",
  "type": "line"
}
```

## Padrão de Design: Service-Repository

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│    (FastAPI Endpoints / HTTP Routes)                    │
└──────────────────┬──────────────────────────────────────┘
                   │ Injeta dependências
                   │ (get_db: Session)
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Service Layer (Business Logic)             │
│  ┌─────────────────────────────────────────────────┐   │
│  │  DashboardService(db: Session)                  │   │
│  │                                                 │   │
│  │  def get_executive_summary():                   │   │
│  │    ├─ Cria repositório                          │   │
│  │    ├─ Chama métodos repository                  │   │
│  │    ├─ Processa dados                            │   │
│  │    ├─ Calcula tendências                        │   │
│  │    └─ Retorna resposta normalizada              │   │
│  └──────────┬────────────────────────────────────┘   │
│             │ Usa
│  ┌──────────▼────────────────────────────────────┐   │
│  │  DashboardRepository(db: Session)               │   │
│  │                                                │   │
│  │  def get_metric_history(metric, days):        │   │
│  │    └─ Query DB, retorna raw data               │   │
│  │                                                │   │
│  │  def record_metric(metric_type, value):       │   │
│  │    └─ INSERT na tabela                         │   │
│  │                                                │   │
│  │  def create_kpi(...):                          │   │
│  │    └─ INSERT KPI                               │   │
│  └──────────┬────────────────────────────────────┘   │
└─────────────┼─────────────────────────────────────────┘
              │ SQLAlchemy ORM
              │ (Queries parametrizadas)
              │
┌─────────────▼─────────────────────────────────────────┐
│              Data Layer (Database)                     │
│  - Cached queries                                     │
│  - Indexed lookups                                    │
│  - Relational integrity                               │
└───────────────────────────────────────────────────────┘
```

## Dependências de Dados

```
Executive Summary
├── total_clients ◄─── clientes.count()
├── active_contracts ◄─ contratos.count() WHERE status='ativo'
├── monthly_revenue ◄── faturas.sum() WHERE date >= month_start
├── pending_orders ◄─── ordens_servico.count() WHERE status IN (...)
├── support_tickets_open ◄── tickets.count() WHERE status IN (...)
├── revenue_trend ◄──── (comparar com mês anterior)
├── client_growth_percentage ◄── (calcular diferença)
├── net_revenue ◄───── (monthly_revenue * 0.75)
└── avg_ticket_value ◄─ (monthly_revenue / total_tickets)

Revenue Chart
├── Queries: faturas.data_emissao >= (now - 30 days)
├── Agregação: GROUP BY DATE(data_emissao), SUM(valor_total)
└── Resultado: 30 pontos de dados

Orders Status Chart
├── Query: ordens_servico.status
├── Contagem: COUNT(*) GROUP BY status
└── Resultado: 4 categorias (pendente, em_progresso, concluido, cancelado)

Top Clients Chart
├── Join: clientes ◄─► faturas
├── Agregação: GROUP BY cliente, SUM(valor)
├── Ordenação: ORDER BY SUM DESC
└── Limite: TOP 10
```

## Escalabilidade

```
┌─────────────────────────────────────────────────────────┐
│                  Current State (SQLite)                 │
│  - Single process                                       │
│  - No caching                                           │
│  - Direct queries                                       │
└─────────────────────────────────────────────────────────┘
                          │ Escalar para
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Production State (PostgreSQL)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Redis       │  │  PostgreSQL  │  │  Celery      │  │
│  │  Cache       │  │  Database    │  │  Workers     │  │
│  │              │  │              │  │              │  │
│  │ - KPI Cache  │  │ - Indexes    │  │ - Scheduled  │  │
│  │ - Chart Data │  │ - Partitions │  │   metrics    │  │
│  │ - TTL: 5min  │  │ - Replication   │  - Alerts    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │ Escalar para
                          ▼
┌─────────────────────────────────────────────────────────┐
│        Enterprise State (Multi-service)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Dashboard│  │ Alerting │  │ Analytics│  │Reports │  │
│  │ Service  │  │ Service  │  │ Service  │  │Service │  │
│  │          │  │          │  │          │  │        │  │
│  │ REST API │  │ Webhooks │  │ ML/BI    │  │PDF/XLS │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│       ▲                                         ▲        │
│       └─────────────────┬──────────────────────┘        │
│                         │                               │
│            ┌────────────▼──────────────┐                │
│            │  Event Bus / Message Queue │                │
│            │  (RabbitMQ, Kafka, Redis)  │                │
│            └─────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

## Segurança (Camadas)

```
Client Request
      │
      ▼
┌─────────────────────────────────────────┐
│  1. HTTPS/TLS                           │
│     - Encrypta transit                  │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│  2. Authentication (JWT)                │
│     - Verifica token                    │
│     - Valida assinatura                 │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│  3. Authorization (RBAC)                │
│     - Valida role (admin, gerente)      │
│     - Verifica permissões               │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│  4. Input Validation (Pydantic)         │
│     - Valida tipos                      │
│     - Valida ranges                     │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│  5. Query Injection Prevention           │
│     - SQLAlchemy ORM                    │
│     - Parametrized queries              │
└──────────────────┬──────────────────────┘
                   ▼
┌─────────────────────────────────────────┐
│  6. Rate Limiting                       │
│     - SlowAPI (TODO)                    │
└──────────────────┬──────────────────────┘
                   ▼
              Response
```

---

**Arquitetura modular, escalável e segura.**
