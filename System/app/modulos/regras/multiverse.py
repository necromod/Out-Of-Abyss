"""
Raças do Monsters of the Multiverse

Fonte: MPMM (Mordenkainen Presents: Monsters of the Multiverse)

Característica principal: Sistema de bônus de atributos flexível
- O jogador escolhe onde aplicar +2/+1 ou +1/+1/+1

Raças incluídas: 33 raças reimaginadas
"""

from ..database import get_connection, json_dumps
from .base import inserir_raca


# ==================== RAÇAS DO MULTIVERSE ====================

RACAS_MULTIVERSE = [
    # Aarakocra
    {
        'nome': 'Aarakocra',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Voo (velocidade igual à terrestre)',
            'Garras: Ataque desarmado 1d6 + FOR cortante',
            'Rajada de Vento: 1x/descanso longo'
        ],
    },
    
    # Aasimar
    {
        'nome': 'Aasimar',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum', 'Celestial'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resistência Celestial: Resistência a necrótico e radiante',
            'Mãos Curativas: Cura PV = bônus de proficiência (1x/descanso longo)',
            'Portador da Luz: Truque Luz',
            'Revelação Celestial (nível 3): Transformação 1x/descanso longo'
        ],
        'resistencias': ['necrótico', 'radiante'],
    },
    
    # Bugbear
    {
        'nome': 'Bugbear',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'pericias_bonus': ['furtividade'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Constituição Feérica: Vantagem contra encantamento, imune a sono mágico',
            'Membros Longos: +1,5m de alcance em ataques corpo a corpo no seu turno',
            'Físico Poderoso: Conta como Grande para capacidade de carga',
            'Ataque Surpresa: +2d6 de dano em criaturas surpresas'
        ],
    },
    
    # Centauro
    {
        'nome': 'Centauro',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 12,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Investida: Bônus de dano após mover 9m em linha reta',
            'Forma Equina: Velocidade 12m, conta como montaria',
            'Cascos: Ataque desarmado 1d6 + FOR contundente'
        ],
    },
    
    # Changeling
    {
        'nome': 'Changeling',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 2,
        'caracteristicas': [
            'Instintos do Changeling: Proficiência em 2 perícias à escolha',
            'Metamorfose: Pode alterar aparência como ação'
        ],
        'pericias_escolha': 2,
    },
    
    # Deep Gnome (Svirfneblin)
    {
        'nome': 'Gnomo das Profundezas',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Gnômico', 'Subcomum'],
        'caracteristicas': [
            'Visão no Escuro (36m)',
            'Presente da Svirfneblin: Disfarçar-se, Passos sem Pegadas ou Nondetection',
            'Camuflagem Gnômica: Vantagem em Furtividade em terreno rochoso',
            'Esperteza Gnômica: Vantagem contra magia (INT, SAB, CAR)'
        ],
    },
    
    # Duergar
    {
        'nome': 'Duergar',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Anão'],
        'caracteristicas': [
            'Visão no Escuro (36m)',
            'Resiliência Duergar: Vantagem contra ilusões, encantamento e paralisia',
            'Magia Duergar: Ampliar/Reduzir (nível 3), Invisibilidade (nível 5)',
            'Constituição Anã: Resistência a veneno'
        ],
        'resistencias': ['veneno'],
    },
    
    # Eladrin
    {
        'nome': 'Eladrin',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono mágico',
            'Passo Feérico: Teleporte bônus 9m (bônus de prof/descanso longo)',
            'Transe: 4h de meditação = 8h de sono'
        ],
    },
    
    # Fairy
    {
        'nome': 'Fada',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Voo (velocidade igual à terrestre)',
            'Magia Feérica: Druídico, Fogo das Fadas (nv3), Ampliar/Reduzir (nv5)',
            'Passagem Feérica: Pode atravessar espaços de criaturas maiores'
        ],
    },
    
    # Firbolg
    {
        'nome': 'Firbolg',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Magia Firbolg: Detectar Magia, Disfarçar-se',
            'Passo Oculto: Bônus invisibilidade até início do próximo turno',
            'Físico Poderoso: Conta como Grande para carga',
            'Fala das Bestas e Folhas: Comunicação limitada com plantas e animais'
        ],
    },
    
    # Genasi do Ar
    {
        'nome': 'Genasi do Ar',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 10,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Não precisa respirar',
            'Resistência a raios',
            'Respiração Interminável: Pode prender respiração indefinidamente',
            'Misturar-se ao Vento: Levitação (nv3), Passo Nebuloso (nv5)'
        ],
        'resistencias': ['elétrico'],
    },
    
    # Genasi da Terra
    {
        'nome': 'Genasi da Terra',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Caminhada na Terra: Pode mover por terreno difícil não-mágico sem custo extra',
            'Mesclar-se à Pedra: Passar sem Deixar Rastro, Pico de Pedra (nv5)'
        ],
    },
    
    # Genasi do Fogo
    {
        'nome': 'Genasi do Fogo',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resistência a fogo',
            'Alcançar as Chamas: Produzir Chamas, Mãos Flamejantes (nv3), Lâmina Flamejante (nv5)'
        ],
        'resistencias': ['fogo'],
    },
    
    # Genasi da Água
    {
        'nome': 'Genasi da Água',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Anfíbio: Pode respirar ar e água',
            'Resistência a ácido',
            'Natação: Velocidade de natação igual à terrestre',
            'Chamado das Ondas: Moldar Água, Criar/Destruir Água (nv3), Caminhar na Água (nv5)'
        ],
        'resistencias': ['ácido'],
    },
    
    # Githyanki
    {
        'nome': 'Githyanki',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Gith'],
        'caracteristicas': [
            'Resistência Astral: Vantagem contra encantamento',
            'Prodígio Githyanki: Proficiências à escolha',
            'Psiônicos Githyanki: Mão Mágica, Salto (nv3), Passo Nebuloso (nv5)'
        ],
    },
    
    # Githzerai
    {
        'nome': 'Githzerai',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Gith'],
        'caracteristicas': [
            'Resistência Mental: Vantagem contra encantamento',
            'Disciplina Githzerai: Pode usar reação para cancelar Amedrontado/Enfeitiçado',
            'Psiônicos Githzerai: Mão Mágica, Escudo (nv3), Detectar Pensamentos (nv5)'
        ],
    },
    
    # Goblin
    {
        'nome': 'Goblin',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Goblin'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Fúria dos Pequenos: Dano extra = bônus de proficiência (prof/descanso longo)',
            'Fuga Ágil: Desengajar ou Esconder como ação bônus'
        ],
    },
    
    # Goliath
    {
        'nome': 'Goliath',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'pericias_bonus': ['atletismo'],
        'caracteristicas': [
            'Atleta Natural: Proficiência em Atletismo',
            'Constituição de Gigante da Pedra: Resistência a frio',
            'Físico Poderoso: Conta como Grande para carga',
            'Resistência de Montanha: Reduz dano = 1d12 + CON (prof/descanso longo)'
        ],
        'resistencias': ['gélido'],
    },
    
    # Harengon
    {
        'nome': 'Harengon',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'pericias_bonus': ['percepcao'],
        'caracteristicas': [
            'Pulo de Coelho: Salto em distância como ação bônus = prof x 1,5m',
            'Intuição de Lebre: +bônus de prof em iniciativa',
            'Sorte de Lebre: Reação para adicionar d4 em salvaguarda'
        ],
    },
    
    # Hobgoblin
    {
        'nome': 'Hobgoblin',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Goblin'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Constituição Feérica: Vantagem contra encantamento, imune a sono mágico',
            'Presente da Legião Fantasma: Truque de ilusão/encantamento + Ajuda (prof/descanso longo)',
            'Fortuna dos Muitos: +d6 em ataque/salvaguarda/teste se aliado visível em 9m'
        ],
    },
    
    # Kenku
    {
        'nome': 'Kenku',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Recordação de Especialista: Proficiência em 2 perícias à escolha',
            'Imitação: Vantagem em testes para imitar sons',
            'Recital de Kenku: Pode usar Prestidigitação, Falar com Animais ou similares'
        ],
        'pericias_escolha': 2,
    },
    
    # Kobold
    {
        'nome': 'Kobold',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Pequeno',
        'idiomas': ['Comum', 'Dracônico'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Rugido Dracônico: Aliados em 3m têm vantagem (prof/descanso longo)',
            'Legado Dracônico: Escolha uma característica dracônica',
            'Sorcaria Kobold: 1 truque de feiticeiro'
        ],
    },
    
    # Lizardfolk (Povo-Lagarto)
    {
        'nome': 'Povo-Lagarto',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Mordida: Ataque desarmado 1d6 + FOR perfurante',
            'Prender a Respiração: Até 15 minutos',
            'Mandíbulas Famintas: HP temp = prof (prof/descanso longo)',
            'Armadura Natural: CA = 13 + DES sem armadura',
            'Artesanato Natural: Pode criar escudo/arma de restos'
        ],
    },
    
    # Minotaur
    {
        'nome': 'Minotauro',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Chifres: Ataque desarmado 1d6 + FOR perfurante',
            'Investida com Chifres: +2d6 após mover 6m em linha reta',
            'Marrada: Empurra como ação bônus após acertar com chifres',
            'Memória Labiríntica: Vantagem para lembrar caminhos'
        ],
    },
    
    # Orc
    {
        'nome': 'Orc',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Orc'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Adrenalina: Ação bônus para mover velocidade em direção a inimigo',
            'Resistência Implacável: 1x/descanso longo, ao cair para 0 HP, cai para 1 HP',
            'Físico Poderoso: Conta como Grande para carga'
        ],
    },
    
    # Satyr (Sátiro)
    {
        'nome': 'Sátiro',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 10,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Tipo Criatura: Feérico (não humanoide)',
            'Resistência Mágica: Vantagem em salvaguardas contra magia',
            'Salto de Miriti: Salto em distância extra',
            'Chifrada: Ataque desarmado 1d6 + FOR contundente',
            'Artista Revelador: Proficiência em Performance + 1 instrumento'
        ],
    },
    
    # Sea Elf (Elfo do Mar)
    {
        'nome': 'Elfo do Mar',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono',
            'Filho do Mar: Pode respirar água, natação = velocidade',
            'Amigo do Mar: Comunicação simples com bestas aquáticas',
            'Transe: 4h = 8h sono'
        ],
    },
    
    # Shadar-kai
    {
        'nome': 'Shadar-kai',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum', 'Élfico'],
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono',
            'Resistência Necrótica',
            'Bênção da Rainha Corvo: Teleporte 9m + resistência (prof/descanso longo)',
            'Transe: 4h = 8h sono'
        ],
        'resistencias': ['necrótico'],
    },
    
    # Shifter
    {
        'nome': 'Shifter',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Instintos Bestiais: Proficiência em Acrobacia, Atletismo, Intuição ou Sobrevivência',
            'Mudar: HP temp + característica bestial (prof/descanso longo)'
        ],
        'pericias_opcoes': ['acrobacia', 'atletismo', 'intuicao', 'sobrevivencia'],
    },
    
    # Tabaxi
    {
        'nome': 'Tabaxi',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Garras de Gato: Ataque desarmado 1d6 + FOR cortante, escalada = velocidade',
            'Talento Felino: Proficiência em Percepção e Furtividade',
            'Agilidade Felina: Dobra velocidade até fim do turno (recarga)'
        ],
        'pericias_bonus': ['percepcao', 'furtividade'],
    },
    
    # Tortle
    {
        'nome': 'Tortle',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Garras: Ataque desarmado 1d6 + FOR cortante',
            'Prender Respiração: 1 hora',
            'Armadura Natural: CA 17 (não pode usar armadura)',
            'Defesa do Casco: +4 CA quando entra no casco (ação)'
        ],
    },
    
    # Triton (Tritão)
    {
        'nome': 'Tritão',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Anfíbio: Respira ar e água',
            'Resistência a frio',
            'Emissário do Mar: Comunicação com criaturas aquáticas',
            'Guardião das Profundezas: Resistência a dano de profundidade',
            'Controle de Ar e Água: Névoa Obscurecente, Rajada de Vento (nv3), Caminhar na Água (nv5)'
        ],
        'resistencias': ['gélido'],
    },
    
    # Yuan-ti
    {
        'nome': 'Yuan-ti',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'caracteristicas': [
            'Visão no Escuro (18m)',
            'Resistência Mágica: Vantagem em salvaguardas contra magia',
            'Resistência a veneno, imunidade a condição envenenado',
            'Magia Serpentina: Veneno por Contato, Sugestão (nv3)'
        ],
        'resistencias': ['veneno'],
    },
    
    # Owlin
    {
        'nome': 'Owlin',
        'categoria': 'Monsters of the Multiverse',
        'bonus_atributos': {},
        'atributos_escolha': 3,
        'velocidade': 9,
        'tamanho': 'Médio ou Pequeno',
        'idiomas': ['Comum'],
        'idiomas_escolha': 1,
        'pericias_bonus': ['furtividade'],
        'caracteristicas': [
            'Visão no Escuro (36m)',
            'Voo (velocidade igual à terrestre, não pode usar armadura média/pesada)',
            'Voo Silencioso: Proficiência em Furtividade'
        ],
    },
]


# ==================== FUNÇÃO DE POPULAÇÃO ====================

def popular_racas_multiverse():
    """Popula raças do Monsters of the Multiverse no banco"""
    with get_connection() as conn:
        print("[DB] Carregando raças do Monsters of the Multiverse...")
        for raca in RACAS_MULTIVERSE:
            inserir_raca(conn, raca.copy(), fonte='MPMM')
