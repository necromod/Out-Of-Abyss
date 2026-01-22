"""
Rotas para gerenciamento de fichas (personagens e monstros)
"""

from flask import Blueprint, request, jsonify, render_template
from ..modulos.fichas_personagens import GerenciadorPersonagens
from ..modulos.fichas_monstros import GerenciadorMonstros

fichas_bp = Blueprint('fichas', __name__)

gerenciador_personagens = GerenciadorPersonagens()
gerenciador_monstros = GerenciadorMonstros()


# ==================== PERSONAGENS ====================

@fichas_bp.route('/personagens', methods=['GET'])
def listar_personagens():
    """Lista todos os personagens"""
    personagens = gerenciador_personagens.listar_todos()
    return jsonify(personagens)


@fichas_bp.route('/personagem/<string:id>', methods=['GET'])
def obter_personagem(id):
    """Obtém ficha completa de um personagem"""
    personagem = gerenciador_personagens.obter(id)
    if personagem:
        return jsonify(personagem)
    return jsonify({'erro': 'Personagem não encontrado'}), 404


@fichas_bp.route('/personagem', methods=['POST'])
def criar_personagem():
    """Cria um novo personagem"""
    data = request.get_json()
    resultado = gerenciador_personagens.criar(data)
    return jsonify(resultado)


@fichas_bp.route('/personagem/<string:id>', methods=['PUT', 'PATCH'])
def atualizar_personagem(id):
    """Atualiza dados de um personagem (parcial ou completo)"""
    data = request.get_json()
    resultado = gerenciador_personagens.atualizar(id, data)
    return jsonify(resultado)


@fichas_bp.route('/personagem/<string:id>/atributo', methods=['PATCH'])
def editar_atributo_personagem(id):
    """Edita um atributo específico em tempo real"""
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')
    
    resultado = gerenciador_personagens.editar_campo(id, campo, valor)
    return jsonify(resultado)


# ==================== MONSTROS ====================

@fichas_bp.route('/monstros', methods=['GET'])
def listar_monstros():
    """Lista todos os monstros disponíveis"""
    monstros = gerenciador_monstros.listar_todos()
    return jsonify(monstros)


@fichas_bp.route('/monstro/<string:id>', methods=['GET'])
def obter_monstro(id):
    """Obtém ficha completa de um monstro"""
    monstro = gerenciador_monstros.obter(id)
    if monstro:
        return jsonify(monstro)
    return jsonify({'erro': 'Monstro não encontrado'}), 404


@fichas_bp.route('/monstro/instancia', methods=['POST'])
def criar_instancia_monstro():
    """Cria uma instância de monstro para combate (com HP próprio, etc)"""
    data = request.get_json()
    monstro_base_id = data.get('monstro_id')
    nome_instancia = data.get('nome')  # Ex: "Goblin 1", "Goblin 2"
    
    resultado = gerenciador_monstros.criar_instancia(monstro_base_id, nome_instancia)
    return jsonify(resultado)


@fichas_bp.route('/monstro/instancia/<string:id>/atributo', methods=['PATCH'])
def editar_atributo_monstro(id):
    """Edita um atributo específico de uma instância de monstro"""
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')
    
    resultado = gerenciador_monstros.editar_campo_instancia(id, campo, valor)
    return jsonify(resultado)


# ==================== WIDGETS HTML ====================

@fichas_bp.route('/widget/personagem/<string:id>')
def widget_personagem(id):
    """Retorna HTML do widget de ficha de personagem"""
    personagem = gerenciador_personagens.obter(id)
    return render_template('widgets/ficha_personagem.html', personagem=personagem)


@fichas_bp.route('/widget/monstro/<string:id>')
def widget_monstro(id):
    """Retorna HTML do widget de ficha de monstro"""
    monstro = gerenciador_monstros.obter(id)
    return render_template('widgets/ficha_monstro.html', monstro=monstro)
