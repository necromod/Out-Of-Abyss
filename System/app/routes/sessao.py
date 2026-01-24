"""
Rotas da Tela de Sessão - principal área de mestragem
Sistema de persistência de sessões em JSON
"""

from flask import Blueprint, render_template, request, jsonify, send_from_directory
from datetime import datetime, date
import json
import os
import tempfile
import threading
import time
from pathlib import Path

sessao_bp = Blueprint('sessao', __name__)

# Caminho para os arquivos de sessão
SESSOES_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'sessoes')

# Caminho base do projeto (fora de System)
BASE_PATH = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

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
            
            # Tenta renomear com retry (Google Drive pode bloquear)
            max_tentativas = 3
            for tentativa in range(max_tentativas):
                try:
                    if os.path.exists(caminho):
                        os.replace(temp_path, caminho)
                    else:
                        os.rename(temp_path, caminho)
                    break  # Sucesso
                except PermissionError as pe:
                    if tentativa < max_tentativas - 1:
                        time.sleep(0.1)  # Aguarda 100ms e tenta novamente
                    else:
                        # Última tentativa: força sobrescrita direta
                        try:
                            with open(caminho, 'w', encoding='utf-8') as f:
                                json.dump(sessao, f, ensure_ascii=False, indent=2)
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                        except:
                            raise pe
        except Exception as e:
            # Limpa arquivo temporário em caso de erro
            if 'temp_path' in locals() and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
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


@sessao_bp.route('/imagens/<path:filename>')
def servir_imagem(filename):
    """Serve imagens da pasta Imagens"""
    imagens_path = BASE_PATH / 'Imagens'
    return send_from_directory(str(imagens_path), filename)


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


@sessao_bp.route('/api/cenarios', methods=['GET'])
def listar_cenarios():
    """Lista todos os cenários disponíveis"""
    from pathlib import Path
    
    # Caminho para a pasta de cenários (fora do System)
    base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    cenarios_path = base_path / 'Imagens' / 'Cenários'
    
    if not cenarios_path.exists():
        cenarios_path.mkdir(parents=True, exist_ok=True)
    
    # Lista todas as imagens
    extensoes = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    cenarios = []
    imagens_path = base_path / 'Imagens'
    
    for arquivo in cenarios_path.iterdir():
        if arquivo.is_file() and arquivo.suffix.lower() in extensoes:
            # Caminho relativo à pasta Imagens (para usar com /sessao/imagens/)
            caminho_relativo = str(arquivo.relative_to(imagens_path)).replace('\\', '/')
            cenarios.append({
                'nome': arquivo.name,
                'caminho': caminho_relativo,  # Ex: "Cenários/mapa.png"
                'tamanho': arquivo.stat().st_size
            })
    
    # Ordena por nome
    cenarios.sort(key=lambda x: x['nome'])
    
    return jsonify(cenarios)


@sessao_bp.route('/api/cenarios/upload', methods=['POST'])
def upload_cenario():
    """Recebe upload de imagem de cenário via drag-and-drop"""
    from pathlib import Path
    from werkzeug.utils import secure_filename
    
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'erro': 'Nome de arquivo vazio'}), 400
    
    # Valida extensão
    extensoes_permitidas = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
    ext = Path(file.filename).suffix.lower()
    
    if ext not in extensoes_permitidas:
        return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400
    
    # Caminho para a pasta de cenários
    base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    cenarios_path = base_path / 'Imagens' / 'Cenários'
    cenarios_path.mkdir(parents=True, exist_ok=True)
    
    # Nome seguro do arquivo
    nome_original = secure_filename(file.filename)
    nome_sem_ext = Path(nome_original).stem
    
    # Verifica duplicatas e adiciona número
    contador = 1
    nome_final = nome_original
    caminho_final = cenarios_path / nome_final
    
    while caminho_final.exists():
        nome_final = f"{nome_sem_ext}_{contador}{ext}"
        caminho_final = cenarios_path / nome_final
        contador += 1
    
    # Salva o arquivo
    file.save(str(caminho_final))
    
    # Retorna o caminho relativo à pasta Imagens (para usar com /sessao/imagens/)
    imagens_path = base_path / 'Imagens'
    caminho_relativo = str(caminho_final.relative_to(imagens_path)).replace('\\', '/')
    
    return jsonify({
        'sucesso': True,
        'nome': nome_final,
        'caminho': caminho_relativo,  # Ex: "Cenários/mapa.png"
        'mensagem': f'Cenário "{nome_final}" salvo com sucesso!'
    })


@sessao_bp.route('/api/cenarios/selecionar', methods=['POST'])
def selecionar_cenario():
    """Define o cenário atual da sessão"""
    data = request.get_json()
    caminho = data.get('caminho')
    
    if not caminho:
        return jsonify({'erro': 'Caminho não fornecido'}), 400
    
    sessao = get_ou_criar_sessao_atual()
    sessao['estado']['mapa_atual'] = caminho
    salvar_sessao(sessao)
    
    return jsonify({
        'sucesso': True,
        'mapa': caminho
    })
