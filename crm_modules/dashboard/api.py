from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crm_core.db.base import get_db
from crm_modules.dashboard.service import DashboardService
from crm_core.security.dependencies import obter_usuario_atual

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados resumidos para o dashboard"""
    service = DashboardService(db)
    return service.get_summary()

@router.get("/charts/revenue")
def get_revenue_chart(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados do gráfico de receita"""
    service = DashboardService(db)
    return service.get_revenue_chart_data()

@router.get("/charts/orders")
def get_orders_chart(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados do gráfico de ordens por status"""
    service = DashboardService(db)
    return service.get_orders_chart_data()

@router.get("/charts/blocked-clients")
def get_blocked_clients_chart(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados do gráfico de clientes bloqueados"""
    service = DashboardService(db)
    return service.get_blocked_clients_chart()

@router.get("/charts/connection-status")
def get_connection_status_chart(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados do gráfico de status de conexão"""
    service = DashboardService(db)
    return service.get_connection_status_chart()

@router.get("/charts/connection-uptime")
def get_connection_uptime_chart(db: Session = Depends(get_db), _ = Depends(obter_usuario_atual)):
    """Retorna dados do gráfico de uptime de conexão"""
    service = DashboardService(db)
    return service.get_connection_uptime_chart()
