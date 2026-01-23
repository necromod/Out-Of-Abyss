@echo off
REM Inicia o Out of the Abyss System (com terminal visivel para debug)
cd /d "%~dp0"
powershell.exe -ExecutionPolicy Bypass -File "run_system.ps1"
pause
