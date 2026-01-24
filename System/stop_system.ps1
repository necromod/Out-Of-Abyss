# Script para parar o Out of the Abyss System
$ErrorActionPreference = "SilentlyContinue"

Write-Host "Procurando servidor Flask na porta 5000..." -ForegroundColor Cyan

# Encontra processos usando a porta 5000
$connections = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue

if ($connections) {
    # Filtra PIDs válidos (ignora 0 e 4 que são processos do sistema)
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique | Where-Object { $_ -gt 4 }
    
    if ($processIds) {
        foreach ($procId in $processIds) {
            $process = Get-Process -Id $procId -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "Encerrando processo: $($process.Name) (PID: $procId)" -ForegroundColor Yellow
                Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
            }
        }
        Write-Host "Servidor Flask encerrado com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "Nenhum processo de usuario na porta 5000." -ForegroundColor Yellow
    }
} else {
    Write-Host "Nenhum servidor rodando na porta 5000." -ForegroundColor Yellow
}

pause
