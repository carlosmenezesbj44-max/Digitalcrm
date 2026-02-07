@echo off
chcp 65001 > nul
REM Setup Automático do Dashboard - Batch Script para Windows

echo.
echo ===============================================
echo  SETUP AUTOMÁTICO - DASHBOARD EXECUTIVO
echo ===============================================
echo.

REM Passo 1: Migrations
echo.
echo ===============================================
echo  Passo 1: Rodando Migrations
echo ===============================================
echo.

echo Executando: alembic upgrade head
call alembic upgrade head

if %ERRORLEVEL% EQU 0 (
    echo ✓ Migrations completadas com sucesso!
) else (
    echo ✗ Erro ao rodar migrations
    echo Tente rodar manualmente: alembic upgrade head
)

REM Passo 2: Inicializar Dashboard
echo.
echo ===============================================
echo  Passo 2: Inicializando Dashboard
echo ===============================================
echo.

echo Inicializando dashboard padrão...

python -c "^
import sys; ^
sys.path.insert(0, '.'); ^
from crm_core.db.base import SessionLocal; ^
from crm_modules.dashboard.service import DashboardService; ^
db = SessionLocal(); ^
service = DashboardService(db); ^
service.initialize_default_dashboard(); ^
print('✓ Dashboard inicializado com sucesso!'); ^
db.close()^
"

if %ERRORLEVEL% EQU 0 (
    echo Dashboard pronto!
) else (
    echo ✗ Erro ao inicializar dashboard
    echo Você pode inicializar depois via API
)

REM Resumo Final
echo.
echo ===============================================
echo  ✓ SETUP COMPLETO!
echo ===============================================
echo.
echo 📝 PRÓXIMOS PASSOS:
echo.
echo 1. Edite main.py (se ainda não editou):
echo    - Adicione: from interfaces.api.routes_dashboard import router as dashboard_router
echo    - Adicione: app.include_router(dashboard_router)
echo.
echo 2. Inicie o servidor:
echo    python -m uvicorn interfaces.api.main:app --reload
echo.
echo 3. Teste em outro terminal:
echo    curl http://localhost:8000/api/v1/dashboard/executive-summary
echo.
echo 4. Acesse:
echo    http://localhost:8000/docs (Swagger Documentation)
echo    DASHBOARD_INICIO_RAPIDO.md (Documentação)
echo.
echo ===============================================
echo.
pause
