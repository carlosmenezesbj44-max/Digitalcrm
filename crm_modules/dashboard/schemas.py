"""Pydantic schemas for Dashboard"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class KPIResponse(BaseModel):
    """KPI Response Schema"""
    id: int
    name: str
    metric_type: str
    current_value: float
    previous_value: Optional[float] = None
    target_value: Optional[float] = None
    unit: str
    trend: Optional[str] = None  # up, down, stable
    percentage_change: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChartDataResponse(BaseModel):
    """Chart Data Response Schema"""
    labels: List[str]
    datasets: List[Dict[str, Any]]
    title: str
    type: str  # line, bar, pie, doughnut, etc


class MetricResponse(BaseModel):
    """Single Metric Response"""
    label: str
    value: float
    unit: str
    status: str  # success, warning, danger, info
    icon: Optional[str] = None


class DashboardWidgetResponse(BaseModel):
    """Dashboard Widget Response"""
    id: int
    title: str
    widget_type: str
    position: int
    description: Optional[str] = None
    data_source: str
    is_visible: bool

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    """Complete Dashboard Response"""
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    kpis: List[KPIResponse] = []
    widgets: List[DashboardWidgetResponse] = []

    class Config:
        from_attributes = True


class DashboardCreateRequest(BaseModel):
    """Create Dashboard Request"""
    name: str
    description: Optional[str] = None
    is_active: bool = True


class DashboardUpdateRequest(BaseModel):
    """Update Dashboard Request"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class KPICreateRequest(BaseModel):
    """Create KPI Request"""
    name: str
    metric_type: str
    current_value: float
    target_value: Optional[float] = None
    unit: str


class ExecutiveSummary(BaseModel):
    """Executive Summary - Quick overview"""
    total_clients: int
    active_contracts: int
    monthly_revenue: float
    pending_orders: int
    support_tickets_open: int
    system_uptime_percentage: float
    revenue_trend: Optional[str] = None
    client_growth_percentage: float
    net_revenue: float
    avg_ticket_value: float
