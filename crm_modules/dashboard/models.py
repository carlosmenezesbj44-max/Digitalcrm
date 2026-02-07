"""Dashboard models for KPIs and metrics"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from crm_core.db.models_base import Base


class Dashboard(Base):
    """Main Dashboard entity"""
    __tablename__ = "dashboard"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    kpis = relationship("DashboardKPI", back_populates="dashboard", cascade="all, delete-orphan")
    widgets = relationship("DashboardWidget", back_populates="dashboard", cascade="all, delete-orphan")


class DashboardKPI(Base):
    """KPI metrics for dashboard"""
    __tablename__ = "dashboard_kpi"

    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, ForeignKey("dashboard.id"), index=True)
    name = Column(String(255), index=True)
    metric_type = Column(String(50))  # revenue, clients, orders, uptime, etc
    current_value = Column(Float, default=0.0)
    previous_value = Column(Float, nullable=True)
    target_value = Column(Float, nullable=True)
    unit = Column(String(50))  # currency, percentage, count, hours, etc
    trend = Column(String(20), nullable=True)  # up, down, stable
    percentage_change = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dashboard = relationship("Dashboard", back_populates="kpis")


class DashboardWidget(Base):
    """Dashboard widgets configuration"""
    __tablename__ = "dashboard_widget"

    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, ForeignKey("dashboard.id"), index=True)
    widget_type = Column(String(50))  # chart, kpi_card, table, gauge, etc
    title = Column(String(255))
    description = Column(Text, nullable=True)
    position = Column(Integer)  # Order in dashboard
    data_source = Column(String(255))  # Which metric/query this widget uses
    config = Column(Text, nullable=True)  # JSON config for widget
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dashboard = relationship("Dashboard", back_populates="widgets")


class MetricHistory(Base):
    """Historical data for metrics tracking"""
    __tablename__ = "metric_history"

    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(String(255), index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    period = Column(String(50))  # daily, weekly, monthly, yearly
    data_metadata = Column(Text, nullable=True)  # JSON additional data
