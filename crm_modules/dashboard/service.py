from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from crm_modules.clientes.models import ClienteModel, ClienteConexaoLog
from crm_modules.ordens_servico.models import OrdemServicoModel
from crm_modules.faturamento.models import FaturaModel
from crm_modules.planos.models import PlanoModel
from typing import Dict, Any

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_summary(self) -> Dict[str, Any]:
        """Retorna resumo executivo para o dashboard"""
        try:
            # Total de clientes
            total_clients = self.db.query(func.count(ClienteModel.id)).scalar() or 0

            # Contratos ativos (clientes com status ativo)
            active_contracts = self.db.query(func.count(ClienteModel.id)).filter(ClienteModel.status_servico == 'ativo').scalar() or 0

            # Receita do mês atual
            current_month = datetime.utcnow().month
            current_year = datetime.utcnow().year

            monthly_revenue = self.db.query(func.sum(FaturaModel.valor_total)).filter(
                func.extract('month', FaturaModel.data_emissao) == current_month,
                func.extract('year', FaturaModel.data_emissao) == current_year,
                FaturaModel.status == 'pago'
            ).scalar() or 0.0

            # Pedidos pendentes (ordens de serviço com status pendente)
            pending_orders = self.db.query(func.count(OrdemServicoModel.id)).filter(
                OrdemServicoModel.status.in_(['aberta', 'em_andamento'])
            ).scalar() or 0

            # Campos adicionais para ExecutiveSummary
            support_tickets_open = 0  # TODO: implementar tabela de tickets
            system_uptime_percentage = 99.9  # Valor padrão
            client_growth_percentage = 0.0  # TODO: calcular crescimento mensal
            net_revenue = float(monthly_revenue)  # Por enquanto igual à receita mensal
            avg_ticket_value = 0.0  # TODO: implementar cálculo médio

            return {
                "total_clients": total_clients,
                "active_contracts": active_contracts,
                "monthly_revenue": float(monthly_revenue),
                "pending_orders": pending_orders,
                "support_tickets_open": support_tickets_open,
                "system_uptime_percentage": system_uptime_percentage,
                "client_growth_percentage": client_growth_percentage,
                "net_revenue": net_revenue,
                "avg_ticket_value": avg_ticket_value
            }
        except Exception as e:
            # Em caso de erro, retornar valores padrão
            return {
                "total_clients": 0,
                "active_contracts": 0,
                "monthly_revenue": 0.0,
                "pending_orders": 0,
                "support_tickets_open": 0,
                "system_uptime_percentage": 99.9,
                "client_growth_percentage": 0.0,
                "net_revenue": 0.0,
                "avg_ticket_value": 0.0
            }

    def get_revenue_chart_data(self) -> Dict[str, Any]:
        """Retorna dados para gráfico de receita (últimos 6 meses)"""
        try:
            # Dados mockados por enquanto, implementar consulta real depois
            return {
                "labels": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                "datasets": [{
                    "label": 'Receita',
                    "data": [10000, 12000, 15000, 14000, 18000, 20000],
                    "borderColor": '#667eea',
                    "backgroundColor": 'rgba(102, 126, 234, 0.1)'
                }],
                "title": "Receita Mensal",
                "type": "line"
            }
        except Exception:
            return {
                "labels": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                "datasets": [{
                    "label": 'Receita',
                    "data": [0, 0, 0, 0, 0, 0],
                    "borderColor": '#667eea',
                    "backgroundColor": 'rgba(102, 126, 234, 0.1)'
                }],
                "title": "Receita Mensal",
                "type": "line"
            }

    def get_orders_chart_data(self) -> Dict[str, Any]:
        """Retorna dados para gráfico de ordens por status"""
        try:
            # Contar ordens por status
            pendente = self.db.query(func.count(OrdemServicoModel.id)).filter(OrdemServicoModel.status == 'aberta').scalar() or 0
            em_andamento = self.db.query(func.count(OrdemServicoModel.id)).filter(OrdemServicoModel.status == 'em_andamento').scalar() or 0
            concluida = self.db.query(func.count(OrdemServicoModel.id)).filter(OrdemServicoModel.status == 'concluida').scalar() or 0

            return {
                "labels": ['Pendente', 'Em Andamento', 'Concluída'],
                "datasets": [{
                    "label": 'Ordens',
                    "data": [pendente, em_andamento, concluida],
                    "backgroundColor": ['#e74c3c', '#f39c12', '#2ecc71']
                }],
                "title": "Ordens por Status",
                "type": "doughnut"
            }
        except Exception:
            return {
                "labels": ['Pendente', 'Em Andamento', 'Concluída'],
                "datasets": [{
                    "label": 'Ordens',
                    "data": [0, 0, 0],
                    "backgroundColor": ['#e74c3c', '#f39c12', '#2ecc71']
                }],
                "title": "Ordens por Status",
                "type": "doughnut"
            }

    # Métodos chamados pelas rotas da API
    def get_executive_summary(self) -> Dict[str, Any]:
        """Alias para get_summary para compatibilidade com API"""
        return self.get_summary()

    def get_revenue_chart(self, days: int = 30) -> Dict[str, Any]:
        """Alias para get_revenue_chart_data"""
        return self.get_revenue_chart_data()

    def get_clients_chart(self, days: int = 30) -> Dict[str, Any]:
        """Retorna dados para gráfico de crescimento de clientes"""
        try:
            # Dados mockados por enquanto
            return {
                "labels": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                "datasets": [{
                    "label": 'Novos Clientes',
                    "data": [5, 8, 12, 10, 15, 18],
                    "borderColor": '#764ba2',
                    "backgroundColor": 'rgba(118, 75, 162, 0.1)'
                }],
                "title": "Crescimento de Clientes",
                "type": "line"
            }
        except Exception:
            return {
                "labels": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                "datasets": [{
                    "label": 'Novos Clientes',
                    "data": [0, 0, 0, 0, 0, 0],
                    "borderColor": '#764ba2',
                    "backgroundColor": 'rgba(118, 75, 162, 0.1)'
                }],
                "title": "Crescimento de Clientes",
                "type": "line"
            }

    def get_orders_status_chart(self) -> Dict[str, Any]:
        """Alias para get_orders_chart_data"""
        return self.get_orders_chart_data()

    def get_top_clients_chart(self, limit: int = 10) -> Dict[str, Any]:
        """Retorna top clientes por receita"""
        try:
            # Dados mockados por enquanto
            return {
                "labels": ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
                "datasets": [{
                    "label": 'Receita',
                    "data": [8000, 7000, 6500, 5000, 4500],
                    "backgroundColor": '#667eea'
                }],
                "title": "Top Clientes por Receita",
                "type": "bar"
            }
        except Exception:
            return {
                "labels": ['Cliente A', 'Cliente B', 'Cliente C', 'Cliente D', 'Cliente E'],
                "datasets": [{
                    "label": 'Receita',
                    "data": [0, 0, 0, 0, 0],
                    "backgroundColor": '#667eea'
                }],
                "title": "Top Clientes por Receita",
                "type": "bar"
            }

    def get_support_tickets_chart(self) -> Dict[str, Any]:
        """Retorna dados para gráfico de tickets de suporte"""
        try:
            # Dados mockados por enquanto
            return {
                "labels": ['Aberto', 'Em Andamento', 'Fechado', 'Pendente'],
                "datasets": [{
                    "label": 'Tickets',
                    "data": [12, 8, 45, 5],
                    "backgroundColor": ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
                }],
                "title": "Tickets de Suporte",
                "type": "pie"
            }
        except Exception:
            return {
                "labels": ['Aberto', 'Em Andamento', 'Fechado', 'Pendente'],
                "datasets": [{
                    "label": 'Tickets',
                    "data": [0, 0, 0, 0],
                    "backgroundColor": ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
                }],
                "title": "Tickets de Suporte",
                "type": "pie"
            }

    def get_contracts_status_chart(self) -> Dict[str, Any]:
        """Retorna dados para gráfico de contratos por status"""
        try:
            # Contar contratos por status (usando clientes como proxy)
            ativo = self.db.query(func.count(ClienteModel.id)).filter(ClienteModel.status_servico == 'ativo').scalar() or 0
            pendente = self.db.query(func.count(ClienteModel.id)).filter(ClienteModel.status_servico == 'pendente').scalar() or 0
            cancelado = self.db.query(func.count(ClienteModel.id)).filter(ClienteModel.status_servico == 'cancelado').scalar() or 0

            return {
                "labels": ['Ativo', 'Pendente', 'Cancelado'],
                "datasets": [{
                    "label": 'Contratos',
                    "data": [ativo, pendente, cancelado],
                    "backgroundColor": ['#2ecc71', '#3498db', '#e74c3c']
                }],
                "title": "Contratos por Status",
                "type": "doughnut"
            }
        except Exception:
            return {
                "labels": ['Ativo', 'Pendente', 'Cancelado'],
                "datasets": [{
                    "label": 'Contratos',
                    "data": [0, 0, 0],
                    "backgroundColor": ['#2ecc71', '#3498db', '#e74c3c']
                }],
                "title": "Contratos por Status",
                "type": "doughnut"
            }

    def get_revenue_by_plan_chart(self) -> Dict[str, Any]:
        """Retorna dados para gráfico de receita por plano"""
        try:
            # Query para agrupar receita por plano
            revenue_by_plan = self.db.query(
                PlanoModel.nome,
                func.sum(FaturaModel.valor_total).label('total_revenue')
            ).join(
                ClienteModel, ClienteModel.plano_id == PlanoModel.id
            ).join(
                FaturaModel, FaturaModel.cliente_id == ClienteModel.id
            ).filter(
                FaturaModel.status == 'pago'
            ).group_by(
                PlanoModel.id, PlanoModel.nome
            ).order_by(
                func.sum(FaturaModel.valor_total).desc()
            ).all()

            if revenue_by_plan:
                labels = [row[0] for row in revenue_by_plan]
                data = [float(row[1]) for row in revenue_by_plan]
            else:
                # Dados mockados se não houver dados reais
                labels = ['Plano 50Mbps', 'Plano 100Mbps', 'Plano 200Mbps']
                data = [15000, 25000, 35000]

            return {
                "labels": labels,
                "datasets": [{
                    "label": 'Receita por Plano',
                    "data": data,
                    "backgroundColor": ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
                }],
                "title": "Receita por Plano",
                "type": "bar"
            }
        except Exception as e:
            # Fallback para dados mockados
            return {
                "labels": ['Plano 50Mbps', 'Plano 100Mbps', 'Plano 200Mbps'],
                "datasets": [{
                    "label": 'Receita por Plano',
                    "data": [15000, 25000, 35000],
                    "backgroundColor": ['#667eea', '#764ba2', '#f093fb']
                }],
                "title": "Receita por Plano",
                "type": "bar"
            }

    def initialize_default_dashboard(self):
        """Inicializa dashboard padrão"""
        pass  # Implementar se necessário

    def record_daily_metrics(self):
        """Registra métricas diárias"""
        pass  # Implementar se necessário
