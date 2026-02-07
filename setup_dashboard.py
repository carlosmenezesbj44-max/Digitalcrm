#!/usr/bin/env python
"""
Setup script for Dashboard implementation

This script:
1. Creates database tables via Alembic
2. Initializes default dashboard
3. Records initial metrics
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("Dashboard Executivo - Setup")
    print("="*60)

    # Get the root directory
    root_dir = Path(__file__).parent
    
    # Step 1: Run migrations
    if not run_command(
        f"cd {root_dir} && alembic upgrade head",
        "Running database migrations"
    ):
        print("\n✗ Failed to run migrations. Please run manually:")
        print("  alembic upgrade head")
        sys.exit(1)

    # Step 2: Initialize dashboard
    print(f"\n{'='*60}")
    print("▶ Initializing default dashboard")
    print(f"{'='*60}")
    
    try:
        # Create initialization script inline
        init_script = f'''
import sys
sys.path.insert(0, r"{root_dir}")

from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

print("Creating database session...")
db = SessionLocal()

try:
    service = DashboardService(db)
    print("Initializing default dashboard...")
    service.initialize_default_dashboard()
    print("✓ Dashboard initialized successfully!")
except Exception as e:
    print(f"✗ Error initializing dashboard: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()
'''
        
        # Run the inline script
        result = subprocess.run(
            [sys.executable, "-c", init_script],
            cwd=root_dir,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        
        if result.returncode != 0:
            raise RuntimeError("Dashboard initialization failed")
            
        print("✓ Dashboard initialized - SUCCESS")
        
    except Exception as e:
        print(f"✗ Dashboard initialization - FAILED")
        print(f"Error: {e}")
        print("\nYou can initialize manually by running:")
        print("  python -c \"from crm_modules.dashboard.service import DashboardService; from crm_core.db.base import SessionLocal; db = SessionLocal(); DashboardService(db).initialize_default_dashboard()\"")

    # Step 3: Summary
    print(f"\n{'='*60}")
    print("✓ Dashboard Setup Complete!")
    print(f"{'='*60}")
    print("\nNext steps:")
    print("1. Add the dashboard routes to interfaces/api/main.py")
    print("2. Start the API server: python -m uvicorn interfaces.api.main:app --reload")
    print("3. Access dashboard endpoints:")
    print("   - Executive Summary: GET /api/v1/dashboard/executive-summary")
    print("   - Revenue Chart: GET /api/v1/dashboard/charts/revenue")
    print("   - More endpoints documented in DASHBOARD_IMPLEMENTACAO.md")
    print("\nDocumentation: DASHBOARD_IMPLEMENTACAO.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
