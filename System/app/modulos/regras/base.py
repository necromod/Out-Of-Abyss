"""
Dados Base D&D 5e - Perícias, Idiomas e Utilidades

Este módulo contém:
- Perícias (18 perícias base)
- Idiomas (comuns, exóticos, secretos)
- Funções utilitárias para inserção
"""

from ..database import get_connection, json_dumps


# ==================== DADOS ESTÁTICOS ====================

PERICIAS = [
    ('acrobacia', 'Acrobacia', 'destreza', 'Equilíbrio, acrobacias, escapar de amarras'),
    ('adestrar_animais', 'Adestrar Animais', 'sabedoria', 'Acalmar, treinar ou controlar animais'),
    ('arcanismo', 'Arcanismo', 'inteligencia', 'Conhecimento sobre magia, planos, criaturas mágicas'),
    ('atletismo', 'Atletismo', 'forca', 'Escalar, saltar, nadar, situações de força'),
    ('atuacao', 'Atuação', 'carisma', 'Entreter, atuar, tocar instrumentos'),
    ('enganacao', 'Enganação', 'carisma', 'Mentir, disfarçar intenções, blefar'),
    ('furtividade', 'Furtividade', 'destreza', 'Esconder-se, mover-se silenciosamente'),
    ('historia', 'História', 'inteligencia', 'Conhecimento histórico, lendas, eventos'),
    ('intimidacao', 'Intimidação', 'carisma', 'Ameaçar, coagir, influenciar por medo'),
    ('intuicao', 'Intuição', 'sabedoria', 'Detectar mentiras, perceber intenções'),
    ('investigacao', 'Investigação', 'inteligencia', 'Procurar pistas, deduzir, analisar'),
    ('medicina', 'Medicina', 'sabedoria', 'Estabilizar, diagnosticar, curar'),
    ('natureza', 'Natureza', 'inteligencia', 'Conhecimento sobre fauna, flora, clima'),
    ('percepcao', 'Percepção', 'sabedoria', 'Notar detalhes, ouvir, ver, sentir'),
    ('persuasao', 'Persuasão', 'carisma', 'Convencer, negociar, diplomacia'),
    ('prestidigitacao', 'Prestidigitação', 'destreza', 'Truques de mão, furtar, desativar'),
    ('religiao', 'Religião', 'inteligencia', 'Conhecimento sobre deuses, rituais, símbolos'),
    ('sobrevivencia', 'Sobrevivência', 'sabedoria', 'Rastrear, caçar, navegar, encontrar comida'),
]

IDIOMAS = [
    # Idiomas Comuns
    ('Comum', 'comum', 'Humanos, maioria das raças civilizadas'),
    ('Anão', 'comum', 'Anões'),
    ('Élfico', 'comum', 'Elfos'),
    ('Gigante', 'comum', 'Ogros, gigantes'),
    ('Gnômico', 'comum', 'Gnomos'),
    ('Goblin', 'comum', 'Goblins, hobgoblins, bugbears'),
    ('Halfling', 'comum', 'Halflings'),
    ('Orc', 'comum', 'Orcs'),
    
    # Idiomas Exóticos
    ('Abissal', 'exotico', 'Demônios'),
    ('Celestial', 'exotico', 'Celestiais'),
    ('Dracônico', 'exotico', 'Dragões, draconatos'),
    ('Dialeto Subterrâneo', 'exotico', 'Comerciantes do Subterrâneo'),
    ('Infernal', 'exotico', 'Diabos'),
    ('Primordial', 'exotico', 'Elementais'),
    ('Silvestre', 'exotico', 'Criaturas feéricas'),
    ('Subcomum', 'exotico', 'Criaturas do Subterrâneo'),
    ('Gith', 'exotico', 'Githyanki, Githzerai'),
    
    # Idiomas Secretos
    ('Druídico', 'secreto', 'Druidas (secreto)'),
    ('Cant dos Ladrões', 'secreto', 'Ladinos (secreto)'),
]

# Tipos de Criatura D&D 5e
TIPOS_CRIATURA = [
    ('aberracao', 'Aberração', 
     'Criaturas completamente alienígenas, com anatomia bizarra e poderes psíquicos.',
     'Aboleth, Beholder, Mind Flayer'),
    ('besta', 'Besta', 
     'Criaturas não-humanóides do mundo natural, animais comuns e fantásticos.',
     'Lobo, Urso, Coruja Gigante'),
    ('celestial', 'Celestial', 
     'Criaturas nativas dos Planos Superiores, geralmente de natureza bondosa.',
     'Anjo, Unicórnio, Couatl'),
    ('constructo', 'Constructo', 
     'Criaturas artificiais criadas por magia ou alquimia.',
     'Golem, Animated Armor, Shield Guardian'),
    ('dragao', 'Dragão', 
     'Répteis alados ancestrais, frequentemente com sopros elementais.',
     'Dragão Vermelho, Dragão de Ouro, Pseudodragão'),
    ('elemental', 'Elemental', 
     'Criaturas compostas de essência elemental pura.',
     'Elemental de Fogo, Djinn, Salamandra'),
    ('fada', 'Fada', 
     'Criaturas mágicas conectadas às forças da natureza e ao Feywild.',
     'Pixie, Dríade, Sátiro'),
    ('fera-monstruosa', 'Fera Monstruosa', 
     'Bestas sobrenaturais com características mágicas ou monstruosas.',
     'Grifo, Quimera, Cockatrice'),
    ('gigante', 'Gigante', 
     'Humanóides de grande porte, frequentemente com poderes elementais.',
     'Gigante do Fogo, Ogro, Troll'),
    ('humanoide', 'Humanóide', 
     'Criaturas bípedes com sociedade e cultura, incluindo as raças jogáveis.',
     'Humano, Elfo, Goblin, Orc'),
    ('monstruosidade', 'Monstruosidade', 
     'Criaturas assustadoras que não se encaixam em outras categorias.',
     'Medusa, Minotauro, Hidra'),
    ('morto-vivo', 'Morto-vivo', 
     'Criaturas que já foram vivas e agora existem em estado de não-morte.',
     'Zumbi, Vampiro, Lich'),
    ('limo', 'Limo', 
     'Criaturas amorfas que geralmente dissolvem matéria orgânica.',
     'Cubo Gelatinoso, Gosma Cinzenta, Pudim Negro'),
    ('planta', 'Planta', 
     'Criaturas vegetais animadas por magia ou natureza.',
     'Shambling Mound, Treant, Myconid'),
]


# ==================== FUNÇÕES DE INSERÇÃO ====================

def popular_dados_base():
    """Popula perícias e idiomas no banco"""
    with get_connection() as conn:
        # Verifica se já tem perícias
        cursor = conn.execute("SELECT COUNT(*) as total FROM pericias")
        if cursor.fetchone()['total'] > 0:
            return
        
        print("[DB] Carregando perícias...")
        conn.executemany(
            "INSERT INTO pericias (nome, nome_display, atributo_base, descricao) VALUES (?, ?, ?, ?)",
            PERICIAS
        )
        
        print("[DB] Carregando idiomas...")
        conn.executemany(
            "INSERT INTO idiomas (nome, tipo, falantes) VALUES (?, ?, ?)",
            IDIOMAS
        )


def popular_tipos_criatura():
    """Popula tipos de criatura D&D 5e no banco"""
    with get_connection() as conn:
        # Verifica se já tem tipos
        cursor = conn.execute("SELECT COUNT(*) as total FROM tipos_criatura")
        if cursor.fetchone()['total'] > 0:
            return
        
        print("[DB] Carregando tipos de criatura...")
        conn.executemany(
            "INSERT INTO tipos_criatura (nome, nome_display, descricao, exemplos) VALUES (?, ?, ?, ?)",
            TIPOS_CRIATURA
        )


def inserir_raca(conn, dados: dict, fonte: str = 'PHB'):
    """
    Insere uma raça no banco de dados
    
    Args:
        conn: Conexão com o banco
        dados: Dicionário com dados da raça
        fonte: Código do livro (PHB, MM, XGE, TCE, etc)
    """
    # Valores padrão
    defaults = {
        'categoria': 'Livro do Jogador',
        'bonus_atributos': json_dumps({}),
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': json_dumps(['Comum']),
        'proficiencias_armas': json_dumps([]),
        'proficiencias_armaduras': json_dumps([]),
        'proficiencias_ferramentas': json_dumps([]),
        'pericias_bonus': json_dumps([]),
        'caracteristicas': json_dumps([]),
        'resistencias': json_dumps([]),
        'imunidades': json_dumps([]),
        'atributos_escolha': 0,
        'pericias_escolha': 0,
        'idiomas_escolha': 0,
        'pericias_opcoes': json_dumps([]),
        'subraca_de': None,
        'fonte': fonte,
    }
    
    # Mescla dados com defaults
    for key, value in defaults.items():
        dados.setdefault(key, value)
    
    # Garante que campos JSON estejam serializados
    campos_json = [
        'bonus_atributos', 'idiomas', 'proficiencias_armas', 
        'proficiencias_armaduras', 'proficiencias_ferramentas',
        'pericias_bonus', 'caracteristicas', 'resistencias', 
        'imunidades', 'pericias_opcoes'
    ]
    for campo in campos_json:
        if isinstance(dados.get(campo), (list, dict)):
            dados[campo] = json_dumps(dados[campo])
    
    conn.execute("""
        INSERT INTO racas (
            nome, categoria, fonte, bonus_atributos, velocidade, tamanho,
            idiomas, proficiencias_armas, proficiencias_armaduras,
            proficiencias_ferramentas, pericias_bonus, caracteristicas,
            resistencias, imunidades, atributos_escolha, pericias_escolha,
            idiomas_escolha, pericias_opcoes, subraca_de
        ) VALUES (
            :nome, :categoria, :fonte, :bonus_atributos, :velocidade, :tamanho,
            :idiomas, :proficiencias_armas, :proficiencias_armaduras,
            :proficiencias_ferramentas, :pericias_bonus, :caracteristicas,
            :resistencias, :imunidades, :atributos_escolha, :pericias_escolha,
            :idiomas_escolha, :pericias_opcoes, :subraca_de
        )
    """, dados)


def inserir_classe(conn, dados: dict, fonte: str = 'PHB'):
    """
    Insere uma classe no banco de dados
    
    Args:
        conn: Conexão com o banco
        dados: Dicionário com dados da classe
        fonte: Código do livro (PHB, TCE, XGE, etc)
    """
    # Valores padrão
    defaults = {
        'salvaguardas_proficientes': json_dumps([]),
        'armaduras': json_dumps([]),
        'armas': json_dumps([]),
        'ferramentas': json_dumps([]),
        'pericias_disponiveis': json_dumps([]),
        'qtd_pericias': 2,
        'caracteristicas_nivel_1': json_dumps([]),
        'conjurador': 0,
        'atributo_conjuracao': None,
        'truques_nivel_1': 0,
        'magias_conhecidas_nivel_1': 0,
        'fonte': fonte,
    }
    
    # Mescla dados com defaults
    for key, value in defaults.items():
        dados.setdefault(key, value)
    
    # Garante que campos JSON estejam serializados
    campos_json = [
        'salvaguardas_proficientes', 'armaduras', 'armas', 
        'ferramentas', 'pericias_disponiveis', 'caracteristicas_nivel_1'
    ]
    for campo in campos_json:
        if isinstance(dados.get(campo), (list, dict)):
            dados[campo] = json_dumps(dados[campo])
    
    conn.execute("""
        INSERT INTO classes (
            nome, fonte, dado_vida, hp_primeiro_nivel, salvaguardas_proficientes,
            armaduras, armas, ferramentas, pericias_disponiveis, qtd_pericias,
            caracteristicas_nivel_1, conjurador, atributo_conjuracao,
            truques_nivel_1, magias_conhecidas_nivel_1
        ) VALUES (
            :nome, :fonte, :dado_vida, :hp_primeiro_nivel, :salvaguardas_proficientes,
            :armaduras, :armas, :ferramentas, :pericias_disponiveis, :qtd_pericias,
            :caracteristicas_nivel_1, :conjurador, :atributo_conjuracao,
            :truques_nivel_1, :magias_conhecidas_nivel_1
        )
    """, dados)
