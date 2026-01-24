"""
Raças de Outros Suplementos

Fontes:
- ERLW: Eberron: Rising from the Last War
- GGR: Guildmasters' Guide to Ravnica
- SCAG: Sword Coast Adventurer's Guide (subclasses apenas)
- TCE: Tasha's Cauldron of Everything (regras opcionais)
- VGM: Volo's Guide to Monsters (versões antigas - muitas reimaginadas no MPMM)

Nota: Algumas raças foram reimaginadas no Monsters of the Multiverse.
      Essas versões são mantidas para compatibilidade ou preferência do jogador.
"""

from ..database import get_connection, json_dumps
from .base import inserir_raca


# ==================== RAÇAS DE EBERRON ====================

RACAS_EBERRON = [
    # Kalashtar
    {
        'nome': 'Kalashtar',
        'categoria': 'Eberron',
        'bonus_atributos': {'sabedoria': 2, 'carisma': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Quori'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Mente Dual: Vantagem em salvaguardas de Sabedoria',
            'Disciplina Mental: Resistência a dano psíquico',
            'Ligação Mental: Telepatia até 18m (não é conversação completa)',
            'Ligação Espiritual: +vantagem em morte, vantagem em percepção durante descanso'
        ],
        'resistencias': ['psíquico'],
    },
    
    # Warforged
    {
        'nome': 'Warforged',
        'categoria': 'Eberron',
        'bonus_atributos': {'constituicao': 2},
        'atributos_escolha': 1,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Construído para Guerra: +1 CA',
            'Resiliência Construída: Vantagem contra veneno, resistência a veneno',
            'Resistência Construída: Não precisa comer, beber, respirar ou dormir',
            'Modo Sentinela: 6h de inatividade = descanso longo (permanece consciente)',
            'Integração: Armadura pode ser integrada ao corpo'
        ],
        'resistencias': ['veneno'],
    },
]


# ==================== RAÇAS DE RAVNICA ====================

RACAS_RAVNICA = [
    # Loxodon
    {
        'nome': 'Loxodon',
        'categoria': 'Ravnica',
        'bonus_atributos': {'constituicao': 2, 'sabedoria': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Loxodon'],
        'caracteristicas': [
            'Físico Poderoso: Conta como Grande para carga',
            'Tromba: Pode segurar objetos, usar como snorkel',
            'Armadura Natural: CA = 12 + CON sem armadura',
            'Serenidade de Loxodon: Vantagem contra amedrontado e encantado'
        ],
    },
    
    # Simic Hybrid
    {
        'nome': 'Híbrido Simic',
        'categoria': 'Ravnica',
        'bonus_atributos': {'constituicao': 2},
        'atributos_escolha': 1,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Adaptação Animal (nível 1): Escolha 1 adaptação',
            'Adaptação Animal (nível 5): Escolha outra adaptação'
        ],
    },
    
    # Vedalken
    {
        'nome': 'Vedalken',
        'categoria': 'Ravnica',
        'bonus_atributos': {'inteligencia': 2, 'sabedoria': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Vedalken'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Descrença Vedalken: Vantagem em INT, SAB, CAR contra magia',
            'Precisão Incansável: Proficiência em ferramenta + perícia',
            'Pensamento Parcialmente Anfíbio: Pode respirar água por 1h'
        ],
    },
]


# ==================== FUNÇÃO DE POPULAÇÃO ====================

def popular_racas_suplementos():
    """Popula raças de outros suplementos no banco"""
    with get_connection() as conn:
        print("[DB] Carregando raças de Eberron...")
        for raca in RACAS_EBERRON:
            inserir_raca(conn, raca.copy(), fonte='ERLW')
        
        print("[DB] Carregando raças de Ravnica...")
        for raca in RACAS_RAVNICA:
            inserir_raca(conn, raca.copy(), fonte='GGR')
