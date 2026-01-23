"""
Rotas da Tela de Sessão - principal área de mestragem
Sistema de persistência de sessões em JSON
"""

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, date
import json
import os

sessao_bp = Blueprint('sessao', __name__)

# Caminho para os arquivos de sessão
SESSOES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'sessoes')

def garantir_pasta_sessoes():
    """Garante que a pasta de sessões existe"""
    if not os.path.exists(SESSOES_PATH):
        os.makedirs(SESSOES_PATH)

def get_data_atual():
    """Retorna a data atual no formato YYYY-MM-DD"""
    return date.today().isoformat()

def get_caminho_sessao(data_sessao):
    """Retorna o caminho do arquivo JSON de uma sessão"""
    garantir_pasta_sessoes()
    return os.path.join(SESSOES_PATH, f"sessao_{data_sessao}.json")

def get_caminho_indice():
    """Retorna o caminho do arquivo de índice de sessões"""
    garantir_pasta_sessoes()
    return os.path.join(SESSOES_PATH, "indice_sessoes.json")

def carregar_indice():
    """Carrega o índice de sessões"""
    caminho = get_caminho_indice()
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"sessao_atual": None, "sessoes": []}

def salvar_indice(indice):
    """Salva o índice de sessões"""
    caminho = get_caminho_indice()
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)

def criar_sessao_estrutura(data_sessao, numero):
    """Cria estrutura inicial de uma sessão"""
    return {
        "numero": numero,
        "data": data_sessao,
        "criada_em": datetime.now().isoformat(),
        "atualizada_em": datetime.now().isoformat(),
        "estado": {
            "mapa_atual": None,
            "combate_ativo": False,
            "round_atual": 0,
            "turno_atual": 0,
            "ordem_turnos": [],
            "widgets": []
        },
        "log": []
    }

def carregar_sessao(data_sessao):
    """Carrega uma sessão pelo arquivo JSON"""
    caminho = get_caminho_sessao(data_sessao)
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def salvar_sessao(sessao):
    """Salva uma sessão no arquivo JSON"""
    sessao['atualizada_em'] = datetime.now().isoformat()
    caminho = get_caminho_sessao(sessao['data'])
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(sessao, f, ensure_ascii=False, indent=2)

def get_ou_criar_sessao_atual():
    """Obtém a sessão atual ou cria uma nova se necessário"""
    indice = carregar_indice()
    data_hoje = get_data_atual()
    
    # Se não há sessão atual, cria uma
    if not indice['sessao_atual']:
        numero = len(indice['sessoes']) + 1
        nova_sessao = criar_sessao_estrutura(data_hoje, numero)
        salvar_sessao(nova_sessao)
        
        indice['sessao_atual'] = data_hoje
        indice['sessoes'].append({
            "numero": numero,
            "data": data_hoje,
            "titulo": f"Sessão {numero}"
        })
        salvar_indice(indice)
        return nova_sessao
    
    # Se a data da sessão atual é diferente de hoje, cria nova
    if indice['sessao_atual'] != data_hoje:
        numero = len(indice['sessoes']) + 1
        nova_sessao = criar_sessao_estrutura(data_hoje, numero)
        salvar_sessao(nova_sessao)
        
        indice['sessao_atual'] = data_hoje
        indice['sessoes'].append({
            "numero": numero,
            "data": data_hoje,
            "titulo": f"Sessão {numero}"
        })
        salvar_indice(indice)
        return nova_sessao
    
    # Carrega a sessão atual
    sessao = carregar_sessao(indice['sessao_atual'])
    if not sessao:
        # Sessão não existe, cria
        numero = len(indice['sessoes'])
        sessao = criar_sessao_estrutura(data_hoje, numero)
        salvar_sessao(sessao)
    
    return sessao


@sessao_bp.route('/')
def tela_sessao():
    """Tela principal de sessão - usada durante o jogo ao vivo"""
    sessao = get_ou_criar_sessao_atual()
    indice = carregar_indice()
    
    return render_template('sessao/tela_sessao.html', 
                         sessao=sessao, 
                         sessoes=indice['sessoes'])


@sessao_bp.route('/api/atual', methods=['GET'])
def api_sessao_atual():
    """Retorna dados da sessão atual"""
    sessao = get_ou_criar_sessao_atual()
    return jsonify(sessao)


@sessao_bp.route('/api/lista', methods=['GET'])
def api_listar_sessoes():
    """Lista todas as sessões"""
    indice = carregar_indice()
    return jsonify(indice['sessoes'])


@sessao_bp.route('/api/<data_sessao>', methods=['GET'])
def api_carregar_sessao(data_sessao):
    """Carrega uma sessão específica (somente leitura)"""
    sessao = carregar_sessao(data_sessao)
    if sessao:
        return jsonify(sessao)
    return jsonify({'erro': 'Sessão não encontrada'}), 404


@sessao_bp.route('/api/nova', methods=['POST'])
def api_nova_sessao():
    """Cria uma nova sessão manualmente"""
    indice = carregar_indice()
    data_hoje = get_data_atual()
    
    numero = len(indice['sessoes']) + 1
    nova_sessao = criar_sessao_estrutura(data_hoje, numero)
    salvar_sessao(nova_sessao)
    
    indice['sessao_atual'] = data_hoje
    indice['sessoes'].append({
        "numero": numero,
        "data": data_hoje,
        "titulo": f"Sessão {numero}"
    })
    salvar_indice(indice)
    
    return jsonify(nova_sessao)


@sessao_bp.route('/api/estado', methods=['POST'])
def api_salvar_estado():
    """Salva o estado atual da sessão"""
    data = request.get_json()
    sessao = get_ou_criar_sessao_atual()
    
    # Atualiza o estado
    if 'estado' in data:
        sessao['estado'].update(data['estado'])
    
    salvar_sessao(sessao)
    return jsonify({'sucesso': True})


@sessao_bp.route('/api/log', methods=['POST'])
def api_adicionar_log():
    """Adiciona uma entrada ao log da sessão"""
    data = request.get_json()
    sessao = get_ou_criar_sessao_atual()
    
    entrada_log = {
        "timestamp": datetime.now().isoformat(),
        "tipo": data.get('tipo', 'info'),
        "mensagem": data.get('mensagem', ''),
        "dados": data.get('dados', {})
    }
    
    sessao['log'].append(entrada_log)
    salvar_sessao(sessao)
    
    return jsonify({'sucesso': True, 'entrada': entrada_log})


@sessao_bp.route('/api/log/limpar', methods=['POST'])
def api_limpar_log():
    """Limpa o log da sessão atual"""
    sessao = get_ou_criar_sessao_atual()
    sessao['log'] = []
    salvar_sessao(sessao)
    return jsonify({'sucesso': True})


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
    data = request.get_json()
    caminho_mapa = data.get('caminho')
    
    sessao = get_ou_criar_sessao_atual()
    sessao['estado']['mapa_atual'] = caminho_mapa
    salvar_sessao(sessao)
    
    return jsonify({'sucesso': True, 'mapa': caminho_mapa})
