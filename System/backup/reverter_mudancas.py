"""
Script para reverter mudanças feitas pelo Copilot
Restaura os arquivos ao estado original antes das modificações
"""

import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).parent.parent.parent

# Conteúdos originais dos arquivos

RUN_SYSTEM_PS1_ORIGINAL = """# Script para executar o Out of the Abyss System
$ErrorActionPreference = "Stop"

# Verifica se ja tem servidor rodando na porta 5000
$existingProcess = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -First 1
if ($existingProcess) {
    Write-Host "Servidor ja esta rodando! Abrindo navegador..." -ForegroundColor Yellow
    Start-Process "http://127.0.0.1:5000"
    exit 0
}

Write-Host "Iniciando Out of the Abyss System..." -ForegroundColor Cyan

# Caminho do venv (está uma pasta acima de System)
$venvPath = Join-Path (Split-Path $PSScriptRoot -Parent) ".venv\\Scripts\\Activate.ps1"

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
"""

MAIN_PY_ORIGINAL = '''"""
Out of the Abyss - Sistema de Mestragem D&D 5e
Ponto de entrada da aplicação

Execute com: python main.py
"""

import sys
import os

# Adiciona o diretório do sistema ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("⚔️  OUT OF THE ABYSS - Sistema de Mestragem")
    print("=" * 50)
    print("🌐 Servidor iniciando em: http://127.0.0.1:5000")
    print("📖 Pressione Ctrl+C para encerrar")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
'''

# Lista de arquivos para reverter
ARQUIVOS = [
    {
        'caminho': BASE_DIR / 'System' / 'run_system.ps1',
        'conteudo': RUN_SYSTEM_PS1_ORIGINAL,
        'descricao': 'Script PowerShell de inicialização'
    },
    {
        'caminho': BASE_DIR / 'System' / 'main.py',
        'conteudo': MAIN_PY_ORIGINAL,
        'descricao': 'Arquivo principal Python'
    }
]

def reverter_arquivos():
    """Reverte todos os arquivos modificados ao estado original"""
    print("=" * 60)
    print("🔄 REVERTENDO MUDANÇAS DO COPILOT")
    print("=" * 60)
    print()
    
    sucesso = 0
    falha = 0
    
    for arquivo in ARQUIVOS:
        caminho = arquivo['caminho']
        descricao = arquivo['descricao']
        
        try:
            print(f"📝 Revertendo: {descricao}")
            print(f"   Arquivo: {caminho.name}")
            
            # Cria backup do arquivo atual
            if caminho.exists():
                backup_path = caminho.with_suffix(caminho.suffix + '.backup')
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo_atual = f.read()
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(conteudo_atual)
                print(f"   ✅ Backup criado: {backup_path.name}")
            
            # Escreve conteúdo original
            with open(caminho, 'w', encoding='utf-8', newline='\n') as f:
                f.write(arquivo['conteudo'])
            
            print(f"   ✅ Arquivo revertido com sucesso!")
            print()
            sucesso += 1
            
        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            print()
            falha += 1
    
    print("=" * 60)
    print(f"✅ Sucesso: {sucesso} arquivo(s)")
    if falha > 0:
        print(f"❌ Falha: {falha} arquivo(s)")
    print("=" * 60)
    print()
    print("📋 NOTAS:")
    print("- Backups dos arquivos modificados foram criados com extensão .backup")
    print("- O ambiente virtual (.venv) NÃO foi alterado - foi recriado limpo")
    print("- Execute 'python -m venv .venv' novamente se necessário")
    print()

if __name__ == '__main__':
    try:
        reverter_arquivos()
        input("Pressione ENTER para sair...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ ERRO CRÍTICO: {e}")
        input("Pressione ENTER para sair...")
