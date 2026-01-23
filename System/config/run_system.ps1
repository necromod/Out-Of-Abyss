# Script para executar o Out of the Abyss System
$ErrorActionPreference = "Stop"

Write-Host "Iniciando Out of the Abyss System..." -ForegroundColor Cyan

# Caminho do venv (está uma pasta acima de System)
$venvPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    Write-Host "Ativando ambiente virtual..." -ForegroundColor Green
    & $venvPath
} else {
    Write-Host "Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv .venv" -ForegroundColor Yellow
    pause
    exit 1
}

# Abre o navegador apos 2 segundos (em background)
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:5000"
} | Out-Null

# Executa o webapp
$appPath = Join-Path $PSScriptRoot "main.py"
Write-Host "Executando aplicacao..." -ForegroundColor Cyan
python $appPath
