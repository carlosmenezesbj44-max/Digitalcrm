# Script PowerShell para reiniciar a aplicação

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "      Reiniciando Aplicacao CRM Provedor" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Passo 1: Matar processo na porta 8000
Write-Host "[1/3] Finalizando processo anterior..." -ForegroundColor Yellow

$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($processes) {
    foreach ($process in $processes) {
        Stop-Process -Id $process.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Write-Host "✓ Processo finalizado" -ForegroundColor Green
} else {
    Write-Host "✓ Nenhum processo encontrado na porta 8000" -ForegroundColor Green
}

# Aguardar um segundo
Start-Sleep -Seconds 1

# Passo 2: Iniciar aplicação
Write-Host ""
Write-Host "[2/3] Iniciando aplicacao..." -ForegroundColor Yellow
Write-Host ""

$appPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $appPath

# Verificar se arquivo existe
if (Test-Path "interfaces/api/main.py") {
    Write-Host "✓ Arquivo main.py encontrado" -ForegroundColor Green
    Write-Host ""
    
    # Iniciar aplicação
    python interfaces/api/main.py
    
    # Se chegar aqui, aplicação foi interrompida
    Write-Host ""
    Write-Host "[3/3] Aplicacao foi interrompida" -ForegroundColor Yellow
} else {
    Write-Host "✗ Arquivo main.py nao encontrado!" -ForegroundColor Red
    Write-Host "Caminho esperado: $appPath\interfaces\api\main.py" -ForegroundColor Red
}

Write-Host ""
Write-Host "Acesse:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/carnes" -ForegroundColor Green
Write-Host "  http://localhost:8000/boletos" -ForegroundColor Green
Write-Host ""

Read-Host "Pressione ENTER para sair"
