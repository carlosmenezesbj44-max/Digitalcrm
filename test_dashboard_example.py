#!/usr/bin/env python
"""
Example script to test Dashboard Executivo

Usage:
    python test_dashboard_example.py
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))


def test_dashboard_service():
    """Test DashboardService with sample data"""
    
    print("\n" + "="*70)
    print("Dashboard Executivo - Test Script")
    print("="*70)
    
    try:
        # Import after path is set
        from crm_core.db.base import SessionLocal
        from crm_modules.dashboard.service import DashboardService
        
        # Create database session
        print("\n▶ Creating database session...")
        db = SessionLocal()
        print("✓ Session created")
        
        # Initialize service
        print("\n▶ Initializing DashboardService...")
        service = DashboardService(db)
        print("✓ Service initialized")
        
        # Initialize default dashboard
        print("\n▶ Initializing default dashboard...")
        service.initialize_default_dashboard()
        print("✓ Default dashboard created/updated")
        
        # Test Executive Summary
        print("\n▶ Testing Executive Summary...")
        summary = service.get_executive_summary()
        print("✓ Executive Summary retrieved:")
        print(f"  - Total Clientes: {summary.total_clients}")
        print(f"  - Contratos Ativos: {summary.active_contracts}")
        print(f"  - Receita do Mês: R$ {summary.monthly_revenue:,.2f}")
        print(f"  - Pedidos Pendentes: {summary.pending_orders}")
        print(f"  - Tickets Abertos: {summary.support_tickets_open}")
        print(f"  - Receita Líquida: R$ {summary.net_revenue:,.2f}")
        print(f"  - Valor Médio por Ticket: R$ {summary.avg_ticket_value:,.2f}")
        print(f"  - Tendência Receita: {summary.revenue_trend}")
        print(f"  - Crescimento Clientes: {summary.client_growth_percentage:.2f}%")
        print(f"  - Uptime Sistema: {summary.system_uptime_percentage}%")
        
        # Test Revenue Chart
        print("\n▶ Testing Revenue Chart (últimos 30 dias)...")
        revenue_chart = service.get_revenue_chart(days=30)
        print("✓ Revenue Chart retrieved:")
        print(f"  - Tipo: {revenue_chart.type}")
        print(f"  - Título: {revenue_chart.title}")
        print(f"  - Número de dias: {len(revenue_chart.labels)}")
        if revenue_chart.labels:
            print(f"  - Primeiro dia: {revenue_chart.labels[0]}")
            print(f"  - Último dia: {revenue_chart.labels[-1]}")
        print(f"  - Datasets: {len(revenue_chart.datasets)}")
        
        # Test Clients Chart
        print("\n▶ Testing Clients Chart...")
        clients_chart = service.get_clients_chart(days=30)
        print("✓ Clients Chart retrieved:")
        print(f"  - Tipo: {clients_chart.type}")
        print(f"  - Título: {clients_chart.title}")
        print(f"  - Número de dias: {len(clients_chart.labels)}")
        
        # Test Orders Status Chart
        print("\n▶ Testing Orders Status Chart...")
        orders_chart = service.get_orders_status_chart()
        print("✓ Orders Status Chart retrieved:")
        print(f"  - Tipo: {orders_chart.type}")
        print(f"  - Título: {orders_chart.title}")
        print(f"  - Categorias: {orders_chart.labels}")
        
        # Test Top Clients Chart
        print("\n▶ Testing Top Clients Chart...")
        top_clients_chart = service.get_top_clients_chart(limit=10)
        print("✓ Top Clients Chart retrieved:")
        print(f"  - Tipo: {top_clients_chart.type}")
        print(f"  - Título: {top_clients_chart.title}")
        print(f"  - Número de clientes: {len(top_clients_chart.labels)}")
        
        # Test Support Tickets Chart
        print("\n▶ Testing Support Tickets Chart...")
        tickets_chart = service.get_support_tickets_chart()
        print("✓ Support Tickets Chart retrieved:")
        print(f"  - Tipo: {tickets_chart.type}")
        print(f"  - Título: {tickets_chart.title}")
        print(f"  - Categorias: {tickets_chart.labels}")
        
        # Test Contracts Status Chart
        print("\n▶ Testing Contracts Status Chart...")
        contracts_chart = service.get_contracts_status_chart()
        print("✓ Contracts Status Chart retrieved:")
        print(f"  - Tipo: {contracts_chart.type}")
        print(f"  - Título: {contracts_chart.title}")
        print(f"  - Categorias: {contracts_chart.labels}")
        
        # Test Recording Metrics
        print("\n▶ Testing Record Daily Metrics...")
        service.record_daily_metrics()
        print("✓ Daily metrics recorded successfully")
        
        # Summary
        print("\n" + "="*70)
        print("✓ All Dashboard Tests Passed!")
        print("="*70)
        print("\nNext steps:")
        print("1. Start API: python -m uvicorn interfaces.api.main:app --reload")
        print("2. Access: http://localhost:8000/api/v1/dashboard/executive-summary")
        print("3. See documentation: DASHBOARD_INICIO_RAPIDO.md")
        print("="*70 + "\n")
        
        # Close session
        db.close()
        return True
        
    except ImportError as e:
        print(f"✗ Import Error: {e}")
        print("\nMake sure you have:")
        print("1. Created crm_modules/dashboard/ directory")
        print("2. Created all dashboard module files")
        print("3. Ran database migrations: alembic upgrade head")
        return False
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoints (requires running API server)"""
    
    print("\n" + "="*70)
    print("Dashboard API Endpoints Test")
    print("="*70)
    
    try:
        import requests
        
        BASE_URL = "http://localhost:8000/api/v1/dashboard"
        
        # Test Executive Summary
        print("\n▶ Testing GET /executive-summary...")
        response = requests.get(f"{BASE_URL}/executive-summary", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✓ Executive Summary endpoint working")
            print(f"  Status: {response.status_code}")
            print(f"  Data: {data}")
        else:
            print(f"✗ Failed with status {response.status_code}")
            print(f"  Response: {response.text}")
        
        # Test Revenue Chart
        print("\n▶ Testing GET /charts/revenue...")
        response = requests.get(f"{BASE_URL}/charts/revenue?days=30", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✓ Revenue Chart endpoint working")
            print(f"  Status: {response.status_code}")
            print(f"  Tipo: {data.get('type')}")
            print(f"  Título: {data.get('title')}")
            print(f"  Pontos de dados: {len(data.get('labels', []))}")
        else:
            print(f"✗ Failed with status {response.status_code}")
        
        # Test Initialize
        print("\n▶ Testing POST /initialize...")
        response = requests.post(f"{BASE_URL}/initialize", timeout=5)
        if response.status_code == 200:
            print("✓ Initialize endpoint working")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Failed with status {response.status_code}")
        
        print("\n" + "="*70)
        print("API Endpoints Test Complete")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server")
        print("  Make sure the API is running on http://localhost:8000")
        print("  Run: python -m uvicorn interfaces.api.main:app --reload")
    except ImportError:
        print("✗ requests library not installed")
        print("  Run: pip install requests")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Dashboard implementation")
    parser.add_argument(
        "--api",
        action="store_true",
        help="Test API endpoints (requires running server)"
    )
    parser.add_argument(
        "--service",
        action="store_true",
        default=True,
        help="Test DashboardService directly (default)"
    )
    
    args = parser.parse_args()
    
    # Test service
    if args.service:
        success = test_dashboard_service()
        if not success:
            sys.exit(1)
    
    # Test API
    if args.api:
        test_api_endpoints()
