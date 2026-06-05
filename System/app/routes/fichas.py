"""
Rotas para gerenciamento de fichas (personagens, monstros e NPCs)
"""

from flask import Blueprint, request, jsonify, render_template
from ..modulos.repositories import (
    PersonagemRepository, MonstroRepository, 
    InstanciaMonstroRepository, NPCRepository
)
from ..modulos.database import get_connection, json_loads_safe

fichas_bp = Blueprint('fichas', __name__)


# ==================== FUNÇÕES AUXILIARES ====================

def obter_dados_dnd():
    """Busca raças, classes e antecedentes do banco para uso em templates"""
    with get_connection() as conn:
        # Raças agrupadas por fonte
        cursor = conn.execute("""
            SELECT nome, categoria, fonte FROM racas 
            WHERE ativo = 1 ORDER BY fonte, categoria, nome
        """)
        racas_por_fonte = {}
        for row in cursor.fetchall():
            fonte = row['fonte'] or 'PHB'
            if fonte not in racas_por_fonte:
                racas_por_fonte[fonte] = []
            racas_por_fonte[fonte].append({
                'nome': row['nome'],
                'categoria': row['categoria']
            })
        
        # Classes agrupadas por fonte
        cursor = conn.execute("""
            SELECT nome, fonte FROM classes 
            WHERE ativo = 1 ORDER BY fonte, nome
        """)
        classes_por_fonte = {}
        for row in cursor.fetchall():
            fonte = row['fonte'] or 'PHB'
            if fonte not in classes_por_fonte:
                classes_por_fonte[fonte] = []
            classes_por_fonte[fonte].append(row['nome'])
        
        # Antecedentes agrupados por fonte
        cursor = conn.execute("""
            SELECT nome, fonte FROM antecedentes 
            WHERE ativo = 1 ORDER BY fonte, nome
        """)
        antecedentes_por_fonte = {}
        for row in cursor.fetchall():
            fonte = row['fonte'] or 'PHB'
            if fonte not in antecedentes_por_fonte:
                antecedentes_por_fonte[fonte] = []
            antecedentes_por_fonte[fonte].append(row['nome'])
    
    return {
        'racas': racas_por_fonte,
        'classes': classes_por_fonte,
        'antecedentes': antecedentes_por_fonte
    }


# ==================== PÁGINAS HTML ====================

# --- PERSONAGENS ---

@fichas_bp.route('/personagens')
def lista_personagens():
    """Página de lista de personagens"""
    return render_template('fichas/lista_personagens.html')


@fichas_bp.route('/personagem/novo')
def novo_personagem():
    """Página para criar novo personagem"""
    dados_dnd = obter_dados_dnd()
    return render_template('fichas/personagem.html', personagem=None, **dados_dnd)


@fichas_bp.route('/personagem/<int:id>')
def ver_personagem(id):
    """Página de visualização de personagem"""
    personagem = PersonagemRepository.get_by_id(id)
    if not personagem:
        return render_template('erro.html', mensagem='Personagem não encontrado'), 404
    dados_dnd = obter_dados_dnd()
    return render_template('fichas/personagem.html', personagem=personagem, **dados_dnd)


@fichas_bp.route('/personagem/<int:id>/editar')
def editar_personagem(id):
    """Página de edição de personagem"""
    personagem = PersonagemRepository.get_by_id(id)
    if not personagem:
        return render_template('erro.html', mensagem='Personagem não encontrado'), 404
    dados_dnd = obter_dados_dnd()
    return render_template('fichas/personagem.html', personagem=personagem, modo_edicao=True, **dados_dnd)


# --- MONSTROS ---

@fichas_bp.route('/monstros')
def lista_monstros():
    """Página de lista de monstros (bestiário)"""
    return render_template('fichas/lista_monstros.html')


@fichas_bp.route('/monstro/novo')
def novo_monstro():
    """Página para criar novo monstro"""
    return render_template('fichas/monstro.html', monstro=None)


@fichas_bp.route('/monstro/<int:id>')
def ver_monstro(id):
    """Página de visualização de monstro"""
    monstro = MonstroRepository.get_by_id(id)
    if not monstro:
        return render_template('erro.html', mensagem='Monstro não encontrado'), 404
    return render_template('fichas/monstro.html', monstro=monstro)


# --- NPCs ---

@fichas_bp.route('/npcs')
def lista_npcs():
    """Página de lista de NPCs"""
    return render_template('fichas/lista_npcs.html')


@fichas_bp.route('/npc/novo')
def novo_npc():
    """Página para criar novo NPC"""
    return render_template('fichas/npc.html', npc=None)


@fichas_bp.route('/npc/<int:id>')
def ver_npc(id):
    """Página de visualização de NPC"""
    npc = NPCRepository.get_by_id(id)
    if not npc:
        return render_template('erro.html', mensagem='NPC não encontrado'), 404
    return render_template('fichas/npc.html', npc=npc)


@fichas_bp.route('/npc/<int:id>/editar')
def editar_npc(id):
    """Página de edição de NPC"""
    npc = NPCRepository.get_by_id(id)
    if not npc:
        return render_template('erro.html', mensagem='NPC não encontrado'), 404
    return render_template('fichas/npc.html', npc=npc, modo_edicao=True)


# ==================== WIDGETS HTML (para sessão) ====================

@fichas_bp.route('/widget/personagem/<int:id>')
def widget_personagem(id):
    """Retorna HTML do widget compacto de ficha de personagem"""
    personagem = PersonagemRepository.get_by_id(id)
    return render_template('widgets/ficha_personagem.html', personagem=personagem)


@fichas_bp.route('/widget/monstro/<int:id>')
def widget_monstro(id):
    """Retorna HTML do widget compacto de ficha de monstro"""
    monstro = MonstroRepository.get_by_id(id)
    return render_template('widgets/ficha_monstro.html', monstro=monstro)


@fichas_bp.route('/widget/monstro-instancia/<int:id>')
def widget_monstro_instancia(id):
    """Retorna HTML do widget de instância de monstro em combate"""
    instancia = InstanciaMonstroRepository.get_completo(id)
    return render_template('widgets/ficha_monstro.html', monstro=instancia, instancia=True)


@fichas_bp.route('/widget/npc/<int:id>')
def widget_npc(id):
    """Retorna HTML do widget compacto de NPC"""
    npc = NPCRepository.get_by_id(id)
    return render_template('widgets/ficha_npc.html', npc=npc)


# ==================== API - PERSONAGENS ====================

@fichas_bp.route('/api/personagens', methods=['GET'])
def api_listar_personagens():
    """Lista todos os personagens"""
    personagens = PersonagemRepository.get_all()
    return jsonify(personagens)


@fichas_bp.route('/api/personagem', methods=['POST'])
def api_criar_personagem():
    """Cria um novo personagem"""
    data = request.get_json()
    resultado = PersonagemRepository.criar(data)
    return jsonify(resultado)


@fichas_bp.route('/api/personagem/<int:id>', methods=['GET'])
def api_obter_personagem(id):
    """Obtém ficha completa de um personagem"""
    personagem = PersonagemRepository.get_by_id(id)
    if personagem:
        return jsonify(personagem)
    return jsonify({'erro': 'Personagem não encontrado'}), 404


@fichas_bp.route('/api/personagem/<int:id>', methods=['PUT', 'PATCH'])
def api_atualizar_personagem(id):
    """Atualiza dados de um personagem"""
    data = request.get_json()
    # Debug: ver dados recebidos
    print(f"[INFO] Recebido para personagem {id}:")
    print(f"   armas: {data.get('armas')}")
    print(f"   equipamentos: {data.get('equipamentos')}")
    resultado = PersonagemRepository.atualizar(id, data)
    return jsonify(resultado)


@fichas_bp.route('/api/personagem/<int:id>', methods=['DELETE'])
def api_deletar_personagem(id):
    """Remove um personagem"""
    resultado = PersonagemRepository.delete(id)
    return jsonify({'sucesso': resultado})


@fichas_bp.route('/api/personagem/<int:id>/campo', methods=['PATCH'])
def api_editar_campo_personagem(id):
    """Edita um campo específico do personagem em tempo real"""
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')
    resultado = PersonagemRepository.atualizar_campo(id, campo, valor)
    return jsonify(resultado)


# ==================== API - MONSTROS ====================

@fichas_bp.route('/api/monstros', methods=['GET'])
def api_listar_monstros():
    """Lista todos os monstros do bestiário"""
    monstros = MonstroRepository.get_all()
    return jsonify(monstros)


@fichas_bp.route('/api/monstro', methods=['POST'])
def api_criar_monstro():
    """Cria um novo monstro no bestiário"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não recebidos'}), 400
        if not data.get('nome'):
            return jsonify({'erro': 'Nome é obrigatório'}), 400
        
        resultado = MonstroRepository.criar(data)
        return jsonify(resultado)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500


@fichas_bp.route('/api/monstro/<int:id>', methods=['GET'])
def api_obter_monstro(id):
    """Obtém ficha completa de um monstro"""
    monstro = MonstroRepository.get_by_id(id)
    if monstro:
        return jsonify(monstro)
    return jsonify({'erro': 'Monstro não encontrado'}), 404


@fichas_bp.route('/api/monstro/<int:id>', methods=['PUT', 'PATCH'])
def api_atualizar_monstro(id):
    """Atualiza dados de um monstro"""
    try:
        data = request.get_json()
        resultado = MonstroRepository.atualizar(id, data)
        if resultado:
            return jsonify(resultado)
        return jsonify({'erro': 'Monstro não encontrado'}), 404
    except Exception as e:
        print(f"[ERRO] Erro ao atualizar monstro {id}: {e}")
        return jsonify({'erro': str(e)}), 500


@fichas_bp.route('/api/monstro/<int:id>', methods=['DELETE'])
def api_deletar_monstro(id):
    """Remove um monstro"""
    resultado = MonstroRepository.delete(id)
    return jsonify({'sucesso': resultado})


# ==================== API - INSTÂNCIAS DE MONSTRO ====================

@fichas_bp.route('/api/monstro/instancia', methods=['POST'])
def api_criar_instancia_monstro():
    """Cria uma instância de monstro para combate"""
    data = request.get_json()
    monstro_id = data.get('monstro_id')
    nome = data.get('nome')
    sessao_id = data.get('sessao_id')
    
    resultado = InstanciaMonstroRepository.criar_instancia(monstro_id, nome, sessao_id)
    if not resultado:
        return jsonify({'erro': 'Monstro base não encontrado'}), 404
    return jsonify(resultado)


@fichas_bp.route('/api/monstro/instancia/<int:id>', methods=['GET'])
def api_obter_instancia_monstro(id):
    """Obtém uma instância de monstro com dados completos"""
    instancia = InstanciaMonstroRepository.get_completo(id)
    if instancia:
        return jsonify(instancia)
    return jsonify({'erro': 'Instância não encontrada'}), 404


@fichas_bp.route('/api/monstro/instancia/<int:id>', methods=['PATCH'])
def api_atualizar_instancia_monstro(id):
    """Atualiza campos de uma instância de monstro"""
    data = request.get_json()
    InstanciaMonstroRepository.update(id, data)
    resultado = InstanciaMonstroRepository.get_completo(id)
    return jsonify(resultado)


@fichas_bp.route('/api/monstro/instancia/<int:id>/campo', methods=['PATCH'])
def api_editar_campo_instancia(id):
    """Edita um campo específico da instância de monstro"""
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')
    InstanciaMonstroRepository.update(id, {campo: valor})
    resultado = InstanciaMonstroRepository.get_completo(id)
    return jsonify(resultado)


# ==================== API - NPCs ====================

@fichas_bp.route('/api/npcs', methods=['GET'])
def api_listar_npcs():
    """Lista todos os NPCs"""
    npcs = NPCRepository.get_all()
    return jsonify(npcs)


@fichas_bp.route('/api/npc', methods=['POST'])
def api_criar_npc():
    """Cria um novo NPC"""
    data = request.get_json()
    id = NPCRepository.insert(data)
    resultado = NPCRepository.get_by_id(id)
    return jsonify(resultado)


@fichas_bp.route('/api/npc/<int:id>', methods=['GET'])
def api_obter_npc(id):
    """Obtém ficha completa de um NPC"""
    npc = NPCRepository.get_by_id(id)
    if npc:
        return jsonify(npc)
    return jsonify({'erro': 'NPC não encontrado'}), 404


@fichas_bp.route('/api/npc/<int:id>', methods=['PUT', 'PATCH'])
def api_atualizar_npc(id):
    """Atualiza dados de um NPC"""
    data = request.get_json()
    NPCRepository.update(id, data)
    resultado = NPCRepository.get_by_id(id)
    return jsonify(resultado)


@fichas_bp.route('/api/npc/<int:id>', methods=['DELETE'])
def api_deletar_npc(id):
    """Remove um NPC"""
    resultado = NPCRepository.delete(id)
    return jsonify({'sucesso': resultado})


@fichas_bp.route('/api/npc/<int:id>/campo', methods=['PATCH'])
def api_editar_campo_npc(id):
    """Edita um campo específico do NPC em tempo real"""
    data = request.get_json()
    campo = data.get('campo')
    valor = data.get('valor')
    NPCRepository.update(id, {campo: valor})
    resultado = NPCRepository.get_by_id(id)
    return jsonify(resultado)
