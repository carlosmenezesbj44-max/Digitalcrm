#!/usr/bin/env powershell
# Setup Automático do Dashboard - PowerShell Script
# Execute: powershell -ExecutionPolicy Bypass -File DASHBOARD_SETUP.ps1

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host " SETUP AUTOMÁTICO - DASHBOARD EXECUTIVO" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

$projectRoot = Get-Location
Write-Host "`nDiretório do projeto: $projectRoot" -ForegroundColor Green

# Passo 1: Migrations
Write-Host "`n===============================================" -ForegroundColor Yellow
Write-Host "▶ Passo 1: Rodando Migrations" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow

try {
    Write-Host "Executando: alembic upgrade head" -ForegroundColor Cyan
    & alembic upgrade head
    Write-Host "✓ Migrations completadas com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "✗ Erro ao rodar migrations: $_" -ForegroundColor Red
    Write-Host "Tente rodar manualmente: alembic upgrade head" -ForegroundColor Yellow
}

# Passo 2: Verificar arquivo main.py
Write-Host "`n===============================================" -ForegroundColor Yellow
Write-Host "▶ Passo 2: Verificando main.py" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow

$mainFile = "interfaces/api/main.py"
if (Test-Path $mainFile) {
    $content = Get-Content $mainFile -Raw
    if ($content -like "*routes_dashboard*") {
        Write-Host "✓ main.py já possui as rotas do dashboard" -ForegroundColor Green
    } else {
        Write-Host "⚠️  main.py precisa ser editado manualmente" -ForegroundColor Yellow
        Write-Host "Adicione estas linhas:" -ForegroundColor Cyan
        Write-Host "from interfaces.api.routes_dashboard import router as dashboard_router" -ForegroundColor White
        Write-Host "app.include_router(dashboard_router)" -ForegroundColor White
    }
} else {
    Write-Host "✗ Arquivo main.py não encontrado" -ForegroundColor Red
}

# Passo 3: Inicializar Dashboard
Write-Host "`n===============================================" -ForegroundColor Yellow
Write-Host "▶ Passo 3: Inicializando Dashboard" -ForegroundColor Yellow
Write-Host "===============================================" -ForegroundColor Yellow

$initScript = @"
import sys
sys.path.insert(0, '.')
from crm_core.db.base import SessionLocal
from crm_modules.dashboard.service import DashboardService

try:
    print('Conectando ao banco...')
    db = SessionLocal()
    service = DashboardService(db)
    print('Inicializando dashboard padrão...')
    service.initialize_default_dashboard()
    print('✓ Dashboard inicializado com sucesso!')
    db.close()
except Exception as e:
    print(f'✗ Erro: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"@

try {
    Write-Host "Executando inicialização do dashboard..." -ForegroundColor Cyan
    $initScript | python -
    Write-Host "✓ Dashboard inicializado!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Não conseguiu inicializar via script" -ForegroundColor Yellow
    Write-Host "Você pode inicializar depois via API quando o servidor estiver rodando:" -ForegroundColor Cyan
    Write-Host "curl -X POST http://localhost:8000/api/v1/dashboard/initialize" -ForegroundColor White
}

# Resumo Final
Write-Host "`n===============================================" -ForegroundColor Green
Write-Host "✓ SETUP COMPLETO!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

Write-Host "`n📝 PRÓXIMOS PASSOS:" -ForegroundColor Cyan

Write-Host "`n1. Se não editou main.py, edite agora:" -ForegroundColor Yellow
Write-Host "   Abra: interfaces/api/main.py" -ForegroundColor White
Write-Host "   Adicione (após imports):" -ForegroundColor White
Write-Host "   from interfaces.api.routes_dashboard import router as dashboard_router" -ForegroundColor Gray
Write-Host "   Adicione (após criar app):" -ForegroundColor White
Write-Host "   app.include_router(dashboard_router)" -ForegroundColor Gray

Write-Host "`n2. Inicie o servidor:" -ForegroundColor Yellow
Write-Host "   python -m uvicorn interfaces.api.main:app --reload" -ForegroundColor White

Write-Host "`n3. Teste em outro terminal:" -ForegroundColor Yellow
Write-Host "   # Resumo Executivo" -ForegroundColor Gray
Write-Host "   curl http://localhost:8000/api/v1/dashboard/executive-summary" -ForegroundColor White
Write-Host "   " -ForegroundColor White
Write-Host "   # Gráfico de Receita" -ForegroundColor Gray
Write-Host "   curl http://localhost:8000/api/v1/dashboard/charts/revenue" -ForegroundColor White

Write-Host "`n4. Acesse a documentação:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/docs (Swagger)" -ForegroundColor White
Write-Host "   DASHBOARD_INICIO_RAPIDO.md (Documentação)" -ForegroundColor White

Write-Host "`n===============================================" -ForegroundColor Green
Write-Host "Pressione qualquer tecla para sair..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
