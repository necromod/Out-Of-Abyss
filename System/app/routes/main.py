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


@main_bp.route('/notas/<int:nota_id>')
def janela_nota(nota_id):
    """Página standalone para edição de uma nota em janela externa"""
    from ..modulos.repositories import NotasSessaoRepository
    nota = NotasSessaoRepository.get_by_id(nota_id)
    if not nota:
        return render_template('erro.html', mensagem='Nota não encontrada'), 404
    return render_template('notas/janela.html', nota=nota)
