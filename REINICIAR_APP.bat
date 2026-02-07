@echo off
REM Script para reiniciar a aplicação

echo.
echo ===============================================
echo      Reiniciando Aplicacao CRM Provedor
echo ===============================================
echo.

REM Matar processo na porta 8000
echo [1/3] Finalizando processo anterior...
netstat -ano | findstr :8000 > nul
if %errorlevel%==0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /PID %%a /F 2>nul
    echo ✓ Processo finalizado
) else (
    echo ✓ Nenhum processo encontrado na porta 8000
)

REM Aguardar um segundo
timeout /t 1 /nobreak

REM Iniciar aplicação
echo.
echo [2/3] Iniciando aplicacao...
cd /d "%~dp0"
python interfaces/api/main.py

REM Se chegar aqui, aplicação foi interrompida
echo.
echo [3/3] Aplicacao foi interrompida
echo.
echo Acesse: http://localhost:8000/carnes
echo         http://localhost:8000/boletos
echo.
pause
