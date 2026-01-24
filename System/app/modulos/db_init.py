"""
Inicialização do Banco de Dados
Cria dados iniciais para teste e uso
"""

from .database import init_database, get_connection, json_dumps, migrate_database
from .regras import popular_todas_regras


def popular_dados_iniciais():
    """Popula o banco com dados iniciais"""
    
    # Primeiro, executar migrações pendentes
    migrate_database()
    
    # Popular regras D&D (sistema modular)
    popular_todas_regras()
    
    with get_connection() as conn:
        # Verifica se já tem dados
        cursor = conn.execute("SELECT COUNT(*) as total FROM configuracoes")
        if cursor.fetchone()['total'] > 0:
            return  # Já inicializado
        
        # ==================== CONFIGURAÇÕES ====================
        configs = [
            ('regras_xanathar', '0'),
            ('regras_tasha', '0'),
            ('regras_underdark', '1'),  # Ativo por padrão para Out of the Abyss
            ('usar_fome_sede', '1'),
            ('usar_exaustao_underdark', '1'),
            ('tema', 'escuro'),
            ('auto_save', '1'),
            ('intervalo_save', '30'),  # segundos
        ]
        conn.executemany(
            "INSERT INTO configuracoes (chave, valor) VALUES (?, ?)",
            configs
        )
        
        # ==================== CONDIÇÕES PADRÃO ====================
        # (Condições do D&D 5e serão gerenciadas pelo módulo de regras)
        
        # ==================== MONSTROS DO UNDERDARK ====================
        monstros = [
            {
                'nome': 'Quaggoth',
                'tipo': 'humanóide',
                'tamanho': 'Médio',
                'alinhamento': 'Caótico e Neutro',
                'nd': 2,
                'xp': 450,
                'ca': 13,
                'ca_tipo': 'armadura natural',
                'hp_medio': 45,
                'hp_formula': '6d8+18',
                'atributos': json_dumps({
                    'forca': 17, 'destreza': 12, 'constituicao': 16,
                    'inteligencia': 6, 'sabedoria': 12, 'carisma': 7
                }),
                'velocidade': json_dumps({'normal': 30, 'escalada': 30}),
                'pericias': json_dumps({'atletismo': 5}),
                'resistencias': json_dumps(['dano de veneno']),
                'sentidos': json_dumps({'visão no escuro': 120}),
                'idiomas': json_dumps(['Subcomum']),
                'habilidades': json_dumps([
                    {
                        'nome': 'Frenesi Ferido',
                        'descricao': 'Quando seu HP cai para 10 ou menos, ganha vantagem em ataques corpo a corpo.'
                    }
                ]),
                'acoes': json_dumps([
                    {
                        'nome': 'Garras',
                        'descricao': 'Ataque corpo a corpo com arma: +5 para acertar, alcance 1,5m, um alvo.',
                        'ataque': '+5',
                        'dano': '1d6+3',
                        'tipo_dano': 'cortante'
                    }
                ])
            },
            {
                'nome': 'Drow Elite Warrior',
                'tipo': 'humanóide (elfo)',
                'tamanho': 'Médio',
                'alinhamento': 'Neutro e Mau',
                'nd': 5,
                'xp': 1800,
                'ca': 18,
                'ca_tipo': 'brunea + escudo',
                'hp_medio': 71,
                'hp_formula': '11d8+22',
                'atributos': json_dumps({
                    'forca': 13, 'destreza': 18, 'constituicao': 14,
                    'inteligencia': 11, 'sabedoria': 13, 'carisma': 12
                }),
                'velocidade': json_dumps({'normal': 30}),
                'salvaguardas': json_dumps({'destreza': 7, 'constituicao': 5, 'sabedoria': 4}),
                'pericias': json_dumps({'percepção': 4, 'furtividade': 7}),
                'sentidos': json_dumps({'visão no escuro': 120}),
                'idiomas': json_dumps(['Élfico', 'Subcomum']),
                'habilidades': json_dumps([
                    {
                        'nome': 'Ancestralidade Feérica',
                        'descricao': 'Vantagem em salvaguardas contra ser enfeitiçado, e magia não pode fazê-lo dormir.'
                    },
                    {
                        'nome': 'Sensibilidade à Luz Solar',
                        'descricao': 'Desvantagem em ataques e testes de percepção que dependam de visão enquanto em luz solar direta.'
                    }
                ]),
                'acoes': json_dumps([
                    {
                        'nome': 'Ataque Múltiplo',
                        'descricao': 'O drow faz dois ataques com espada curta.'
                    },
                    {
                        'nome': 'Espada Curta',
                        'descricao': 'Ataque corpo a corpo: +7 para acertar, alcance 1,5m.',
                        'ataque': '+7',
                        'dano': '1d6+4',
                        'tipo_dano': 'perfurante',
                        'extra': 'mais 3d6 de veneno'
                    },
                    {
                        'nome': 'Besta de Mão',
                        'descricao': 'Ataque à distância: +7 para acertar, alcance 9/36m.',
                        'ataque': '+7',
                        'dano': '1d6+4',
                        'tipo_dano': 'perfurante',
                        'extra': 'mais veneno drow'
                    }
                ])
            },
            {
                'nome': 'Hook Horror',
                'tipo': 'monstruosidade',
                'tamanho': 'Grande',
                'alinhamento': 'Neutro',
                'nd': 3,
                'xp': 700,
                'ca': 15,
                'ca_tipo': 'armadura natural',
                'hp_medio': 75,
                'hp_formula': '10d10+20',
                'atributos': json_dumps({
                    'forca': 18, 'destreza': 10, 'constituicao': 15,
                    'inteligencia': 6, 'sabedoria': 12, 'carisma': 7
                }),
                'velocidade': json_dumps({'normal': 30, 'escalada': 30}),
                'pericias': json_dumps({'percepção': 3}),
                'sentidos': json_dumps({'percepção às cegas': 60, 'visão no escuro': 10}),
                'idiomas': json_dumps(['Hook Horror']),
                'habilidades': json_dumps([
                    {
                        'nome': 'Ecolocalização',
                        'descricao': 'O hook horror não pode usar sua percepção às cegas enquanto surdo.'
                    },
                    {
                        'nome': 'Audição Aguçada',
                        'descricao': 'Vantagem em testes de Sabedoria (Percepção) que dependam de audição.'
                    }
                ]),
                'acoes': json_dumps([
                    {
                        'nome': 'Ataque Múltiplo',
                        'descricao': 'O hook horror faz dois ataques de gancho.'
                    },
                    {
                        'nome': 'Gancho',
                        'descricao': 'Ataque corpo a corpo: +6 para acertar, alcance 3m.',
                        'ataque': '+6',
                        'dano': '2d6+4',
                        'tipo_dano': 'perfurante'
                    }
                ])
            },
            {
                'nome': 'Giant Spider',
                'tipo': 'besta',
                'tamanho': 'Grande',
                'alinhamento': 'Sem Tendência',
                'nd': 1,
                'xp': 200,
                'ca': 14,
                'ca_tipo': 'armadura natural',
                'hp_medio': 26,
                'hp_formula': '4d10+4',
                'atributos': json_dumps({
                    'forca': 14, 'destreza': 16, 'constituicao': 12,
                    'inteligencia': 2, 'sabedoria': 11, 'carisma': 4
                }),
                'velocidade': json_dumps({'normal': 30, 'escalada': 30}),
                'pericias': json_dumps({'furtividade': 7}),
                'sentidos': json_dumps({'percepção às cegas': 10, 'visão no escuro': 60}),
                'habilidades': json_dumps([
                    {
                        'nome': 'Andar nas Teias',
                        'descricao': 'A aranha ignora restrições de movimento causadas por teias.'
                    },
                    {
                        'nome': 'Sentir Teias',
                        'descricao': 'Enquanto em contato com uma teia, conhece a localização de outras criaturas na mesma teia.'
                    }
                ]),
                'acoes': json_dumps([
                    {
                        'nome': 'Mordida',
                        'descricao': 'Ataque corpo a corpo: +5 para acertar, alcance 1,5m.',
                        'ataque': '+5',
                        'dano': '1d8+3',
                        'tipo_dano': 'perfurante',
                        'extra': 'O alvo deve fazer salvaguarda CON CD 11 ou sofrer 2d8 de dano de veneno (metade se passar)'
                    },
                    {
                        'nome': 'Teia (Recarrega 5-6)',
                        'descricao': 'Ataque à distância: +5 para acertar, alcance 9/18m. Alvo está contido. Pode se libertar com teste FOR CD 12.',
                        'ataque': '+5'
                    }
                ])
            }
        ]
        
        for monstro in monstros:
            conn.execute("""
                INSERT INTO monstros (nome, tipo, tamanho, alinhamento, nd, xp, ca, ca_tipo, 
                                      hp_medio, hp_formula, atributos, velocidade, salvaguardas,
                                      pericias, resistencias, sentidos, idiomas, habilidades, acoes)
                VALUES (:nome, :tipo, :tamanho, :alinhamento, :nd, :xp, :ca, :ca_tipo,
                        :hp_medio, :hp_formula, :atributos, :velocidade, :salvaguardas,
                        :pericias, :resistencias, :sentidos, :idiomas, :habilidades, :acoes)
            """, {
                'nome': monstro.get('nome'),
                'tipo': monstro.get('tipo'),
                'tamanho': monstro.get('tamanho'),
                'alinhamento': monstro.get('alinhamento'),
                'nd': monstro.get('nd'),
                'xp': monstro.get('xp'),
                'ca': monstro.get('ca'),
                'ca_tipo': monstro.get('ca_tipo'),
                'hp_medio': monstro.get('hp_medio'),
                'hp_formula': monstro.get('hp_formula'),
                'atributos': monstro.get('atributos', '{}'),
                'velocidade': monstro.get('velocidade', '{}'),
                'salvaguardas': monstro.get('salvaguardas', '{}'),
                'pericias': monstro.get('pericias', '{}'),
                'resistencias': monstro.get('resistencias', '[]'),
                'sentidos': monstro.get('sentidos', '{}'),
                'idiomas': monstro.get('idiomas', '[]'),
                'habilidades': monstro.get('habilidades', '[]'),
                'acoes': monstro.get('acoes', '[]')
            })
        
        # ==================== NPCS IMPORTANTES ====================
        npcs = [
            {
                'nome': 'Ilvara Mizzrym',
                'raca': 'Drow',
                'classe': 'Sacerdotisa de Lolth',
                'descricao': 'Alta Sacerdotisa drow que comanda a prisão de Velkynvelve. Cruel e calculista.',
                'localizacao': 'Velkynvelve',
                'hp_maximo': 71,
                'hp_atual': 71,
                'ca': 16,
                'alinhamento': 'hostil',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'Principal antagonista inicial. Perseguirá os prisioneiros fugitivos.'
            },
            {
                'nome': 'Buppido',
                'raca': 'Derro',
                'classe': 'Nenhuma',
                'descricao': 'Um derro que foi capturado pelos drow. Parece ser amigável demais...',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 13,
                'hp_atual': 13,
                'ca': 13,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'SEGREDO: É um serial killer que acredita ser um avatar do deus derro. Matará secretamente outros NPCs.'
            },
            {
                'nome': 'Jimjar',
                'raca': 'Deep Gnome (Svirfneblin)',
                'classe': 'Ladino',
                'descricao': 'Um gnomo das profundezas viciado em apostas. Aposta em qualquer coisa.',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 16,
                'hp_atual': 16,
                'ca': 15,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'Sempre propõe apostas. Útil como guia no Underdark.'
            },
            {
                'nome': 'Sarith Kzekarit',
                'raca': 'Drow',
                'classe': 'Guerreiro',
                'descricao': 'Um guerreiro drow preso por assassinar um oficial. Parece doente e perturbado.',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 39,
                'hp_atual': 39,
                'ca': 18,
                'alinhamento': 'indiferente',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'SEGREDO: Está infectado por esporos de Zuggtmoy e eventualmente se transformará.'
            },
            {
                'nome': 'Shuushar, o Pacífico',
                'raca': 'Kuo-toa',
                'classe': 'Nenhuma',
                'descricao': 'Um kuo-toa pacifista incomum que prega a não-violência.',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 18,
                'hp_atual': 18,
                'ca': 11,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'Genuinamente pacífico. Útil para guiar até Sloobludop.'
            },
            {
                'nome': 'Príncipe Derendil',
                'raca': 'Quaggoth',
                'classe': 'Nenhuma',
                'descricao': 'Um quaggoth que afirma ser um príncipe élfico transformado por magia.',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 45,
                'hp_atual': 45,
                'ca': 13,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'Acredita genuinamente ser um príncipe élfico. Pode entrar em frenesi quaggoth.'
            },
            {
                'nome': 'Stool',
                'raca': 'Myconid Sprout',
                'classe': 'Nenhuma',
                'descricao': 'Um pequeno myconid assustado que foi separado de seu círculo.',
                'localizacao': 'Velkynvelve (prisioneiro)',
                'hp_maximo': 7,
                'hp_atual': 7,
                'ca': 12,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'Pode criar link telepático via esporos. Quer voltar para Neverlight Grove.'
            },
            {
                'nome': 'Topsy e Turvy',
                'raca': 'Deep Gnome',
                'classe': 'Nenhuma',
                'descricao': 'Gêmeos svirfneblin que parecem nervosos e secretivos.',
                'localizacao': 'Velkynvelve (prisioneiros)',
                'hp_maximo': 16,
                'hp_atual': 16,
                'ca': 15,
                'alinhamento': 'amigável',
                'conhecido': 1,
                'vivo': 1,
                'notas': 'SEGREDO: São lobisomens (wererat). Mantêm isso escondido.'
            }
        ]
        
        for npc in npcs:
            conn.execute("""
                INSERT INTO npcs (nome, raca, classe, descricao, localizacao, hp_maximo, hp_atual, 
                                  ca, alinhamento, conhecido, vivo, notas)
                VALUES (:nome, :raca, :classe, :descricao, :localizacao, :hp_maximo, :hp_atual,
                        :ca, :alinhamento, :conhecido, :vivo, :notas)
            """, npc)
        
        print("[DB] Dados iniciais carregados com sucesso!")


def inicializar_banco():
    """Inicializa o banco de dados completo"""
    init_database()
    popular_dados_iniciais()
    print("[DB] Banco de dados pronto!")
