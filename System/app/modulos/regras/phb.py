"""
Raças e Classes do Player's Handbook (Livro do Jogador)

Fonte: PHB
Raças: Anão, Elfo, Halfling, Humano, Draconato, Gnomo, Meio-Elfo, Meio-Orc, Tiefling
Classes: Bárbaro, Bardo, Bruxo, Clérigo, Druida, Feiticeiro, Guerreiro, Ladino, Mago, Monge, Paladino, Patrulheiro
"""

from ..database import get_connection, json_dumps
from .base import inserir_raca, inserir_classe


# ==================== RAÇAS DO PHB ====================

RACAS_PHB = [
    # === ANÃO ===
    {
        'nome': 'Anão',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'constituicao': 2},
        'velocidade': 7,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Anão'],
        'proficiencias_armas': ['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resiliência Anã: Vantagem em salvaguardas contra veneno',
            'Especialização em Pedra: Dobra proficiência em História relacionada a pedra'
        ],
        'resistencias': ['veneno'],
    },
    {
        'nome': 'Anão da Colina',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'constituicao': 2, 'sabedoria': 1},
        'velocidade': 7,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Anão'],
        'proficiencias_armas': ['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resiliência Anã: Vantagem em salvaguardas contra veneno',
            'Especialização em Pedra: Dobra proficiência em História relacionada a pedra',
            'Tenacidade Anã: HP máximo aumenta em 1 por nível'
        ],
        'resistencias': ['veneno'],
        'subraca_de': 1,
    },
    {
        'nome': 'Anão da Montanha',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'constituicao': 2, 'forca': 2},
        'velocidade': 7,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Anão'],
        'proficiencias_armas': ['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra'],
        'proficiencias_armaduras': ['armaduras leves', 'armaduras médias'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resiliência Anã: Vantagem em salvaguardas contra veneno',
            'Especialização em Pedra: Dobra proficiência em História relacionada a pedra',
            'Treinamento Anão com Armaduras'
        ],
        'resistencias': ['veneno'],
        'subraca_de': 1,
    },
    
    # === ELFO ===
    {
        'nome': 'Elfo',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'pericias_bonus': ['percepcao'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
            'Transe: 4 horas de meditação = 8 horas de sono'
        ],
        'imunidades': ['sono mágico'],
    },
    {
        'nome': 'Alto Elfo',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2, 'inteligencia': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'idiomas_escolha': 1,
        'proficiencias_armas': ['espada longa', 'espada curta', 'arco longo', 'arco curto'],
        'pericias_bonus': ['percepcao'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
            'Transe: 4 horas de meditação = 8 horas de sono',
            'Truque: Conhece 1 truque de mago (Inteligência)'
        ],
        'imunidades': ['sono mágico'],
        'subraca_de': 4,
    },
    {
        'nome': 'Elfo da Floresta',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2, 'sabedoria': 1},
        'velocidade': 10,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'proficiencias_armas': ['espada longa', 'espada curta', 'arco longo', 'arco curto'],
        'pericias_bonus': ['percepcao'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
            'Transe: 4 horas de meditação = 8 horas de sono',
            'Máscara da Natureza: Pode se esconder com folhagem, chuva, neve, neblina',
            'Pés Ligeiros: Velocidade base 10m'
        ],
        'imunidades': ['sono mágico'],
        'subraca_de': 4,
    },
    {
        'nome': 'Drow',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2, 'carisma': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'proficiencias_armas': ['rapieira', 'espada curta', 'besta de mão'],
        'pericias_bonus': ['percepcao'],
        'caracteristicas': [
            'Visão no Escuro Superior (36m)',
            'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
            'Transe: 4 horas de meditação = 8 horas de sono',
            'Sensibilidade à Luz Solar: Desvantagem em ataques e Percepção sob luz solar',
            'Magia Drow: Conhece Luzes Dançantes; nível 3: Fogo das Fadas; nível 5: Escuridão'
        ],
        'imunidades': ['sono mágico'],
        'subraca_de': 4,
    },
    
    # === HALFLING ===
    {
        'nome': 'Halfling',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Halfling'],
        'caracteristicas': [
            'Sortudo: Ao rolar 1 natural, pode rolar novamente',
            'Corajoso: Vantagem contra ser amedrontado',
            'Agilidade Halfling: Pode mover através de criaturas maiores'
        ],
    },
    {
        'nome': 'Halfling Pés Leves',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2, 'carisma': 1},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Halfling'],
        'caracteristicas': [
            'Sortudo: Ao rolar 1 natural, pode rolar novamente',
            'Corajoso: Vantagem contra ser amedrontado',
            'Agilidade Halfling: Pode mover através de criaturas maiores',
            'Furtividade Natural: Pode se esconder atrás de criaturas maiores'
        ],
        'subraca_de': 8,
    },
    {
        'nome': 'Halfling Robusto',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'destreza': 2, 'constituicao': 1},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Halfling'],
        'caracteristicas': [
            'Sortudo: Ao rolar 1 natural, pode rolar novamente',
            'Corajoso: Vantagem contra ser amedrontado',
            'Agilidade Halfling: Pode mover através de criaturas maiores',
            'Resiliência Robusta: Vantagem contra veneno, resistência a dano de veneno'
        ],
        'resistencias': ['veneno'],
        'subraca_de': 8,
    },
    
    # === HUMANO ===
    {
        'nome': 'Humano',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'forca': 1, 'destreza': 1, 'constituicao': 1, 'inteligencia': 1, 'sabedoria': 1, 'carisma': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Versátil: +1 em todos os atributos',
            'Idioma Extra: Conhece um idioma adicional à escolha'
        ],
    },
    {
        'nome': 'Humano (Variante)',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {},
        'atributos_escolha': 2,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'pericias_escolha': 1,
        'caracteristicas': [
            '+1 em dois atributos diferentes à escolha',
            'Uma perícia à escolha',
            'Um talento à escolha'
        ],
    },
    
    # === DRACONATO ===
    {
        'nome': 'Draconato',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'forca': 2, 'carisma': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Dracônico'],
        'caracteristicas': [
            'Ancestral Dracônico: Escolha um tipo de dragão ancestral',
            'Sopro: Usa ação para soprar energia (dano = 2d6, aumenta com nível)',
            'Resistência a Dano: Resistência ao tipo de dano do ancestral'
        ],
    },
    
    # === GNOMO ===
    {
        'nome': 'Gnomo',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'inteligencia': 2},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Gnômico'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia'
        ],
    },
    {
        'nome': 'Gnomo da Floresta',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'inteligencia': 2, 'destreza': 1},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Gnômico'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia',
            'Ilusionista Nato: Conhece o truque Ilusão Menor',
            'Falar com Bestas Pequenas: Pode se comunicar com animais pequenos'
        ],
        'subraca_de': 15,
    },
    {
        'nome': 'Gnomo das Rochas',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'inteligencia': 2, 'constituicao': 1},
        'velocidade': 7,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Gnômico'],
        'proficiencias_ferramentas': ['ferramentas de artesão'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia',
            'Conhecimento de Artífice: Dobra proficiência em História sobre itens mágicos/tecnológicos',
            'Engenhoqueiro: Pode criar pequenos dispositivos mecânicos'
        ],
        'subraca_de': 15,
    },
    
    # === MEIO-ELFO ===
    {
        'nome': 'Meio-Elfo',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'carisma': 2},
        'atributos_escolha': 2,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'idiomas_escolha': 1,
        'pericias_escolha': 2,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
            'Versatilidade em Perícia: Proficiência em duas perícias à escolha'
        ],
        'imunidades': ['sono mágico'],
    },
    
    # === MEIO-ORC ===
    {
        'nome': 'Meio-Orc',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'forca': 2, 'constituicao': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Orc'],
        'pericias_bonus': ['intimidacao'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resistência Implacável: 1x/descanso longo, ao cair para 0 HP, cai para 1 HP',
            'Ataques Selvagens: Crítico com arma corpo a corpo rola 1 dado de dano extra'
        ],
    },
    
    # === TIEFLING ===
    {
        'nome': 'Tiefling',
        'categoria': 'Livro do Jogador',
        'bonus_atributos': {'carisma': 2, 'inteligencia': 1},
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Infernal'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resistência Infernal: Resistência a dano de fogo',
            'Legado Infernal: Conhece Taumaturgia; nível 3: Repreensão Infernal; nível 5: Escuridão'
        ],
        'resistencias': ['fogo'],
    },
]


# ==================== CLASSES DO PHB ====================

CLASSES_PHB = [
    {
        'nome': 'Bárbaro',
        'dado_vida': 12,
        'hp_primeiro_nivel': '12 + modificador de Constituição',
        'salvaguardas_proficientes': ['forca', 'constituicao'],
        'armaduras': ['armaduras leves', 'armaduras médias', 'escudos'],
        'armas': ['armas simples', 'armas marciais'],
        'ferramentas': [],
        'pericias_disponiveis': ['adestrar_animais', 'atletismo', 'intimidacao', 'natureza', 'percepcao', 'sobrevivencia'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Fúria', 'Defesa sem Armadura'],
    },
    {
        'nome': 'Bardo',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['destreza', 'carisma'],
        'armaduras': ['armaduras leves'],
        'armas': ['armas simples', 'bestas de mão', 'espadas longas', 'rapieiras', 'espadas curtas'],
        'ferramentas': ['três instrumentos musicais à escolha'],
        'pericias_disponiveis': ['todas'],
        'qtd_pericias': 3,
        'caracteristicas_nivel_1': ['Conjuração', 'Inspiração de Bardo (d6)'],
        'conjurador': 1,
        'atributo_conjuracao': 'carisma',
        'truques_nivel_1': 2,
        'magias_conhecidas_nivel_1': 4,
    },
    {
        'nome': 'Bruxo',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['sabedoria', 'carisma'],
        'armaduras': ['armaduras leves'],
        'armas': ['armas simples'],
        'ferramentas': [],
        'pericias_disponiveis': ['arcanismo', 'enganacao', 'historia', 'intimidacao', 'investigacao', 'natureza', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Patrono Transcendental', 'Magia de Pacto'],
        'conjurador': 1,
        'atributo_conjuracao': 'carisma',
        'truques_nivel_1': 2,
        'magias_conhecidas_nivel_1': 2,
    },
    {
        'nome': 'Clérigo',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['sabedoria', 'carisma'],
        'armaduras': ['armaduras leves', 'armaduras médias', 'escudos'],
        'armas': ['armas simples'],
        'ferramentas': [],
        'pericias_disponiveis': ['historia', 'intuicao', 'medicina', 'persuasao', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Conjuração', 'Domínio Divino'],
        'conjurador': 1,
        'atributo_conjuracao': 'sabedoria',
        'truques_nivel_1': 3,
    },
    {
        'nome': 'Druida',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['inteligencia', 'sabedoria'],
        'armaduras': ['armaduras leves (não-metálicas)', 'armaduras médias (não-metálicas)', 'escudos (não-metálicos)'],
        'armas': ['clavas', 'adagas', 'dardos', 'azagaias', 'maças', 'bordões', 'cimitarras', 'foices', 'fundas', 'lanças'],
        'ferramentas': ['kit de herbalismo'],
        'pericias_disponiveis': ['arcanismo', 'adestrar_animais', 'intuicao', 'medicina', 'natureza', 'percepcao', 'religiao', 'sobrevivencia'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Druídico', 'Conjuração'],
        'conjurador': 1,
        'atributo_conjuracao': 'sabedoria',
        'truques_nivel_1': 2,
    },
    {
        'nome': 'Feiticeiro',
        'dado_vida': 6,
        'hp_primeiro_nivel': '6 + modificador de Constituição',
        'salvaguardas_proficientes': ['constituicao', 'carisma'],
        'armaduras': [],
        'armas': ['adagas', 'dardos', 'fundas', 'bordões', 'bestas leves'],
        'ferramentas': [],
        'pericias_disponiveis': ['arcanismo', 'enganacao', 'intuicao', 'intimidacao', 'persuasao', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Conjuração', 'Origem de Feitiçaria'],
        'conjurador': 1,
        'atributo_conjuracao': 'carisma',
        'truques_nivel_1': 4,
        'magias_conhecidas_nivel_1': 2,
    },
    {
        'nome': 'Guerreiro',
        'dado_vida': 10,
        'hp_primeiro_nivel': '10 + modificador de Constituição',
        'salvaguardas_proficientes': ['forca', 'constituicao'],
        'armaduras': ['todas as armaduras', 'escudos'],
        'armas': ['armas simples', 'armas marciais'],
        'ferramentas': [],
        'pericias_disponiveis': ['acrobacia', 'adestrar_animais', 'atletismo', 'historia', 'intuicao', 'intimidacao', 'percepcao', 'sobrevivencia'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Estilo de Luta', 'Retomar o Fôlego'],
    },
    {
        'nome': 'Ladino',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['destreza', 'inteligencia'],
        'armaduras': ['armaduras leves'],
        'armas': ['armas simples', 'bestas de mão', 'espadas longas', 'rapieiras', 'espadas curtas'],
        'ferramentas': ['ferramentas de ladrão'],
        'pericias_disponiveis': ['acrobacia', 'atletismo', 'atuacao', 'enganacao', 'furtividade', 'intimidacao', 'intuicao', 'investigacao', 'percepcao', 'persuasao', 'prestidigitacao'],
        'qtd_pericias': 4,
        'caracteristicas_nivel_1': ['Especialização', 'Ataque Furtivo (1d6)', 'Gíria dos Ladrões'],
    },
    {
        'nome': 'Mago',
        'dado_vida': 6,
        'hp_primeiro_nivel': '6 + modificador de Constituição',
        'salvaguardas_proficientes': ['inteligencia', 'sabedoria'],
        'armaduras': [],
        'armas': ['adagas', 'dardos', 'fundas', 'bordões', 'bestas leves'],
        'ferramentas': [],
        'pericias_disponiveis': ['arcanismo', 'historia', 'intuicao', 'investigacao', 'medicina', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Conjuração', 'Recuperação Arcana'],
        'conjurador': 1,
        'atributo_conjuracao': 'inteligencia',
        'truques_nivel_1': 3,
    },
    {
        'nome': 'Monge',
        'dado_vida': 8,
        'hp_primeiro_nivel': '8 + modificador de Constituição',
        'salvaguardas_proficientes': ['forca', 'destreza'],
        'armaduras': [],
        'armas': ['armas simples', 'espadas curtas'],
        'ferramentas': ['uma ferramenta de artesão ou instrumento musical'],
        'pericias_disponiveis': ['acrobacia', 'atletismo', 'furtividade', 'historia', 'intuicao', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Defesa sem Armadura', 'Artes Marciais'],
    },
    {
        'nome': 'Paladino',
        'dado_vida': 10,
        'hp_primeiro_nivel': '10 + modificador de Constituição',
        'salvaguardas_proficientes': ['sabedoria', 'carisma'],
        'armaduras': ['todas as armaduras', 'escudos'],
        'armas': ['armas simples', 'armas marciais'],
        'ferramentas': [],
        'pericias_disponiveis': ['atletismo', 'intimidacao', 'intuicao', 'medicina', 'persuasao', 'religiao'],
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': ['Sentido Divino', 'Cura pelas Mãos'],
    },
    {
        'nome': 'Patrulheiro',
        'dado_vida': 10,
        'hp_primeiro_nivel': '10 + modificador de Constituição',
        'salvaguardas_proficientes': ['forca', 'destreza'],
        'armaduras': ['armaduras leves', 'armaduras médias', 'escudos'],
        'armas': ['armas simples', 'armas marciais'],
        'ferramentas': [],
        'pericias_disponiveis': ['adestrar_animais', 'atletismo', 'furtividade', 'intuicao', 'investigacao', 'natureza', 'percepcao', 'sobrevivencia'],
        'qtd_pericias': 3,
        'caracteristicas_nivel_1': ['Inimigo Favorito', 'Explorador Natural'],
    },
]


# ==================== FUNÇÕES DE POPULAÇÃO ====================

def popular_racas_phb():
    """Popula raças do Livro do Jogador no banco"""
    with get_connection() as conn:
        print("[DB] Carregando raças do PHB...")
        for raca in RACAS_PHB:
            inserir_raca(conn, raca.copy(), fonte='PHB')


def popular_classes_phb():
    """Popula classes do Livro do Jogador no banco"""
    with get_connection() as conn:
        print("[DB] Carregando classes do PHB...")
        for classe in CLASSES_PHB:
            inserir_classe(conn, classe.copy(), fonte='PHB')
