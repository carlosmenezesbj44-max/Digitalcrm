"""Repository for Dashboard operations"""

from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from .models import Dashboard, DashboardKPI, DashboardWidget, MetricHistory


class DashboardRepository:
    """Repository for Dashboard database operations"""

    @staticmethod
    def get_dashboard(db: Session, dashboard_id: int) -> Optional[Dashboard]:
        """Get dashboard by ID"""
        return db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()

    @staticmethod
    def get_dashboard_by_name(db: Session, name: str) -> Optional[Dashboard]:
        """Get dashboard by name"""
        return db.query(Dashboard).filter(Dashboard.name == name).first()

    @staticmethod
    def get_all_dashboards(db: Session, skip: int = 0, limit: int = 10) -> List[Dashboard]:
        """Get all dashboards"""
        return db.query(Dashboard).offset(skip).limit(limit).all()

    @staticmethod
    def create_dashboard(db: Session, name: str, description: Optional[str] = None, is_active: bool = True) -> Dashboard:
        """Create new dashboard"""
        dashboard = Dashboard(name=name, description=description, is_active=is_active)
        db.add(dashboard)
        db.commit()
        db.refresh(dashboard)
        return dashboard

    @staticmethod
    def update_dashboard(db: Session, dashboard_id: int, **kwargs) -> Optional[Dashboard]:
        """Update dashboard"""
        dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
        if dashboard:
            for key, value in kwargs.items():
                if hasattr(dashboard, key):
                    setattr(dashboard, key, value)
            dashboard.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(dashboard)
        return dashboard

    @staticmethod
    def delete_dashboard(db: Session, dashboard_id: int) -> bool:
        """Delete dashboard"""
        dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
        if dashboard:
            db.delete(dashboard)
            db.commit()
            return True
        return False

    # KPI Operations
    @staticmethod
    def create_kpi(db: Session, dashboard_id: int, name: str, metric_type: str,
                   current_value: float, unit: str, target_value: float = None) -> DashboardKPI:
        """Create new KPI"""
        kpi = DashboardKPI(
            dashboard_id=dashboard_id,
            name=name,
            metric_type=metric_type,
            current_value=current_value,
            unit=unit,
            target_value=target_value
        )
        db.add(kpi)
        db.commit()
        db.refresh(kpi)
        return kpi

    @staticmethod
    def update_kpi(db: Session, kpi_id: int, current_value: float,
                   previous_value: float = None) -> Optional[DashboardKPI]:
        """Update KPI value and calculate trend"""
        kpi = db.query(DashboardKPI).filter(DashboardKPI.id == kpi_id).first()
        if kpi:
            kpi.previous_value = kpi.current_value
            kpi.current_value = current_value

            # Calculate percentage change
            if kpi.previous_value and kpi.previous_value != 0:
                kpi.percentage_change = ((current_value - kpi.previous_value) / kpi.previous_value) * 100
            else:
                kpi.percentage_change = 0

            # Determine trend
            if kpi.percentage_change > 0:
                kpi.trend = "up"
            elif kpi.percentage_change < 0:
                kpi.trend = "down"
            else:
                kpi.trend = "stable"

            kpi.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(kpi)

        return kpi

    @staticmethod
    def get_kpi(db: Session, kpi_id: int) -> Optional[DashboardKPI]:
        """Get KPI by ID"""
        return db.query(DashboardKPI).filter(DashboardKPI.id == kpi_id).first()

    @staticmethod
    def get_dashboard_kpis(db: Session, dashboard_id: int) -> List[DashboardKPI]:
        """Get all KPIs for a dashboard"""
        return db.query(DashboardKPI).filter(DashboardKPI.dashboard_id == dashboard_id).all()

    @staticmethod
    def delete_kpi(db: Session, kpi_id: int) -> bool:
        """Delete KPI"""
        kpi = db.query(DashboardKPI).filter(DashboardKPI.id == kpi_id).first()
        if kpi:
            db.delete(kpi)
            db.commit()
            return True
        return False

    # Metric History Operations
    @staticmethod
    def record_metric(db: Session, metric_type: str, value: float, period: str = "daily") -> MetricHistory:
        """Record metric history"""
        history = MetricHistory(metric_type=metric_type, value=value, period=period)
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    @staticmethod
    def get_metric_history(db: Session, metric_type: str, days: int = 30) -> List[MetricHistory]:
        """Get metric history for the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return db.query(MetricHistory).filter(
            MetricHistory.metric_type == metric_type,
            MetricHistory.timestamp >= cutoff_date
        ).order_by(MetricHistory.timestamp).all()

    @staticmethod
    def get_metric_summary(db: Session, metric_type: str, period: str = "daily") -> Optional[float]:
        """Get metric summary (average value for period)"""
        result = db.query(func.avg(MetricHistory.value)).filter(
            MetricHistory.metric_type == metric_type,
            MetricHistory.period == period
        ).scalar()
        return result

    # Widget Operations
    @staticmethod
    def create_widget(db: Session, dashboard_id: int, widget_type: str, title: str,
                      position: int, data_source: str, description: Optional[str] = None) -> DashboardWidget:
        """Create dashboard widget"""
        widget = DashboardWidget(
            dashboard_id=dashboard_id,
            widget_type=widget_type,
            title=title,
            position=position,
            data_source=data_source,
            description=description
        )
        db.add(widget)
        db.commit()
        db.refresh(widget)
        return widget

    @staticmethod
    def get_dashboard_widgets(db: Session, dashboard_id: int) -> List[DashboardWidget]:
        """Get all widgets for a dashboard"""
        return db.query(DashboardWidget).filter(
            DashboardWidget.dashboard_id == dashboard_id
        ).order_by(DashboardWidget.position).all()

    @staticmethod
    def update_widget(db: Session, widget_id: int, **kwargs) -> Optional[DashboardWidget]:
        """Update widget"""
        widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
        if widget:
            for key, value in kwargs.items():
                if hasattr(widget, key):
                    setattr(widget, key, value)
            widget.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(widget)
        return widget

    @staticmethod
    def delete_widget(db: Session, widget_id: int) -> bool:
        """Delete widget"""
        widget = db.query(DashboardWidget).filter(DashboardWidget.id == widget_id).first()
        if widget:
            db.delete(widget)
            db.commit()
            return True
        return False
