@echo off
chcp 65001 > nul

echo.
echo ======================================================================
echo  PARANDO TODOS OS SERVIDORES
echo ======================================================================
echo.

echo Procurando por processos Python em execucao...
echo.

tasklist | findstr "python"

echo.
echo Encerrando todos os processos Python...
echo.

taskkill /F /IM python.exe

echo.
echo ======================================================================
echo  SERVIDORES PARADOS
echo ======================================================================
echo.

pause
