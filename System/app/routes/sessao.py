"""
Rotas da Tela de Sessão - principal área de mestragem
Sistema de persistência de sessões em JSON
"""

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, date
import json
import os
import tempfile
import threading

sessao_bp = Blueprint('sessao', __name__)

# Caminho para os arquivos de sessão
SESSOES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'sessoes')

# Lock para evitar escritas simultâneas
_sessao_lock = threading.Lock()

def garantir_pasta_sessoes():
    """Garante que a pasta de sessões existe"""
    if not os.path.exists(SESSOES_PATH):
        os.makedirs(SESSOES_PATH)

def get_data_atual():
    """Retorna a data atual no formato YYYY-MM-DD"""
    return date.today().isoformat()

def get_caminho_sessao(identificador):
    """Retorna o caminho do arquivo JSON de uma sessão (aceita data ou número)"""
    garantir_pasta_sessoes()
    # Se for número, usa formato sessao_N.json, senão sessao_DATA.json
    if isinstance(identificador, int) or identificador.isdigit():
        return os.path.join(SESSOES_PATH, f"sessao_{identificador}.json")
    return os.path.join(SESSOES_PATH, f"sessao_{identificador}.json")

def get_caminho_indice():
    """Retorna o caminho do arquivo de índice de sessões"""
    garantir_pasta_sessoes()
    return os.path.join(SESSOES_PATH, "indice_sessoes.json")

def carregar_indice():
    """Carrega o índice de sessões"""
    caminho = get_caminho_indice()
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8-sig') as f:
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
        "id": str(numero),  # Identificador único para salvar arquivo
        "data": data_sessao,
        "criada_em": datetime.now().isoformat(),
        "atualizada_em": datetime.now().isoformat(),
        "estado": {
            "mapa_atual": None,
            "combate_ativo": False,
            "turno_contador": 0,
            "turno_atual": 0,
            "ordem_turnos": [],
            "widgets": []
        },
        "log": []
    }

def carregar_sessao(identificador):
    """Carrega uma sessão pelo arquivo JSON"""
    caminho = get_caminho_sessao(identificador)
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r', encoding='utf-8-sig') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            # Arquivo corrompido - tenta recuperar ou cria backup
            print(f"AVISO: Arquivo de sessão corrompido: {e}")
            backup = caminho + '.corrupted'
            if os.path.exists(backup):
                os.remove(backup)
            os.rename(caminho, backup)
            return None
    return None

def salvar_sessao(sessao):
    """Salva uma sessão no arquivo JSON de forma atômica"""
    sessao['atualizada_em'] = datetime.now().isoformat()
    # Usa o ID (número) como identificador do arquivo
    identificador = sessao.get('id', sessao.get('numero', sessao['data']))
    caminho = get_caminho_sessao(identificador)
    
    with _sessao_lock:
        # Escrita atômica: escreve em temp e renomeia
        dir_path = os.path.dirname(caminho)
        try:
            fd, temp_path = tempfile.mkstemp(dir=dir_path, suffix='.tmp')
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump(sessao, f, ensure_ascii=False, indent=2)
            
            # Renomeia atomicamente (substitui o arquivo antigo)
            if os.path.exists(caminho):
                os.replace(temp_path, caminho)
            else:
                os.rename(temp_path, caminho)
        except Exception as e:
            # Limpa arquivo temporário em caso de erro
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

def get_ou_criar_sessao_atual():
    """Obtém a sessão atual ou cria uma nova se necessário"""
    indice = carregar_indice()
    data_hoje = get_data_atual()
    
    # Se não há sessão atual, cria uma
    if not indice['sessao_atual']:
        numero = len(indice['sessoes']) + 1
        nova_sessao = criar_sessao_estrutura(data_hoje, numero)
        salvar_sessao(nova_sessao)
        
        indice['sessao_atual'] = str(numero)  # Usa número como ID
        indice['sessoes'].append({
            "numero": numero,
            "id": str(numero),
            "data": data_hoje,
            "titulo": f"Sessão {numero}"
        })
        salvar_indice(indice)
        return nova_sessao
    
    # Carrega a sessão atual pelo ID
    sessao = carregar_sessao(indice['sessao_atual'])
    if not sessao:
        # Sessão não existe, cria nova
        numero = len(indice['sessoes']) + 1
        sessao = criar_sessao_estrutura(data_hoje, numero)
        salvar_sessao(sessao)
        
        indice['sessao_atual'] = str(numero)
        indice['sessoes'].append({
            "numero": numero,
            "id": str(numero),
            "data": data_hoje,
            "titulo": f"Sessão {numero}"
        })
        salvar_indice(indice)
    
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


@sessao_bp.route('/api/<identificador>', methods=['GET'])
def api_carregar_sessao(identificador):
    """Carrega uma sessão específica pelo ID ou data"""
    sessao = carregar_sessao(identificador)
    if sessao:
        return jsonify(sessao)
    return jsonify({'erro': 'Sessão não encontrada'}), 404


@sessao_bp.route('/api/mudar/<identificador>', methods=['POST'])
def api_mudar_sessao(identificador):
    """Muda para uma sessão específica (carrega sessão anterior)"""
    sessao = carregar_sessao(identificador)
    if not sessao:
        return jsonify({'erro': 'Sessão não encontrada'}), 404
    
    indice = carregar_indice()
    indice['sessao_atual'] = str(sessao.get('id', sessao.get('numero', identificador)))
    salvar_indice(indice)
    
    return jsonify({'sucesso': True, 'sessao': sessao})


@sessao_bp.route('/api/nova', methods=['POST'])
def api_nova_sessao():
    """Cria uma nova sessão manualmente (permite múltiplas no mesmo dia)"""
    indice = carregar_indice()
    data_hoje = get_data_atual()
    
    numero = len(indice['sessoes']) + 1
    nova_sessao = criar_sessao_estrutura(data_hoje, numero)
    salvar_sessao(nova_sessao)
    
    indice['sessao_atual'] = str(numero)  # Usa número como ID
    indice['sessoes'].append({
        "numero": numero,
        "id": str(numero),
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
