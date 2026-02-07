"""Dashboard API routes"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from crm_modules.dashboard import DashboardService
from crm_modules.dashboard.schemas import (
    DashboardResponse,
    ExecutiveSummary,
    ChartDataResponse,
    DashboardCreateRequest,
    DashboardUpdateRequest,
    KPICreateRequest,
)
from interfaces.api.dependencies import get_db
from crm_core.security.dependencies import verificar_permissao, obter_usuario_atual

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])
# Temporariamente removendo autenticação para debug


@router.get("/executive-summary", response_model=ExecutiveSummary)
def get_executive_summary(db: Session = Depends(get_db)):
    """
    Get executive summary with key performance indicators

    Returns:
    - total_clients: Total number of clients
    - active_contracts: Number of active contracts
    - monthly_revenue: Revenue for current month
    - pending_orders: Pending service orders
    - support_tickets_open: Open support tickets
    - system_uptime_percentage: System availability
    - revenue_trend: Revenue trend (up/down)
    - client_growth_percentage: Client growth percentage
    - net_revenue: Net revenue after costs
    - avg_ticket_value: Average ticket value
    """
    service = DashboardService(db)
    return service.get_executive_summary()


@router.get("/charts/revenue", response_model=ChartDataResponse)
def get_revenue_chart(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """Get revenue chart data for the last N days"""
    service = DashboardService(db)
    return service.get_revenue_chart(days=days)


@router.get("/charts/clients", response_model=ChartDataResponse)
def get_clients_chart(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """Get client growth chart for the last N days"""
    service = DashboardService(db)
    return service.get_clients_chart(days=days)


@router.get("/charts/orders-status", response_model=ChartDataResponse)
def get_orders_status_chart(db: Session = Depends(get_db)):
    """Get orders grouped by status"""
    service = DashboardService(db)
    return service.get_orders_status_chart()


@router.get("/charts/top-clients", response_model=ChartDataResponse)
def get_top_clients_chart(limit: int = Query(10, ge=5, le=50), db: Session = Depends(get_db)):
    """Get top clients by revenue"""
    service = DashboardService(db)
    return service.get_top_clients_chart(limit=limit)


@router.get("/charts/support-tickets", response_model=ChartDataResponse)
def get_support_tickets_chart(db: Session = Depends(get_db)):
    """Get support tickets grouped by status"""
    service = DashboardService(db)
    return service.get_support_tickets_chart()


@router.get("/charts/contracts-status", response_model=ChartDataResponse)
def get_contracts_status_chart(db: Session = Depends(get_db)):
    """Get contracts grouped by status"""
    service = DashboardService(db)
    return service.get_contracts_status_chart()


@router.post("/initialize")
def initialize_default_dashboard(db: Session = Depends(get_db)):
    """Initialize default dashboard with standard widgets"""
    service = DashboardService(db)
    service.initialize_default_dashboard()
    return {"message": "Dashboard initialized successfully"}


@router.post("/metrics/record")
def record_daily_metrics(db: Session = Depends(get_db)):
    """Manually record daily metrics (normally run via scheduled task)"""
    service = DashboardService(db)
    service.record_daily_metrics()
    return {"message": "Daily metrics recorded successfully"}


@router.get("/{dashboard_id}", response_model=DashboardResponse)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Get dashboard by ID"""
    from crm_modules.dashboard import DashboardRepository
    repository = DashboardRepository()
    dashboard = repository.get_dashboard(db, dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard


@router.get("", response_model=list[DashboardResponse])
def list_dashboards(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all dashboards"""
    from crm_modules.dashboard import DashboardRepository
    repository = DashboardRepository()
    dashboards = repository.get_all_dashboards(db, skip=skip, limit=limit)
    return dashboards


@router.post("", response_model=DashboardResponse)
def create_dashboard(request: DashboardCreateRequest, db: Session = Depends(get_db)):
    """Create new dashboard"""
    from crm_modules.dashboard import DashboardRepository
    repository = DashboardRepository()
    dashboard = repository.create_dashboard(
        db,
        name=request.name,
        description=request.description,
        is_active=request.is_active
    )
    return dashboard


@router.put("/{dashboard_id}", response_model=DashboardResponse)
def update_dashboard(dashboard_id: int, request: DashboardUpdateRequest, db: Session = Depends(get_db)):
    """Update dashboard"""
    from crm_modules.dashboard import DashboardRepository
    repository = DashboardRepository()
    update_data = request.dict(exclude_unset=True)
    dashboard = repository.update_dashboard(db, dashboard_id, **update_data)
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return dashboard


@router.delete("/{dashboard_id}")
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db)):
    """Delete dashboard"""
    from crm_modules.dashboard import DashboardRepository
    repository = DashboardRepository()
    success = repository.delete_dashboard(db, dashboard_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return {"message": "Dashboard deleted successfully"}
