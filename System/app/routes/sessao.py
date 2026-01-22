"""
Rotas da Tela de Sessão - principal área de mestragem
"""

from flask import Blueprint, render_template, request, jsonify

sessao_bp = Blueprint('sessao', __name__)


@sessao_bp.route('/')
def tela_sessao():
    """Tela principal de sessão - usada durante o jogo ao vivo"""
    return render_template('sessao/tela_sessao.html')


@sessao_bp.route('/widgets', methods=['GET'])
def listar_widgets():
    """Lista todos os widgets disponíveis para a tela de sessão"""
    widgets_disponiveis = [
        {'id': 'ficha_personagem', 'nome': 'Ficha de Personagem', 'icone': 'user'},
        {'id': 'ficha_monstro', 'nome': 'Ficha de Monstro', 'icone': 'skull'},
        {'id': 'lista_monstros', 'nome': 'Lista de Monstros', 'icone': 'list'},
        {'id': 'npcs', 'nome': 'NPCs', 'icone': 'users'},
        {'id': 'itens', 'nome': 'Itens', 'icone': 'box'},
        {'id': 'magias', 'nome': 'Magias', 'icone': 'sparkles'},
        {'id': 'condicoes', 'nome': 'Condições', 'icone': 'alert-circle'},
        {'id': 'regras', 'nome': 'Regras Rápidas', 'icone': 'book'},
        {'id': 'notas', 'nome': 'Notas', 'icone': 'edit'},
        {'id': 'log_combate', 'nome': 'Log de Combate', 'icone': 'scroll'},
        {'id': 'iniciativa', 'nome': 'Ordem de Iniciativa', 'icone': 'clock'},
    ]
    return jsonify(widgets_disponiveis)


@sessao_bp.route('/mapa', methods=['POST'])
def alterar_mapa():
    """Altera o mapa de fundo da tela de sessão"""
    # Recebe path da imagem ou upload
    data = request.get_json()
    caminho_mapa = data.get('caminho')
    
    # TODO: Validar se o arquivo existe
    # TODO: Salvar estado da sessão
    
    return jsonify({'sucesso': True, 'mapa': caminho_mapa})


@sessao_bp.route('/estado', methods=['GET', 'POST'])
def estado_sessao():
    """Salva ou recupera o estado atual da sessão (posição dos widgets, etc)"""
    if request.method == 'POST':
        estado = request.get_json()
        # TODO: Persistir estado em arquivo JSON
        return jsonify({'sucesso': True})
    else:
        # TODO: Recuperar estado salvo
        return jsonify({'widgets': [], 'mapa': None})
