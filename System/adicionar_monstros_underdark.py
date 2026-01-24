"""
Adiciona novos monstros do Underdark ao sistema
Monstros de Out of the Abyss - Apêndice C
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.modulos.database import get_connection, json_dumps


def adicionar_monstros_underdark():
    """Adiciona monstros específicos do Underdark"""
    
    monstros = [
        # DERRO
        {
            'nome': 'Derro',
            'tipo': 'humanoide',
            'tamanho': 'Pequeno',
            'alinhamento': 'Caótico e Mau',
            'nd': 0.25,
            'xp': 50,
            'ca': 13,
            'ca_tipo': 'armadura de couro batido',
            'hp_medio': 13,
            'hp_formula': '3d6+3',
            'atributos': json_dumps({
                'forca': 10, 'destreza': 14, 'constituicao': 12,
                'inteligencia': 11, 'sabedoria': 5, 'carisma': 9
            }),
            'velocidade': json_dumps({'normal': 30}),
            'pericias': json_dumps({'furtividade': 4}),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 7,
            'idiomas': json_dumps(['Anão', 'Subterrâneo']),
            'habilidades': json_dumps([
                {
                    'nome': 'Insanidade',
                    'descricao': 'Vantagem em salvaguardas contra ser enfeitiçado ou amedrontado.'
                },
                {
                    'nome': 'Conjuração Inata',
                    'descricao': 'CAR é a habilidade de conjuração (CD 12). Pode conjurar: À vontade: ilusão menor; 1/dia: escuridão, medo.'
                },
                {
                    'nome': 'Resistência à Magia',
                    'descricao': 'Vantagem em salvaguardas contra magias e efeitos mágicos.'
                },
                {
                    'nome': 'Sensibilidade à Luz Solar',
                    'descricao': 'Desvantagem em ataques e testes de Percepção que dependam de visão sob luz solar.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Azagaia',
                    'descricao': 'Ataque corpo a corpo ou à distância: +4 para acertar, alcance 1,5m ou 9/36m.',
                    'ataque': '+4',
                    'dano': '1d6+2',
                    'tipo_dano': 'perfurante'
                },
                {
                    'nome': 'Besta de Mão',
                    'descricao': 'Ataque à distância: +4 para acertar, alcance 9/36m.',
                    'ataque': '+4',
                    'dano': '1d6+2',
                    'tipo_dano': 'perfurante'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # IXITXACHITL
        {
            'nome': 'Ixitxachitl',
            'tipo': 'aberração',
            'tamanho': 'Pequeno',
            'alinhamento': 'Caótico e Mau',
            'nd': 0.25,
            'xp': 50,
            'ca': 15,
            'ca_tipo': 'armadura natural',
            'hp_medio': 18,
            'hp_formula': '4d6+4',
            'atributos': json_dumps({
                'forca': 12, 'destreza': 16, 'constituicao': 13,
                'inteligencia': 12, 'sabedoria': 13, 'carisma': 7
            }),
            'velocidade': json_dumps({'nadando': 30}),
            'sentidos': json_dumps({'visão no escuro': 60}),
            'percepcao_passiva': 11,
            'idiomas': json_dumps(['Abissal', 'Ixitxachitl']),
            'acoes': json_dumps([
                {
                    'nome': 'Mordida',
                    'descricao': 'Ataque corpo a corpo: +3 para acertar, alcance 1,5m.',
                    'ataque': '+3',
                    'dano': '1d6+1',
                    'tipo_dano': 'perfurante'
                }
            ]),
            'reacoes': json_dumps([
                {
                    'nome': 'Cauda Denteada',
                    'descricao': 'Quando uma criatura provocar ataque de oportunidade, pode fazer este ataque no lugar da mordida. +5 para acertar, 1d8+3 perfurante.'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # IXITXACHITL VAMPÍRICA
        {
            'nome': 'Ixitxachitl Vampírica',
            'tipo': 'aberração',
            'tamanho': 'Médio',
            'alinhamento': 'Caótico e Mau',
            'nd': 2,
            'xp': 450,
            'ca': 16,
            'ca_tipo': 'armadura natural',
            'hp_medio': 44,
            'hp_formula': '8d8+8',
            'atributos': json_dumps({
                'forca': 14, 'destreza': 18, 'constituicao': 13,
                'inteligencia': 12, 'sabedoria': 13, 'carisma': 7
            }),
            'velocidade': json_dumps({'nadando': 30}),
            'sentidos': json_dumps({'visão no escuro': 60}),
            'percepcao_passiva': 11,
            'idiomas': json_dumps(['Abissal', 'Ixitxachitl']),
            'habilidades': json_dumps([
                {
                    'nome': 'Regeneração',
                    'descricao': 'Recupera 10 HP no início de seu turno. Morre apenas se iniciar com 0 HP.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Mordida Vampírica',
                    'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 1,5m.',
                    'ataque': '+6',
                    'dano': '1d8+4',
                    'tipo_dano': 'perfurante',
                    'extra': 'CD 11 CON ou HP máximo reduzido em valor igual ao dano. Ixitxachitl recupera mesma quantidade.'
                }
            ]),
            'reacoes': json_dumps([
                {
                    'nome': 'Cauda Denteada',
                    'descricao': 'Quando uma criatura provocar ataque de oportunidade. +8 para acertar, alcance 3m, 1d10+4 perfurante.'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # DUERGAR LÂMINA DA ALMA
        {
            'nome': 'Duergar Lâmina da Alma',
            'tipo': 'humanoide',
            'tamanho': 'Médio',
            'alinhamento': 'Leal e Mau',
            'nd': 1,
            'xp': 200,
            'ca': 14,
            'ca_tipo': 'armadura de couro',
            'hp_medio': 18,
            'hp_formula': '4d8',
            'atributos': json_dumps({
                'forca': 11, 'destreza': 16, 'constituicao': 10,
                'inteligencia': 11, 'sabedoria': 10, 'carisma': 12
            }),
            'velocidade': json_dumps({'normal': 25}),
            'resistencias': json_dumps(['veneno']),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 10,
            'idiomas': json_dumps(['Anão', 'Subterrâneo']),
            'habilidades': json_dumps([
                {
                    'nome': 'Resistência Duergar',
                    'descricao': 'Vantagem em salvaguardas contra veneno, magia e ilusões.'
                },
                {
                    'nome': 'Conjuração Inata (Psiônico)',
                    'descricao': 'SAB é a habilidade (CD 12). À vontade: ataque certeiro, proteção contra lâminas; 3/dia: marca do caçador, salto.'
                },
                {
                    'nome': 'Sensibilidade à Luz Solar',
                    'descricao': 'Desvantagem em ataques e testes de Percepção sob luz solar.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Aumentar (Recarrega em Descanso)',
                    'descricao': 'Por 1 minuto, fica Grande, dobrando dados de dano de ataques baseados em FOR, vantagem em FOR e salvaguardas de FOR.'
                },
                {
                    'nome': 'Criar Lâmina da Alma',
                    'descricao': 'Cria uma lâmina visível de energia psíquica que desaparece se soltar ou for incapacitado.'
                },
                {
                    'nome': 'Invisibilidade (Recarrega em Descanso)',
                    'descricao': 'Fica invisível até atacar, conjurar, usar Aumentar ou perder concentração por até 1 hora.'
                },
                {
                    'nome': 'Lâmina da Alma',
                    'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 1,5m.',
                    'ataque': '+5',
                    'dano': '1d6+3',
                    'tipo_dano': 'energético',
                    'extra': '2d6+3 quando aumentado. +1d6 energético se tiver vantagem.'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # DUERGAR GUARDA DE PEDRA
        {
            'nome': 'Duergar Guarda de Pedra',
            'tipo': 'humanoide',
            'tamanho': 'Médio',
            'alinhamento': 'Leal e Mau',
            'nd': 2,
            'xp': 450,
            'ca': 18,
            'ca_tipo': 'cota de malha e escudo',
            'hp_medio': 39,
            'hp_formula': '6d8+12',
            'atributos': json_dumps({
                'forca': 18, 'destreza': 11, 'constituicao': 14,
                'inteligencia': 11, 'sabedoria': 10, 'carisma': 9
            }),
            'velocidade': json_dumps({'normal': 25}),
            'resistencias': json_dumps(['veneno']),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 10,
            'idiomas': json_dumps(['Anão', 'Subterrâneo']),
            'habilidades': json_dumps([
                {
                    'nome': 'Resistência Duergar',
                    'descricao': 'Vantagem em salvaguardas contra veneno, magia e ilusões.'
                },
                {
                    'nome': 'Formação de Falange',
                    'descricao': 'Vantagem em ataques e salvaguardas de DEX se estiver a 1,5m de aliado duergar com escudo.'
                },
                {
                    'nome': 'Sensibilidade à Luz Solar',
                    'descricao': 'Desvantagem em ataques e testes de Percepção sob luz solar.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Aumentar (Recarrega em Descanso)',
                    'descricao': 'Por 1 minuto, fica Grande, dobrando dados de dano de ataques baseados em FOR.'
                },
                {
                    'nome': 'Invisibilidade (Recarrega em Descanso)',
                    'descricao': 'Fica invisível até atacar, conjurar, usar Aumentar ou perder concentração por até 1 hora.'
                },
                {
                    'nome': 'Azagaia',
                    'descricao': 'Ataque corpo a corpo ou à distância: +6 para acertar, alcance 1,5m ou 9/36m.',
                    'ataque': '+6',
                    'dano': '1d6+4',
                    'tipo_dano': 'perfurante',
                    'extra': '2d6+4 quando aumentado'
                },
                {
                    'nome': 'Faca do Rei (Espada Curta)',
                    'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 1,5m.',
                    'ataque': '+6',
                    'dano': '1d6+4',
                    'tipo_dano': 'perfurante',
                    'extra': '2d6+4 quando aumentado'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # DUERGAR XARRORN
        {
            'nome': 'Duergar Xarrorn',
            'tipo': 'humanoide',
            'tamanho': 'Médio',
            'alinhamento': 'Leal e Mau',
            'nd': 2,
            'xp': 450,
            'ca': 18,
            'ca_tipo': 'armadura de placas',
            'hp_medio': 26,
            'hp_formula': '4d8+8',
            'atributos': json_dumps({
                'forca': 16, 'destreza': 11, 'constituicao': 14,
                'inteligencia': 11, 'sabedoria': 10, 'carisma': 9
            }),
            'velocidade': json_dumps({'normal': 25}),
            'resistencias': json_dumps(['veneno']),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 10,
            'idiomas': json_dumps(['Anão', 'Subterrâneo']),
            'habilidades': json_dumps([
                {
                    'nome': 'Resistência Duergar',
                    'descricao': 'Vantagem em salvaguardas contra veneno, magia e ilusões.'
                },
                {
                    'nome': 'Sensibilidade à Luz Solar',
                    'descricao': 'Desvantagem em ataques e testes de Percepção sob luz solar.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Aumentar (Recarrega em Descanso)',
                    'descricao': 'Por 1 minuto, fica Grande, dobrando dados de dano de ataques baseados em FOR.'
                },
                {
                    'nome': 'Invisibilidade (Recarrega em Descanso)',
                    'descricao': 'Fica invisível até atacar, conjurar, usar Aumentar ou perder concentração por até 1 hora.'
                },
                {
                    'nome': 'Lança Flamejante',
                    'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 3m. Desvantagem se alvo estiver a 1,5m.',
                    'ataque': '+5',
                    'dano': '1d12+3',
                    'tipo_dano': 'perfurante',
                    'extra': '+1d6 ígneo. 2d12+3 perfurante quando aumentado.'
                },
                {
                    'nome': 'Rajada de Fogo (Recarrega 5-6)',
                    'descricao': 'Cone 4,5m ou linha 10m x 1,5m. CD 12 DEX, 3d6 ígneo (metade em sucesso).'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # TROGLODITA CAMPEÃO DE LAOGZED
        {
            'nome': 'Troglodita Campeão de Laogzed',
            'tipo': 'humanoide',
            'tamanho': 'Médio',
            'alinhamento': 'Caótico e Mau',
            'nd': 3,
            'xp': 700,
            'ca': 14,
            'ca_tipo': 'armadura natural',
            'hp_medio': 59,
            'hp_formula': '7d8+28',
            'atributos': json_dumps({
                'forca': 18, 'destreza': 12, 'constituicao': 18,
                'inteligencia': 8, 'sabedoria': 12, 'carisma': 12
            }),
            'velocidade': json_dumps({'normal': 30}),
            'pericias': json_dumps({'atletismo': 6, 'furtividade': 3, 'intimidação': 3}),
            'sentidos': json_dumps({'visão no escuro': 60}),
            'percepcao_passiva': 11,
            'idiomas': json_dumps(['Troglodita']),
            'habilidades': json_dumps([
                {
                    'nome': 'Fedor',
                    'descricao': 'Criaturas que não sejam trogloditas a 1,5m devem fazer CD 12 CON ou ficam envenenadas até próximo turno.'
                },
                {
                    'nome': 'Pele de Camaleão',
                    'descricao': 'Vantagem em testes de Furtividade para se esconder.'
                },
                {
                    'nome': 'Sensibilidade à Luz Solar',
                    'descricao': 'Desvantagem em ataques e testes de Percepção sob luz solar.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Ataques Múltiplos',
                    'descricao': 'Faz três ataques: um com mordida e dois com garras.'
                },
                {
                    'nome': 'Clava Grande',
                    'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 1,5m.',
                    'ataque': '+6',
                    'dano': '1d8+4',
                    'tipo_dano': 'contundente'
                },
                {
                    'nome': 'Garra',
                    'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 1,5m.',
                    'ataque': '+6',
                    'dano': '1d4+4',
                    'tipo_dano': 'cortante'
                },
                {
                    'nome': 'Mordida',
                    'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 1,5m.',
                    'ataque': '+6',
                    'dano': '1d4+4',
                    'tipo_dano': 'perfurante'
                },
                {
                    'nome': 'Jato Ácido (Recarrega 6)',
                    'descricao': 'Linha 4,5m x 1,5m. CD 14 DEX, 3d6 ácido (metade em sucesso).'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # MADRINHA DE ZUGGTMOY
        {
            'nome': 'Madrinha de Zuggtmoy',
            'tipo': 'planta',
            'tamanho': 'Médio',
            'alinhamento': 'Caótico e Mau',
            'nd': 0.125,
            'xp': 25,
            'ca': 13,
            'ca_tipo': 'armadura natural',
            'hp_medio': 22,
            'hp_formula': '5d8',
            'atributos': json_dumps({
                'forca': 14, 'destreza': 11, 'constituicao': 11,
                'inteligencia': 14, 'sabedoria': 8, 'carisma': 18
            }),
            'velocidade': json_dumps({'normal': 20}),
            'sentidos': json_dumps({'visão no escuro': 60}),
            'percepcao_passiva': 9,
            'idiomas': json_dumps(['compreende Abissal mas não fala']),
            'habilidades': json_dumps([
                {
                    'nome': 'Passo Fúngico',
                    'descricao': 'Uma vez por turno, pode usar 3m de movimento para teleportar entre cogumelos/fungos até 6m.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Esporos Alucinógenos',
                    'descricao': 'Criatura a 1,5m deve fazer CD 10 CON ou fica envenenada e incapacitada por 1 minuto.'
                },
                {
                    'nome': 'Infestação de Esporos (1/Dia)',
                    'descricao': 'Esfera 3m de raio. CD 10 CON ou contraí "esporos de Zuggtmoy" e loucura permanente.'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # CAMAREIRO DE ZUGGTMOY
        {
            'nome': 'Camareiro de Zuggtmoy',
            'tipo': 'planta',
            'tamanho': 'Grande',
            'alinhamento': 'Caótico e Mau',
            'nd': 2,
            'xp': 450,
            'ca': 13,
            'ca_tipo': 'armadura natural',
            'hp_medio': 22,
            'hp_formula': '5d8',
            'atributos': json_dumps({
                'forca': 17, 'destreza': 7, 'constituicao': 14,
                'inteligencia': 11, 'sabedoria': 8, 'carisma': 12
            }),
            'velocidade': json_dumps({'normal': 20}),
            'resistencias': json_dumps(['contundente', 'perfurante']),
            'sentidos': json_dumps({'visão no escuro': 60}),
            'percepcao_passiva': 9,
            'idiomas': json_dumps(['Abissal', 'Subterrâneo']),
            'habilidades': json_dumps([
                {
                    'nome': 'Cogumelo Portal',
                    'descricao': 'É considerado cogumelo para efeito do Passo Fúngico das madrinhas.'
                },
                {
                    'nome': 'Esporos Venenosos',
                    'descricao': 'Quando sofre dano, libera esporos. Criaturas a 1,5m fazem CD 12 CON ou envenenadas por 1 minuto.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Ataques Múltiplos',
                    'descricao': 'Faz dois ataques de pancada.'
                },
                {
                    'nome': 'Pancada',
                    'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 1,5m.',
                    'ataque': '+5',
                    'dano': '2d6+3',
                    'tipo_dano': 'contundente'
                },
                {
                    'nome': 'Infestação de Esporos (1/Dia)',
                    'descricao': 'Esfera 3m de raio. CD 12 CON ou contraí "esporos de Zuggtmoy" e loucura permanente.'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # CORCELANTE FÊMEA
        {
            'nome': 'Corcelante Fêmea',
            'tipo': 'besta',
            'tamanho': 'Grande',
            'alinhamento': 'Sem Tendência',
            'nd': 1,
            'xp': 200,
            'ca': 14,
            'ca_tipo': 'armadura natural',
            'hp_medio': 30,
            'hp_formula': '4d10+8',
            'atributos': json_dumps({
                'forca': 15, 'destreza': 16, 'constituicao': 14,
                'inteligencia': 2, 'sabedoria': 10, 'carisma': 3
            }),
            'velocidade': json_dumps({'normal': 30, 'escalada': 30}),
            'pericias': json_dumps({'furtividade': 7}),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 10,
            'habilidades': json_dumps([
                {
                    'nome': 'Escalada Aracnídea',
                    'descricao': 'Pode escalar superfícies difíceis, incluindo tetos de cabeça para baixo, sem testes.'
                },
                {
                    'nome': 'Salto',
                    'descricao': 'Pode gastar todo movimento para saltar até 27m vertical ou horizontalmente.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Mordida',
                    'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 1,5m.',
                    'ataque': '+5',
                    'dano': '1d8+3',
                    'tipo_dano': 'perfurante',
                    'extra': 'CD 12 CON ou 2d8 ácido (metade em sucesso)'
                },
                {
                    'nome': 'Pernas Grudentas (Recarrega sem presas)',
                    'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 1,5m, criaturas Médias ou menores.',
                    'ataque': '+5',
                    'extra': 'Alvo fica agarrado (CD 12 para escapar)'
                }
            ]),
            'fonte': 'Out of the Abyss'
        },
        
        # CORCELANTE MACHO
        {
            'nome': 'Corcelante Macho',
            'tipo': 'besta',
            'tamanho': 'Médio',
            'alinhamento': 'Sem Tendência',
            'nd': 0.25,
            'xp': 50,
            'ca': 12,
            'ca_tipo': 'armadura natural',
            'hp_medio': 13,
            'hp_formula': '2d8+4',
            'atributos': json_dumps({
                'forca': 15, 'destreza': 12, 'constituicao': 14,
                'inteligencia': 2, 'sabedoria': 10, 'carisma': 3
            }),
            'velocidade': json_dumps({'normal': 30, 'escalada': 30}),
            'pericias': json_dumps({'furtividade': 5}),
            'sentidos': json_dumps({'visão no escuro': 120}),
            'percepcao_passiva': 10,
            'habilidades': json_dumps([
                {
                    'nome': 'Escalada Aracnídea',
                    'descricao': 'Pode escalar superfícies difíceis, incluindo tetos de cabeça para baixo, sem testes.'
                },
                {
                    'nome': 'Salto',
                    'descricao': 'Pode gastar todo movimento para saltar até 18m vertical ou horizontalmente.'
                }
            ]),
            'acoes': json_dumps([
                {
                    'nome': 'Mordida',
                    'descricao': 'Ataque corpo a corpo: +4 para acertar, alcance 1,5m.',
                    'ataque': '+4',
                    'dano': '1d8+2',
                    'tipo_dano': 'perfurante',
                    'extra': 'CD 12 CON ou 1d8 ácido (metade em sucesso)'
                },
                {
                    'nome': 'Pernas Grudentas (Recarrega sem presas)',
                    'descricao': 'Ataque corpo a corpo: +4 para acertar, alcance 1,5m, criaturas Pequenas ou Miúdas.',
                    'ataque': '+4',
                    'extra': 'Alvo fica agarrado (CD 12 para escapar)'
                }
            ]),
            'fonte': 'Out of the Abyss'
        }
    ]
    
    with get_connection() as conn:
        # Verifica se já existem esses monstros
        for monstro in monstros:
            cursor = conn.execute(
                "SELECT COUNT(*) as total FROM monstros WHERE nome = ?",
                (monstro['nome'],)
            )
            if cursor.fetchone()['total'] > 0:
                print(f"Monstro '{monstro['nome']}' já existe, pulando...")
                continue
                
            # Insere o monstro
            conn.execute("""
                INSERT INTO monstros (
                    nome, tipo, tamanho, alinhamento, nd, xp, ca, ca_tipo, 
                    hp_medio, hp_formula, atributos, velocidade, salvaguardas,
                    pericias, resistencias, imunidades_dano, imunidades_condicao,
                    vulnerabilidades, sentidos, percepcao_passiva, idiomas, 
                    habilidades, acoes, acoes_bonus, reacoes, acoes_lendarias, fonte
                ) VALUES (
                    :nome, :tipo, :tamanho, :alinhamento, :nd, :xp, :ca, :ca_tipo,
                    :hp_medio, :hp_formula, :atributos, :velocidade, :salvaguardas,
                    :pericias, :resistencias, :imunidades_dano, :imunidades_condicao,
                    :vulnerabilidades, :sentidos, :percepcao_passiva, :idiomas,
                    :habilidades, :acoes, :acoes_bonus, :reacoes, :acoes_lendarias, :fonte
                )
            """, {
                'nome': monstro['nome'],
                'tipo': monstro['tipo'],
                'tamanho': monstro['tamanho'],
                'alinhamento': monstro['alinhamento'],
                'nd': monstro['nd'],
                'xp': monstro['xp'],
                'ca': monstro['ca'],
                'ca_tipo': monstro.get('ca_tipo'),
                'hp_medio': monstro['hp_medio'],
                'hp_formula': monstro['hp_formula'],
                'atributos': monstro['atributos'],
                'velocidade': monstro['velocidade'],
                'salvaguardas': monstro.get('salvaguardas', '{}'),
                'pericias': monstro.get('pericias', '{}'),
                'resistencias': monstro.get('resistencias', '[]'),
                'imunidades_dano': monstro.get('imunidades_dano', '[]'),
                'imunidades_condicao': monstro.get('imunidades_condicao', '[]'),
                'vulnerabilidades': monstro.get('vulnerabilidades', '[]'),
                'sentidos': monstro.get('sentidos', '{}'),
                'percepcao_passiva': monstro.get('percepcao_passiva', 10),
                'idiomas': monstro.get('idiomas', '[]'),
                'habilidades': monstro.get('habilidades', '[]'),
                'acoes': monstro.get('acoes', '[]'),
                'acoes_bonus': monstro.get('acoes_bonus', '[]'),
                'reacoes': monstro.get('reacoes', '[]'),
                'acoes_lendarias': monstro.get('acoes_lendarias', '[]'),
                'fonte': monstro.get('fonte', 'Out of the Abyss')
            })
            
            print(f"✓ Adicionado: {monstro['nome']} (ND {monstro['nd']})")

    print(f"\n🎯 Monstros do Underdark adicionados com sucesso!")


if __name__ == "__main__":
    print("=== Adicionando Monstros do Underdark ===\n")
    adicionar_monstros_underdark()