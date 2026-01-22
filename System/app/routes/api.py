"""
API REST para comunicação com o frontend
Endpoints gerais e utilitários
"""

from flask import Blueprint, request, jsonify, current_app
import os

api_bp = Blueprint('api', __name__)


@api_bp.route('/status')
def status():
    """Verifica se o sistema está funcionando"""
    return jsonify({
        'status': 'online',
        'sistema': 'Out of the Abyss - Sistema de Mestragem',
        'versao': '0.1.0'
    })


@api_bp.route('/regras', methods=['GET', 'POST'])
def configurar_regras():
    """Obtém ou altera configurações de regras ativas"""
    from ..modulos.database import get_connection
    
    if request.method == 'POST':
        data = request.get_json()
        with get_connection() as conn:
            for chave, valor in data.items():
                conn.execute(
                    "INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES (?, ?)",
                    (f"regras_{chave}", str(int(valor)))
                )
        return jsonify({'sucesso': True, 'regras': data})
    else:
        with get_connection() as conn:
            cursor = conn.execute("SELECT chave, valor FROM configuracoes WHERE chave LIKE 'regras_%'")
            regras = {}
            for row in cursor:
                chave = row['chave'].replace('regras_', '')
                regras[chave] = row['valor'] == '1'
        return jsonify(regras)


@api_bp.route('/imagens/cenarios')
def listar_cenarios():
    """Lista imagens disponíveis para mapas de batalha"""
    imagens_dir = current_app.config.get('IMAGENS_DIR')
    cenarios_dir = os.path.join(imagens_dir, 'Cenários')
    
    if not os.path.exists(cenarios_dir):
        return jsonify([])
    
    imagens = []
    extensoes_validas = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    for arquivo in os.listdir(cenarios_dir):
        ext = os.path.splitext(arquivo)[1].lower()
        if ext in extensoes_validas:
            imagens.append({
                'nome': arquivo,
                'caminho': os.path.join(cenarios_dir, arquivo)
            })
    
    return jsonify(imagens)


@api_bp.route('/imagens/npcs')
def listar_imagens_npcs():
    """Lista imagens de NPCs disponíveis"""
    npcs_dir = current_app.config.get('NPCS_DIR')
    
    if not os.path.exists(npcs_dir):
        return jsonify([])
    
    imagens = []
    extensoes_validas = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    for root, dirs, files in os.walk(npcs_dir):
        for arquivo in files:
            ext = os.path.splitext(arquivo)[1].lower()
            if ext in extensoes_validas:
                caminho_completo = os.path.join(root, arquivo)
                caminho_relativo = os.path.relpath(caminho_completo, npcs_dir)
                imagens.append({
                    'nome': arquivo,
                    'caminho': caminho_completo,
                    'relativo': caminho_relativo
                })
    
    return jsonify(imagens)


@api_bp.route('/dados/rolar', methods=['POST'])
def rolar_dados():
    """Rola dados - endpoint utilitário"""
    from ..modulos.dados import rolar_expressao
    
    data = request.get_json()
    expressao = data.get('expressao', '1d20')  # Ex: "2d6+3", "1d20", "4d8-2"
    
    resultado = rolar_expressao(expressao)
    return jsonify(resultado)


# ==================== REGRAS D&D 5e ====================

@api_bp.route('/dnd/racas')
def listar_racas():
    """Lista todas as raças disponíveis"""
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT * FROM racas WHERE ativo = 1 ORDER BY categoria, nome
        """)
        racas = []
        for row in cursor.fetchall():
            raca = dict(row)
            # Parse JSON fields
            raca['bonus_atributos'] = json_loads_safe(raca['bonus_atributos'], {})
            raca['idiomas'] = json_loads_safe(raca['idiomas'], [])
            raca['proficiencias_armas'] = json_loads_safe(raca['proficiencias_armas'], [])
            raca['proficiencias_armaduras'] = json_loads_safe(raca['proficiencias_armaduras'], [])
            raca['proficiencias_ferramentas'] = json_loads_safe(raca['proficiencias_ferramentas'], [])
            raca['pericias_bonus'] = json_loads_safe(raca['pericias_bonus'], [])
            raca['caracteristicas'] = json_loads_safe(raca['caracteristicas'], [])
            raca['resistencias'] = json_loads_safe(raca['resistencias'], [])
            raca['imunidades'] = json_loads_safe(raca['imunidades'], [])
            raca['pericias_opcoes'] = json_loads_safe(raca['pericias_opcoes'], [])
            racas.append(raca)
    
    return jsonify(racas)


@api_bp.route('/dnd/racas/<int:id>')
def obter_raca(id):
    """Obtém uma raça específica"""
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM racas WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'erro': 'Raça não encontrada'}), 404
        
        raca = dict(row)
        raca['bonus_atributos'] = json_loads_safe(raca['bonus_atributos'], {})
        raca['idiomas'] = json_loads_safe(raca['idiomas'], [])
        raca['proficiencias_armas'] = json_loads_safe(raca['proficiencias_armas'], [])
        raca['proficiencias_armaduras'] = json_loads_safe(raca['proficiencias_armaduras'], [])
        raca['proficiencias_ferramentas'] = json_loads_safe(raca['proficiencias_ferramentas'], [])
        raca['pericias_bonus'] = json_loads_safe(raca['pericias_bonus'], [])
        raca['caracteristicas'] = json_loads_safe(raca['caracteristicas'], [])
        raca['resistencias'] = json_loads_safe(raca['resistencias'], [])
        raca['imunidades'] = json_loads_safe(raca['imunidades'], [])
        raca['pericias_opcoes'] = json_loads_safe(raca['pericias_opcoes'], [])
    
    return jsonify(raca)


@api_bp.route('/dnd/classes')
def listar_classes():
    """Lista todas as classes disponíveis"""
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM classes WHERE ativo = 1 ORDER BY nome")
        classes = []
        for row in cursor.fetchall():
            classe = dict(row)
            classe['salvaguardas_proficientes'] = json_loads_safe(classe['salvaguardas_proficientes'], [])
            classe['armaduras'] = json_loads_safe(classe['armaduras'], [])
            classe['armas'] = json_loads_safe(classe['armas'], [])
            classe['ferramentas'] = json_loads_safe(classe['ferramentas'], [])
            classe['pericias_disponiveis'] = json_loads_safe(classe['pericias_disponiveis'], [])
            classe['caracteristicas_nivel_1'] = json_loads_safe(classe['caracteristicas_nivel_1'], [])
            classes.append(classe)
    
    return jsonify(classes)


@api_bp.route('/dnd/classes/<int:id>')
def obter_classe(id):
    """Obtém uma classe específica"""
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM classes WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'erro': 'Classe não encontrada'}), 404
        
        classe = dict(row)
        classe['salvaguardas_proficientes'] = json_loads_safe(classe['salvaguardas_proficientes'], [])
        classe['armaduras'] = json_loads_safe(classe['armaduras'], [])
        classe['armas'] = json_loads_safe(classe['armas'], [])
        classe['ferramentas'] = json_loads_safe(classe['ferramentas'], [])
        classe['pericias_disponiveis'] = json_loads_safe(classe['pericias_disponiveis'], [])
        classe['caracteristicas_nivel_1'] = json_loads_safe(classe['caracteristicas_nivel_1'], [])
    
    return jsonify(classe)


@api_bp.route('/dnd/pericias')
def listar_pericias():
    """Lista todas as perícias"""
    from ..modulos.database import get_connection
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM pericias ORDER BY nome_display")
        pericias = [dict(row) for row in cursor.fetchall()]
    
    return jsonify(pericias)


@api_bp.route('/dnd/idiomas')
def listar_idiomas():
    """Lista todos os idiomas"""
    from ..modulos.database import get_connection
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM idiomas ORDER BY tipo, nome")
        idiomas = [dict(row) for row in cursor.fetchall()]
    
    return jsonify(idiomas)


@api_bp.route('/dnd/antecedentes')
def listar_antecedentes():
    """Lista todos os antecedentes"""
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM antecedentes WHERE ativo = 1 ORDER BY nome")
        antecedentes = []
        for row in cursor.fetchall():
            ant = dict(row)
            ant['pericias'] = json_loads_safe(ant['pericias'], [])
            ant['ferramentas'] = json_loads_safe(ant['ferramentas'], [])
            antecedentes.append(ant)
    
    return jsonify(antecedentes)


@api_bp.route('/dnd/regras-completas')
def obter_regras_completas():
    """
    Retorna todas as regras D&D em uma única requisição.
    Ideal para cache inicial no frontend.
    """
    from ..modulos.database import get_connection, json_loads_safe
    
    with get_connection() as conn:
        # Raças
        cursor = conn.execute("SELECT * FROM racas WHERE ativo = 1")
        racas = {}
        for row in cursor.fetchall():
            raca = dict(row)
            raca['bonus_atributos'] = json_loads_safe(raca['bonus_atributos'], {})
            raca['idiomas'] = json_loads_safe(raca['idiomas'], [])
            raca['proficiencias_armas'] = json_loads_safe(raca['proficiencias_armas'], [])
            raca['proficiencias_armaduras'] = json_loads_safe(raca['proficiencias_armaduras'], [])
            raca['proficiencias_ferramentas'] = json_loads_safe(raca['proficiencias_ferramentas'], [])
            raca['pericias_bonus'] = json_loads_safe(raca['pericias_bonus'], [])
            raca['caracteristicas'] = json_loads_safe(raca['caracteristicas'], [])
            raca['resistencias'] = json_loads_safe(raca['resistencias'], [])
            raca['imunidades'] = json_loads_safe(raca['imunidades'], [])
            raca['pericias_opcoes'] = json_loads_safe(raca['pericias_opcoes'], [])
            racas[raca['nome']] = raca
        
        # Classes
        cursor = conn.execute("SELECT * FROM classes WHERE ativo = 1")
        classes = {}
        for row in cursor.fetchall():
            classe = dict(row)
            classe['salvaguardas_proficientes'] = json_loads_safe(classe['salvaguardas_proficientes'], [])
            classe['armaduras'] = json_loads_safe(classe['armaduras'], [])
            classe['armas'] = json_loads_safe(classe['armas'], [])
            classe['ferramentas'] = json_loads_safe(classe['ferramentas'], [])
            classe['pericias_disponiveis'] = json_loads_safe(classe['pericias_disponiveis'], [])
            classe['caracteristicas_nivel_1'] = json_loads_safe(classe['caracteristicas_nivel_1'], [])
            classes[classe['nome']] = classe
        
        # Perícias
        cursor = conn.execute("SELECT * FROM pericias")
        pericias = {}
        for row in cursor.fetchall():
            p = dict(row)
            pericias[p['nome']] = p
        
        # Idiomas
        cursor = conn.execute("SELECT * FROM idiomas")
        idiomas = [dict(row) for row in cursor.fetchall()]
        
        # Antecedentes
        cursor = conn.execute("SELECT * FROM antecedentes WHERE ativo = 1")
        antecedentes = {}
        for row in cursor.fetchall():
            ant = dict(row)
            ant['pericias'] = json_loads_safe(ant['pericias'], [])
            ant['ferramentas'] = json_loads_safe(ant['ferramentas'], [])
            antecedentes[ant['nome']] = ant
    
    return jsonify({
        'racas': racas,
        'classes': classes,
        'pericias': pericias,
        'idiomas': idiomas,
        'antecedentes': antecedentes,
        # Constantes para criação de personagem
        'point_buy': {
            'pontos_disponiveis': 27,
            'valor_minimo': 8,
            'valor_maximo': 15,
            'custos': {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
        },
        'array_padrao': [15, 14, 13, 12, 10, 8],
        'atributos': ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma'],
        'atributos_display': {
            'forca': 'Força',
            'destreza': 'Destreza',
            'constituicao': 'Constituição',
            'inteligencia': 'Inteligência',
            'sabedoria': 'Sabedoria',
            'carisma': 'Carisma'
        }
    })


# ==================== MONSTROS ====================

@api_bp.route('/monstros')
def listar_monstros():
    """Lista todos os monstros cadastrados"""
    from ..modulos.repositories import MonstroRepository
    
    nome = request.args.get('nome')
    nd_min = request.args.get('nd_min', type=float)
    nd_max = request.args.get('nd_max', type=float)
    
    if nome:
        monstros = MonstroRepository.buscar_por_nome(nome)
    elif nd_min is not None and nd_max is not None:
        monstros = MonstroRepository.buscar_por_nd(nd_min, nd_max)
    else:
        monstros = MonstroRepository.get_all()
    
    return jsonify(monstros)


@api_bp.route('/monstros/<int:id>')
def obter_monstro(id):
    """Obtém um monstro específico"""
    from ..modulos.repositories import MonstroRepository
    
    monstro = MonstroRepository.get_by_id(id)
    if not monstro:
        return jsonify({'erro': 'Monstro não encontrado'}), 404
    return jsonify(monstro)


@api_bp.route('/monstros/instanciar', methods=['POST'])
def criar_instancia_monstro():
    """Cria uma instância de monstro para combate"""
    from ..modulos.repositories import InstanciaMonstroRepository
    
    data = request.get_json()
    monstro_id = data.get('monstro_id')
    nome = data.get('nome')
    sessao_id = data.get('sessao_id')
    
    instancia = InstanciaMonstroRepository.criar_instancia(monstro_id, nome, sessao_id)
    if not instancia:
        return jsonify({'erro': 'Monstro base não encontrado'}), 404
    
    return jsonify(instancia)


# ==================== NPCs ====================

@api_bp.route('/npcs')
def listar_npcs():
    """Lista NPCs conhecidos"""
    from ..modulos.repositories import NPCRepository
    
    apenas_conhecidos = request.args.get('conhecidos', '1') == '1'
    local = request.args.get('local')
    
    if local:
        npcs = NPCRepository.get_por_localizacao(local)
    elif apenas_conhecidos:
        npcs = NPCRepository.get_conhecidos()
    else:
        npcs = NPCRepository.get_all()
    
    return jsonify(npcs)


@api_bp.route('/npcs/<int:id>')
def obter_npc(id):
    """Obtém um NPC específico"""
    from ..modulos.repositories import NPCRepository
    
    npc = NPCRepository.get_by_id(id)
    if not npc:
        return jsonify({'erro': 'NPC não encontrado'}), 404
    return jsonify(npc)


@api_bp.route('/npcs/<int:id>', methods=['PATCH'])
def atualizar_npc(id):
    """Atualiza campos de um NPC"""
    from ..modulos.repositories import NPCRepository
    
    data = request.get_json()
    NPCRepository.update(id, data)
    return jsonify(NPCRepository.get_by_id(id))


# ==================== PERSONAGENS ====================

@api_bp.route('/personagens')
def listar_personagens():
    """Lista personagens ativos"""
    from ..modulos.repositories import PersonagemRepository
    
    personagens = PersonagemRepository.get_all_ativos()
    return jsonify(personagens)


@api_bp.route('/personagens/<int:id>')
def obter_personagem(id):
    """Obtém um personagem específico"""
    from ..modulos.repositories import PersonagemRepository
    
    personagem = PersonagemRepository.get_by_id(id)
    if not personagem:
        return jsonify({'erro': 'Personagem não encontrado'}), 404
    return jsonify(personagem)


@api_bp.route('/personagens', methods=['POST'])
def criar_personagem():
    """Cria um novo personagem"""
    from ..modulos.repositories import PersonagemRepository
    
    data = request.get_json()
    personagem = PersonagemRepository.criar(data)
    return jsonify(personagem), 201


@api_bp.route('/personagens/<int:id>', methods=['PATCH'])
def atualizar_personagem(id):
    """Atualiza campos de um personagem"""
    from ..modulos.repositories import PersonagemRepository
    
    data = request.get_json()
    personagem = PersonagemRepository.atualizar(id, data)
    return jsonify(personagem)


@api_bp.route('/personagens/<int:id>/dano', methods=['POST'])
def aplicar_dano_personagem(id):
    """Aplica dano a um personagem"""
    from ..modulos.repositories import PersonagemRepository
    
    data = request.get_json()
    dano = data.get('dano', 0)
    personagem = PersonagemRepository.aplicar_dano(id, dano)
    if not personagem:
        return jsonify({'erro': 'Personagem não encontrado'}), 404
    return jsonify(personagem)


@api_bp.route('/personagens/<int:id>/curar', methods=['POST'])
def curar_personagem(id):
    """Cura um personagem"""
    from ..modulos.repositories import PersonagemRepository
    
    data = request.get_json()
    quantidade = data.get('quantidade', 0)
    personagem = PersonagemRepository.curar(id, quantidade)
    if not personagem:
        return jsonify({'erro': 'Personagem não encontrado'}), 404
    return jsonify(personagem)


# ==================== SESSÕES ====================

@api_bp.route('/sessoes')
def listar_sessoes():
    """Lista todas as sessões"""
    from ..modulos.repositories import SessaoRepository
    
    sessoes = SessaoRepository.get_all()
    return jsonify(sessoes)


@api_bp.route('/sessoes/atual')
def obter_sessao_atual():
    """Obtém a última sessão"""
    from ..modulos.repositories import SessaoRepository
    
    sessao = SessaoRepository.get_ultima()
    if not sessao:
        return jsonify({'erro': 'Nenhuma sessão encontrada'}), 404
    return jsonify(sessao)


@api_bp.route('/sessoes', methods=['POST'])
def criar_sessao():
    """Cria uma nova sessão"""
    from ..modulos.repositories import SessaoRepository
    
    data = request.get_json()
    numero = data.get('numero')
    titulo = data.get('titulo')
    
    sessao = SessaoRepository.criar_sessao(numero, titulo)
    return jsonify(sessao), 201


# ==================== LOG DE AÇÕES ====================

@api_bp.route('/log/acao', methods=['POST'])
def registrar_acao():
    """Registra uma ação no log"""
    from ..modulos.repositories import AcaoLogRepository
    
    data = request.get_json()
    acao = AcaoLogRepository.registrar(data)
    return jsonify(acao), 201


@api_bp.route('/log/estatisticas/<int:personagem_id>')
def estatisticas_personagem(personagem_id):
    """Retorna estatísticas de um personagem"""
    from ..modulos.repositories import AcaoLogRepository
    
    stats = AcaoLogRepository.estatisticas_personagem(personagem_id)
    return jsonify(stats)


# ==================== API DE FICHAS ====================
# Rotas de compatibilidade para os templates

@api_bp.route('/personagens', methods=['GET'])
def api_personagens():
    """Lista todos os personagens"""
    from ..modulos.repositories import PersonagemRepository
    personagens = PersonagemRepository.get_all()
    return jsonify(personagens)


@api_bp.route('/monstros', methods=['GET'])
def api_monstros():
    """Lista todos os monstros"""
    from ..modulos.repositories import MonstroRepository
    monstros = MonstroRepository.get_all()
    return jsonify(monstros)


@api_bp.route('/npcs', methods=['GET'])
def api_npcs():
    """Lista todos os NPCs"""
    from ..modulos.repositories import NPCRepository
    
    conhecidos = request.args.get('conhecidos')
    if conhecidos == '1':
        npcs = NPCRepository.get_conhecidos()
    else:
        npcs = NPCRepository.get_all()
    return jsonify(npcs)


@api_bp.route('/npcs/<int:id>', methods=['GET'])
def api_obter_npc(id):
    """Obtém um NPC pelo ID"""
    from ..modulos.repositories import NPCRepository
    npc = NPCRepository.get_by_id(id)
    if npc:
        return jsonify(npc)
    return jsonify({'erro': 'NPC não encontrado'}), 404


@api_bp.route('/npcs/<int:id>', methods=['PUT', 'PATCH'])
def api_atualizar_npc(id):
    """Atualiza um NPC"""
    from ..modulos.repositories import NPCRepository
    data = request.get_json()
    NPCRepository.update(id, data)
    npc = NPCRepository.get_by_id(id)
    return jsonify(npc)


@api_bp.route('/npcs', methods=['POST'])
def api_criar_npc():
    """Cria um novo NPC"""
    from ..modulos.repositories import NPCRepository
    data = request.get_json()
    id = NPCRepository.insert(data)
    npc = NPCRepository.get_by_id(id)
    return jsonify(npc)
