# Script para executar o Out of the Abyss System
$ErrorActionPreference = "Stop"

# Verifica se ja tem servidor rodando na porta 5000
$existingProcess = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existingProcess) {
    Write-Host "Servidor ja esta rodando! Abrindo navegador..." -ForegroundColor Yellow
    Start-Process "http://127.0.0.1:5000"
    exit 0
}

Write-Host "Iniciando Out of the Abyss System..." -ForegroundColor Cyan

# Configurar caminhos do ambiente virtual
$projectRoot = Split-Path $PSScriptRoot -Parent
$venvScripts = Join-Path $projectRoot ".venv\Scripts"
$venvPython = Join-Path $venvScripts "python.exe"

if (Test-Path $venvPython) {
    Write-Host "Configurando ambiente virtual..." -ForegroundColor Green
    
    # Configura variáveis de ambiente
    $env:VIRTUAL_ENV = Join-Path $projectRoot ".venv"
    $env:PATH = "$venvScripts;$env:PATH"
    $env:PYTHONPATH = $projectRoot
    
    Write-Host "Ambiente virtual ativado!" -ForegroundColor Green
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
& $venvPython $appPath
