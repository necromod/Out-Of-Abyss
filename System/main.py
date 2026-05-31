"""
Out of the Abyss - Sistema de Mestragem D&D 5e
Ponto de entrada da aplicação

Execute com: python main.py
"""

import sys
import os

# Adiciona o diretório do sistema ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Garante que sys.executable aponta para o Python do venv
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    # Está em um venv
    venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')
    if os.path.exists(venv_python):
        sys.executable = venv_python

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("[SYSTEM] OUT OF THE ABYSS - Sistema de Mestragem")
    print("=" * 50)
    print("[INFO] Servidor iniciando em: http://127.0.0.1:5000")
    print("[INFO] Pressione Ctrl+C para encerrar")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False
    )
