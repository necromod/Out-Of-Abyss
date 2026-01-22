"""
Rotas do sistema de combate
"""

from flask import Blueprint, request, jsonify
from ..modulos.combate import SistemaCombate

combate_bp = Blueprint('combate', __name__)

# Instância do sistema de combate (será gerenciada por sessão futuramente)
sistema_combate = SistemaCombate()


@combate_bp.route('/iniciar', methods=['POST'])
def iniciar_combate():
    """Inicia um novo combate"""
    data = request.get_json() or {}
    participantes = data.get('participantes', [])
    
    resultado = sistema_combate.iniciar(participantes)
    return jsonify(resultado)


@combate_bp.route('/iniciativa', methods=['GET', 'POST'])
def ordem_iniciativa():
    """Gerencia a ordem de iniciativa"""
    if request.method == 'POST':
        data = request.get_json()
        resultado = sistema_combate.definir_iniciativa(data)
        return jsonify(resultado)
    else:
        return jsonify(sistema_combate.obter_ordem())


@combate_bp.route('/acao', methods=['POST'])
def executar_acao():
    """Executa uma ação de combate"""
    data = request.get_json()
    
    atacante_id = data.get('atacante_id')
    alvo_id = data.get('alvo_id')
    tipo_acao = data.get('tipo_acao')  # ataque, magia, habilidade, etc
    detalhes = data.get('detalhes', {})
    
    resultado = sistema_combate.executar_acao(
        atacante_id=atacante_id,
        alvo_id=alvo_id,
        tipo_acao=tipo_acao,
        detalhes=detalhes
    )
    
    return jsonify(resultado)


@combate_bp.route('/acao/desfazer', methods=['POST'])
def desfazer_acao():
    """Desfaz a última ação executada"""
    resultado = sistema_combate.desfazer_ultima_acao()
    return jsonify(resultado)


@combate_bp.route('/acao/sobrescrever', methods=['POST'])
def sobrescrever_resultado():
    """Permite ao mestre sobrescrever qualquer resultado"""
    data = request.get_json()
    
    acao_id = data.get('acao_id')
    novos_valores = data.get('valores')
    
    resultado = sistema_combate.sobrescrever_resultado(acao_id, novos_valores)
    return jsonify(resultado)


@combate_bp.route('/turno/proximo', methods=['POST'])
def proximo_turno():
    """Avança para o próximo turno"""
    resultado = sistema_combate.proximo_turno()
    return jsonify(resultado)


@combate_bp.route('/turno/anterior', methods=['POST'])
def turno_anterior():
    """Volta para o turno anterior"""
    resultado = sistema_combate.turno_anterior()
    return jsonify(resultado)


@combate_bp.route('/log', methods=['GET'])
def log_combate():
    """Retorna o log completo do combate"""
    return jsonify(sistema_combate.obter_log())


@combate_bp.route('/finalizar', methods=['POST'])
def finalizar_combate():
    """Finaliza o combate atual"""
    resultado = sistema_combate.finalizar()
    return jsonify(resultado)
