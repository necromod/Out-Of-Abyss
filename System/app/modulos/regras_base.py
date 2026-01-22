"""
Módulo de Regras Base - D&D 5e Livro do Jogador
Contém todas as regras fundamentais do sistema
"""

from typing import Dict, List, Any, Optional


# ==================== ATRIBUTOS ====================

ATRIBUTOS = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma']

ATRIBUTOS_ABREV = {
    'for': 'forca',
    'des': 'destreza', 
    'con': 'constituicao',
    'int': 'inteligencia',
    'sab': 'sabedoria',
    'car': 'carisma'
}


# ==================== PERÍCIAS ====================

PERICIAS = {
    'acrobacia': 'destreza',
    'adestrar_animais': 'sabedoria',
    'arcanismo': 'inteligencia',
    'atletismo': 'forca',
    'atuacao': 'carisma',
    'enganacao': 'carisma',
    'furtividade': 'destreza',
    'historia': 'inteligencia',
    'intimidacao': 'carisma',
    'intuicao': 'sabedoria',
    'investigacao': 'inteligencia',
    'medicina': 'sabedoria',
    'natureza': 'inteligencia',
    'percepcao': 'sabedoria',
    'persuasao': 'carisma',
    'prestidigitacao': 'destreza',
    'religiao': 'inteligencia',
    'sobrevivencia': 'sabedoria'
}


# ==================== CONDIÇÕES ====================

CONDICOES = {
    'amedrontado': {
        'nome': 'Amedrontado',
        'efeitos': [
            'Desvantagem em testes de habilidade e ataques enquanto a fonte do medo estiver visível',
            'Não pode se mover voluntariamente para mais perto da fonte do medo'
        ]
    },
    'atordoado': {
        'nome': 'Atordoado',
        'efeitos': [
            'Incapacitado',
            'Não pode se mover',
            'Fala apenas de forma hesitante',
            'Falha automaticamente em salvaguardas de Força e Destreza',
            'Ataques contra têm vantagem'
        ]
    },
    'caido': {
        'nome': 'Caído',
        'efeitos': [
            'Só pode se arrastar ou se levantar',
            'Desvantagem em ataques',
            'Ataques à distância têm desvantagem contra',
            'Ataques corpo a corpo de até 1,5m têm vantagem'
        ]
    },
    'cego': {
        'nome': 'Cego',
        'efeitos': [
            'Falha automaticamente em testes que exigem visão',
            'Desvantagem em ataques',
            'Ataques contra têm vantagem'
        ]
    },
    'encantado': {
        'nome': 'Encantado',
        'efeitos': [
            'Não pode atacar o encantador',
            'Encantador tem vantagem em testes sociais'
        ]
    },
    'envenenado': {
        'nome': 'Envenenado',
        'efeitos': [
            'Desvantagem em ataques e testes de habilidade'
        ]
    },
    'exausto': {
        'nome': 'Exausto',
        'niveis': {
            1: 'Desvantagem em testes de habilidade',
            2: 'Velocidade reduzida pela metade',
            3: 'Desvantagem em ataques e salvaguardas',
            4: 'HP máximo reduzido pela metade',
            5: 'Velocidade reduzida a 0',
            6: 'Morte'
        }
    },
    'incapacitado': {
        'nome': 'Incapacitado',
        'efeitos': [
            'Não pode realizar ações ou reações'
        ]
    },
    'inconsciente': {
        'nome': 'Inconsciente',
        'efeitos': [
            'Incapacitado',
            'Não pode se mover ou falar',
            'Não percebe o ambiente',
            'Larga o que estiver segurando e cai',
            'Falha automaticamente em salvaguardas de Força e Destreza',
            'Ataques contra têm vantagem',
            'Ataques de até 1,5m são críticos automaticamente'
        ]
    },
    'invisivel': {
        'nome': 'Invisível',
        'efeitos': [
            'Impossível de ser visto sem magia ou sentido especial',
            'Considerado obscurecido para esconder-se',
            'Vantagem em ataques',
            'Ataques contra têm desvantagem'
        ]
    },
    'paralisado': {
        'nome': 'Paralisado',
        'efeitos': [
            'Incapacitado',
            'Não pode se mover ou falar',
            'Falha automaticamente em salvaguardas de Força e Destreza',
            'Ataques contra têm vantagem',
            'Ataques de até 1,5m são críticos automaticamente'
        ]
    },
    'petrificado': {
        'nome': 'Petrificado',
        'efeitos': [
            'Transformado em pedra (com pertences)',
            'Peso multiplicado por 10',
            'Não envelhece',
            'Incapacitado',
            'Não percebe o ambiente',
            'Resistência a todo dano',
            'Imune a veneno e doença'
        ]
    },
    'surdo': {
        'nome': 'Surdo',
        'efeitos': [
            'Falha automaticamente em testes que exigem audição'
        ]
    },
    'agarrado': {
        'nome': 'Agarrado',
        'efeitos': [
            'Velocidade se torna 0',
            'Termina se agarrador ficar incapacitado',
            'Termina se efeito remover criatura do alcance'
        ]
    },
    'contido': {
        'nome': 'Contido',
        'efeitos': [
            'Velocidade se torna 0',
            'Desvantagem em ataques',
            'Ataques contra têm vantagem',
            'Desvantagem em salvaguardas de Destreza'
        ]
    }
}


# ==================== TIPOS DE DANO ====================

TIPOS_DANO = [
    'cortante', 'perfurante', 'contundente',
    'fogo', 'frio', 'eletrico', 'acido', 'veneno',
    'psiquico', 'necrotico', 'radiante',
    'forca', 'trovao'
]


# ==================== FUNÇÕES UTILITÁRIAS ====================

def calcular_bonus_proficiencia(nivel: int) -> int:
    """Calcula o bônus de proficiência baseado no nível"""
    if nivel < 1:
        return 2
    return 2 + ((nivel - 1) // 4)


def calcular_classe_armadura_base(destreza_mod: int, armadura: Optional[Dict] = None, escudo: bool = False) -> int:
    """
    Calcula a CA base
    Sem armadura: 10 + mod Destreza
    Com armadura: depende do tipo
    """
    ca_escudo = 2 if escudo else 0
    
    if not armadura:
        return 10 + destreza_mod + ca_escudo
    
    tipo = armadura.get('tipo', 'leve')
    ca_base = armadura.get('ca_base', 10)
    
    if tipo == 'leve':
        return ca_base + destreza_mod + ca_escudo
    elif tipo == 'media':
        return ca_base + min(destreza_mod, 2) + ca_escudo
    elif tipo == 'pesada':
        return ca_base + ca_escudo
    
    return 10 + destreza_mod + ca_escudo


def obter_condicao(nome: str) -> Optional[Dict]:
    """Retorna informações de uma condição"""
    return CONDICOES.get(nome.lower())


def obter_pericias_por_atributo(atributo: str) -> List[str]:
    """Retorna lista de perícias associadas a um atributo"""
    return [pericia for pericia, attr in PERICIAS.items() if attr == atributo]
