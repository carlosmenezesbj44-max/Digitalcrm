@echo off
chcp 65001 > nul

echo.
echo ======================================================================
echo  DASHBOARD EXECUTIVO - INICIANDO
echo ======================================================================
echo.

echo Iniciando servidor FastAPI...
echo.
echo ACESSE: http://localhost:8001
echo.
echo Tecle CTRL+C para parar o servidor
echo.
echo ======================================================================

python -m uvicorn interfaces.api.main:app --reload --host 0.0.0.0 --port 8001
