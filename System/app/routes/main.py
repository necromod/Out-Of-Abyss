"""
Rotas principais da aplicação
"""

from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Página inicial - redireciona para tela de sessão"""
    return render_template('index.html')


@main_bp.route('/config')
def configuracoes():
    """Página de configurações do sistema"""
    regras = current_app.config.get('REGRAS_ATIVAS', {})
    return render_template('config.html', regras=regras)
