"""
Dados de Regras D&D 5e - Livro do Jogador
População inicial do banco de dados
"""

from .database import get_connection, json_dumps


def popular_regras_dnd():
    """Popula o banco com todas as regras do D&D 5e"""
    
    with get_connection() as conn:
        # Verifica se já tem dados
        cursor = conn.execute("SELECT COUNT(*) as total FROM racas")
        if cursor.fetchone()['total'] > 0:
            print("[DB] Regras D&D já carregadas")
            return
        
        print("[DB] Carregando regras D&D 5e...")
        
        # ==================== PERÍCIAS ====================
        pericias = [
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
        
        conn.executemany(
            "INSERT INTO pericias (nome, nome_display, atributo_base, descricao) VALUES (?, ?, ?, ?)",
            pericias
        )
        
        # ==================== IDIOMAS ====================
        idiomas = [
            ('Comum', 'comum', 'Humanos, maioria das raças civilizadas'),
            ('Anão', 'comum', 'Anões'),
            ('Élfico', 'comum', 'Elfos'),
            ('Gigante', 'comum', 'Ogros, gigantes'),
            ('Gnômico', 'comum', 'Gnomos'),
            ('Goblin', 'comum', 'Goblins, hobgoblins, bugbears'),
            ('Halfling', 'comum', 'Halflings'),
            ('Orc', 'comum', 'Orcs'),
            ('Abissal', 'exotico', 'Demônios'),
            ('Celestial', 'exotico', 'Celestiais'),
            ('Dracônico', 'exotico', 'Dragões, draconatos'),
            ('Dialeto Subterrâneo', 'exotico', 'Comerciantes do Subterrâneo'),
            ('Infernal', 'exotico', 'Diabos'),
            ('Primordial', 'exotico', 'Elementais'),
            ('Silvestre', 'exotico', 'Criaturas feéricas'),
            ('Subcomum', 'exotico', 'Criaturas do Subterrâneo'),
            ('Druídico', 'secreto', 'Druidas (secreto)'),
            ('Cant dos Ladrões', 'secreto', 'Ladinos (secreto)'),
        ]
        
        conn.executemany(
            "INSERT INTO idiomas (nome, tipo, falantes) VALUES (?, ?, ?)",
            idiomas
        )
        
        # ==================== RAÇAS ====================
        racas_data = [
            # === ANÃO ===
            {
                'nome': 'Anão',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'constituicao': 2}),
                'velocidade': 7,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Anão']),
                'proficiencias_armas': json_dumps(['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resiliência Anã: Vantagem em salvaguardas contra veneno',
                    'Especialização em Pedra: Dobra proficiência em História relacionada a pedra'
                ]),
                'resistencias': json_dumps(['veneno']),
            },
            {
                'nome': 'Anão da Colina',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'constituicao': 2, 'sabedoria': 1}),
                'velocidade': 7,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Anão']),
                'proficiencias_armas': json_dumps(['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resiliência Anã: Vantagem em salvaguardas contra veneno',
                    'Especialização em Pedra: Dobra proficiência em História relacionada a pedra',
                    'Tenacidade Anã: HP máximo aumenta em 1 por nível'
                ]),
                'resistencias': json_dumps(['veneno']),
                'subraca_de': 1,  # Anão
            },
            {
                'nome': 'Anão da Montanha',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'constituicao': 2, 'forca': 2}),
                'velocidade': 7,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Anão']),
                'proficiencias_armas': json_dumps(['machado de batalha', 'machadinha', 'martelo leve', 'martelo de guerra']),
                'proficiencias_armaduras': json_dumps(['armaduras leves', 'armaduras médias']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resiliência Anã: Vantagem em salvaguardas contra veneno',
                    'Especialização em Pedra: Dobra proficiência em História relacionada a pedra',
                    'Treinamento Anão com Armaduras'
                ]),
                'resistencias': json_dumps(['veneno']),
                'subraca_de': 1,  # Anão
            },
            
            # === ELFO ===
            {
                'nome': 'Elfo',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'pericias_bonus': json_dumps(['percepcao']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
                    'Transe: 4 horas de meditação = 8 horas de sono'
                ]),
                'imunidades': json_dumps(['sono mágico']),
            },
            {
                'nome': 'Alto Elfo',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2, 'inteligencia': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'idiomas_escolha': 1,
                'proficiencias_armas': json_dumps(['espada longa', 'espada curta', 'arco longo', 'arco curto']),
                'pericias_bonus': json_dumps(['percepcao']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
                    'Transe: 4 horas de meditação = 8 horas de sono',
                    'Truque: Conhece 1 truque de mago (Inteligência)'
                ]),
                'imunidades': json_dumps(['sono mágico']),
                'subraca_de': 4,  # Elfo
            },
            {
                'nome': 'Elfo da Floresta',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2, 'sabedoria': 1}),
                'velocidade': 10,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'proficiencias_armas': json_dumps(['espada longa', 'espada curta', 'arco longo', 'arco curto']),
                'pericias_bonus': json_dumps(['percepcao']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
                    'Transe: 4 horas de meditação = 8 horas de sono',
                    'Máscara da Natureza: Pode se esconder com folhagem, chuva, neve, neblina',
                    'Pés Ligeiros: Velocidade base 10m'
                ]),
                'imunidades': json_dumps(['sono mágico']),
                'subraca_de': 4,  # Elfo
            },
            {
                'nome': 'Drow',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2, 'carisma': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'proficiencias_armas': json_dumps(['rapieira', 'espada curta', 'besta de mão']),
                'pericias_bonus': json_dumps(['percepcao']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro Superior (36m)',
                    'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
                    'Transe: 4 horas de meditação = 8 horas de sono',
                    'Sensibilidade à Luz Solar: Desvantagem em ataques e Percepção sob luz solar',
                    'Magia Drow: Conhece Luzes Dançantes; nível 3: Fogo das Fadas; nível 5: Escuridão'
                ]),
                'imunidades': json_dumps(['sono mágico']),
                'subraca_de': 4,  # Elfo
            },
            
            # === HALFLING ===
            {
                'nome': 'Halfling',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Halfling']),
                'caracteristicas': json_dumps([
                    'Sortudo: Ao rolar 1 natural, pode rolar novamente',
                    'Corajoso: Vantagem contra ser amedrontado',
                    'Agilidade Halfling: Pode mover através de criaturas maiores'
                ]),
            },
            {
                'nome': 'Halfling Pés Leves',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2, 'carisma': 1}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Halfling']),
                'caracteristicas': json_dumps([
                    'Sortudo: Ao rolar 1 natural, pode rolar novamente',
                    'Corajoso: Vantagem contra ser amedrontado',
                    'Agilidade Halfling: Pode mover através de criaturas maiores',
                    'Furtividade Natural: Pode se esconder atrás de criaturas maiores'
                ]),
                'subraca_de': 8,  # Halfling
            },
            {
                'nome': 'Halfling Robusto',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'destreza': 2, 'constituicao': 1}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Halfling']),
                'caracteristicas': json_dumps([
                    'Sortudo: Ao rolar 1 natural, pode rolar novamente',
                    'Corajoso: Vantagem contra ser amedrontado',
                    'Agilidade Halfling: Pode mover através de criaturas maiores',
                    'Resiliência Robusta: Vantagem contra veneno, resistência a dano de veneno'
                ]),
                'resistencias': json_dumps(['veneno']),
                'subraca_de': 8,  # Halfling
            },
            
            # === HUMANO ===
            {
                'nome': 'Humano',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'forca': 1, 'destreza': 1, 'constituicao': 1, 'inteligencia': 1, 'sabedoria': 1, 'carisma': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Versátil: +1 em todos os atributos',
                    'Idioma Extra: Conhece um idioma adicional à escolha'
                ]),
            },
            {
                'nome': 'Humano (Variante)',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 2,  # +1 em dois atributos à escolha
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'pericias_escolha': 1,
                'caracteristicas': json_dumps([
                    '+1 em dois atributos diferentes à escolha',
                    'Uma perícia à escolha',
                    'Um talento à escolha'
                ]),
            },
            
            # === DRACONATO ===
            {
                'nome': 'Draconato',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'forca': 2, 'carisma': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Dracônico']),
                'caracteristicas': json_dumps([
                    'Ancestral Dracônico: Escolha um tipo de dragão ancestral',
                    'Sopro: Usa ação para soprar energia (dano = 2d6, aumenta com nível)',
                    'Resistência a Dano: Resistência ao tipo de dano do ancestral'
                ]),
            },
            
            # === GNOMO ===
            {
                'nome': 'Gnomo',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'inteligencia': 2}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Gnômico']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia'
                ]),
            },
            {
                'nome': 'Gnomo da Floresta',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'inteligencia': 2, 'destreza': 1}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Gnômico']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia',
                    'Ilusionista Nato: Conhece o truque Ilusão Menor',
                    'Falar com Bestas Pequenas: Pode se comunicar com animais pequenos'
                ]),
                'subraca_de': 15,  # Gnomo
            },
            {
                'nome': 'Gnomo das Rochas',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'inteligencia': 2, 'constituicao': 1}),
                'velocidade': 7,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Gnômico']),
                'proficiencias_ferramentas': json_dumps(['ferramentas de artesão']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Esperteza Gnômica: Vantagem em salvaguardas de INT, SAB, CAR contra magia',
                    'Conhecimento de Artífice: Dobra proficiência em História sobre itens mágicos/tecnológicos',
                    'Engenhoqueiro: Pode criar pequenos dispositivos mecânicos'
                ]),
                'subraca_de': 15,  # Gnomo
            },
            
            # === MEIO-ELFO ===
            {
                'nome': 'Meio-Elfo',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'carisma': 2}),
                'atributos_escolha': 2,  # +1 em dois atributos à escolha (exceto CAR)
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'idiomas_escolha': 1,
                'pericias_escolha': 2,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra ser enfeitiçado, imune a sono mágico',
                    'Versatilidade em Perícia: Proficiência em duas perícias à escolha'
                ]),
                'imunidades': json_dumps(['sono mágico']),
            },
            
            # === MEIO-ORC ===
            {
                'nome': 'Meio-Orc',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'forca': 2, 'constituicao': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Orc']),
                'pericias_bonus': json_dumps(['intimidacao']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resistência Implacável: 1x/descanso longo, ao cair para 0 HP, cai para 1 HP',
                    'Ataques Selvagens: Crítico com arma corpo a corpo rola 1 dado de dano extra'
                ]),
            },
            
            # === TIEFLING ===
            {
                'nome': 'Tiefling',
                'categoria': 'Livro do Jogador',
                'bonus_atributos': json_dumps({'carisma': 2, 'inteligencia': 1}),
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Infernal']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resistência Infernal: Resistência a dano de fogo',
                    'Legado Infernal: Conhece Taumaturgia; nível 3: Repreensão Infernal; nível 5: Escuridão'
                ]),
                'resistencias': json_dumps(['fogo']),
            },
            
            # ==================== MONSTERS OF THE MULTIVERSE ====================
            # Raças com sistema de bônus flexível (+2/+1 ou +1/+1/+1 à escolha)
            
            # Aarakocra
            {
                'nome': 'Aarakocra',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,  # Sistema flexível
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Voo (velocidade igual à terrestre)',
                    'Garras: Ataque desarmado 1d6 + FOR cortante',
                    'Rajada de Vento: 1x/descanso longo'
                ]),
            },
            
            # Aasimar
            {
                'nome': 'Aasimar',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum', 'Celestial']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resistência Celestial: Resistência a necrótico e radiante',
                    'Mãos Curativas: Cura PV = bônus de proficiência (1x/descanso longo)',
                    'Portador da Luz: Truque Luz',
                    'Revelação Celestial (nível 3): Transformação 1x/descanso longo'
                ]),
                'resistencias': json_dumps(['necrótico', 'radiante']),
            },
            
            # Bugbear
            {
                'nome': 'Bugbear',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'pericias_bonus': json_dumps(['furtividade']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Constituição Feérica: Vantagem contra encantamento, imune a sono mágico',
                    'Membros Longos: +1,5m de alcance em ataques corpo a corpo no seu turno',
                    'Físico Poderoso: Conta como Grande para capacidade de carga',
                    'Ataque Surpresa: +2d6 de dano em criaturas surpresas'
                ]),
            },
            
            # Centauro
            {
                'nome': 'Centauro',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 12,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Investida: Bônus de dano após mover 9m em linha reta',
                    'Forma Equina: Velocidade 12m, conta como montaria',
                    'Cascos: Ataque desarmado 1d6 + FOR contundente'
                ]),
            },
            
            # Changeling
            {
                'nome': 'Changeling',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 2,
                'caracteristicas': json_dumps([
                    'Instintos do Changeling: Proficiência em 2 perícias à escolha',
                    'Metamorfose: Pode alterar aparência como ação'
                ]),
                'pericias_escolha': 2,
            },
            
            # Deep Gnome (Svirfneblin)
            {
                'nome': 'Gnomo das Profundezas',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Gnômico', 'Subcomum']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (36m)',
                    'Presente da Svrifrenblin: Disfarçar-se, Passos sem Pegadas ou Nondetection',
                    'Camuflagem Gnômica: Vantagem em Furtividade em terreno rochoso',
                    'Esperteza Gnômica: Vantagem contra magia (INT, SAB, CAR)'
                ]),
            },
            
            # Duergar
            {
                'nome': 'Duergar',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Anão']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (36m)',
                    'Resiliência Duergar: Vantagem contra ilusões, encantamento e paralisia',
                    'Magia Duergar: Ampliar/Reduzir (nível 3), Invisibilidade (nível 5)',
                    'Constituição Anã: Resistência a veneno'
                ]),
                'resistencias': json_dumps(['veneno']),
            },
            
            # Eladrin
            {
                'nome': 'Eladrin',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono mágico',
                    'Passo Feérico: Teleporte bônus 9m (bônus de prof/descanso longo)',
                    'Transe: 4h de meditação = 8h de sono'
                ]),
            },
            
            # Fairy
            {
                'nome': 'Fada',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Voo (velocidade igual à terrestre)',
                    'Magia Feérica: Druídico, Fogo das Fadas (nv3), Ampliar/Reduzir (nv5)',
                    'Passagem Feérica: Pode atravessar espaços de criaturas maiores'
                ]),
            },
            
            # Firbolg
            {
                'nome': 'Firbolg',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Magia Firbolg: Detectar Magia, Disfarçar-se',
                    'Passo Oculto: Bônus invisibilidade até início do próximo turno',
                    'Físico Poderoso: Conta como Grande para carga',
                    'Fala das Bestas e Folhas: Comunicação limitada com plantas e animais'
                ]),
            },
            
            # Genasi (4 tipos)
            {
                'nome': 'Genasi do Ar',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 10,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Não precisa respirar',
                    'Resistência a raios',
                    'Respiração Interminável: Pode prender respiração indefinidamente',
                    'Misturar-se ao Vento: Levitação (nv3), Passo Nebuloso (nv5)'
                ]),
                'resistencias': json_dumps(['elétrico']),
            },
            {
                'nome': 'Genasi da Terra',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Caminhada na Terra: Pode mover por terreno difícil não-mágico sem custo extra',
                    'Mesclar-se à Pedra: Passar sem Deixar Rastro, Pico de Pedra (nv5)'
                ]),
            },
            {
                'nome': 'Genasi do Fogo',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resistência a fogo',
                    'Alcançar as Chamas: Produzir Chamas, Mãos Flamejantes (nv3), Lâmina Flamejante (nv5)'
                ]),
                'resistencias': json_dumps(['fogo']),
            },
            {
                'nome': 'Genasi da Água',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Anfíbio: Pode respirar ar e água',
                    'Resistência a ácido',
                    'Natação: Velocidade de natação igual à terrestre',
                    'Chamado das Ondas: Moldar Água, Criar/Destruir Água (nv3), Caminhar na Água (nv5)'
                ]),
                'resistencias': json_dumps(['ácido']),
            },
            
            # Githyanki
            {
                'nome': 'Githyanki',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Gith']),
                'caracteristicas': json_dumps([
                    'Resistência Astral: Vantagem contra encantamento',
                    'Prodigio Githyanki: Proficiências à escolha',
                    'Psiônicos Githyanki: Mão Mágica, Salto (nv3), Passo Nebuloso (nv5)'
                ]),
            },
            
            # Githzerai
            {
                'nome': 'Githzerai',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Gith']),
                'caracteristicas': json_dumps([
                    'Resistência Mental: Vantagem contra encantamento',
                    'Disciplina Githzerai: Pode usar reação para cancelar Amedrontado/Enfeitiçado',
                    'Psiônicos Githzerai: Mão Mágica, Escudo (nv3), Detectar Pensamentos (nv5)'
                ]),
            },
            
            # Goblin
            {
                'nome': 'Goblin',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Goblin']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Fúria dos Pequenos: Dano extra = bônus de proficiência (prof/descanso longo)',
                    'Fuga Ágil: Desengajar ou Esconder como ação bônus'
                ]),
            },
            
            # Goliath
            {
                'nome': 'Goliath',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'pericias_bonus': json_dumps(['atletismo']),
                'caracteristicas': json_dumps([
                    'Atleta Natural: Proficiência em Atletismo',
                    'Constituição de Gigante da Pedra: Resistência a frio',
                    'Físico Poderoso: Conta como Grande para carga',
                    'Resistência de Montanha: Reduz dano = 1d12 + CON (prof/descanso longo)'
                ]),
                'resistencias': json_dumps(['gélido']),
            },
            
            # Harengon
            {
                'nome': 'Harengon',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'pericias_bonus': json_dumps(['percepcao']),
                'caracteristicas': json_dumps([
                    'Pulo de Coelho: Salto em distância como ação bônus = prof x 1,5m',
                    'Intuição de Lebre: +bônus de prof em iniciativa',
                    'Sorte de Lebre: Reação para adicionar d4 em salvaguarda'
                ]),
            },
            
            # Hobgoblin
            {
                'nome': 'Hobgoblin',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Goblin']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Constituição Feérica: Vantagem contra encantamento, imune a sono mágico',
                    'Presente da Legião Fantasma: Truque de ilusão/encantamento + Ajuda (prof/descanso longo)',
                    'Fortuna dos Muitos: +d6 em ataque/salvaguarda/teste se aliado visível em 9m'
                ]),
            },
            
            # Kenku
            {
                'nome': 'Kenku',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Recordação de Especialista: Proficiência em 2 perícias à escolha',
                    'Imitação: Vantagem em testes para imitar sons',
                    'Recital de Kenku: Pode usar Prestidigitação, Falar com Animais ou similares'
                ]),
                'pericias_escolha': 2,
            },
            
            # Kobold
            {
                'nome': 'Kobold',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Pequeno',
                'idiomas': json_dumps(['Comum', 'Dracônico']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Rugido Dracônico: Aliados em 3m têm vantagem (prof/descanso longo)',
                    'Legado Dracônico: Escolha uma característica dracônica',
                    'Sorcaria Kobold: 1 truque de feiticeiro'
                ]),
            },
            
            # Lizardfolk
            {
                'nome': 'Povo-Lagarto',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Mordida: Ataque desarmado 1d6 + FOR perfurante',
                    'Prender a Respiração: Até 15 minutos',
                    'Mandíbulas Famintas: HP temp = prof (prof/descanso longo)',
                    'Armadura Natural: CA = 13 + DES sem armadura',
                    'Artesanato Natural: Pode criar escudo/arma de restos'
                ]),
            },
            
            # Minotaur
            {
                'nome': 'Minotauro',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Chifres: Ataque desarmado 1d6 + FOR perfurante',
                    'Investida com Chifres: +2d6 após mover 6m em linha reta',
                    'Marrada: Empurra como ação bônus após acertar com chifres',
                    'Memória Labiríntica: Vantagem para lembrar caminhos'
                ]),
            },
            
            # Orc
            {
                'nome': 'Orc',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Orc']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Adrenalina: Ação bônus para mover velocidade em direção a inimigo',
                    'Resistência Implacável: 1x/descanso longo, ao cair para 0 HP, cai para 1 HP',
                    'Físico Poderoso: Conta como Grande para carga'
                ]),
            },
            
            # Satyr
            {
                'nome': 'Sátiro',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 10,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Tipo Criatura: Feérico (não humanoide)',
                    'Resistência Mágica: Vantagem em salvaguardas contra magia',
                    'Salto de Miriti: Salto em distância extra',
                    'Chifrada: Ataque desarmado 1d6 + FOR contundente',
                    'Artista Revelador: Proficiência em Performance + 1 instrumento'
                ]),
            },
            
            # Sea Elf
            {
                'nome': 'Elfo do Mar',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono',
                    'Filho do Mar: Pode respirar água, natação = velocidade',
                    'Amigo do Mar: Comunicação simples com bestas aquáticas',
                    'Transe: 4h = 8h sono'
                ]),
            },
            
            # Shadar-kai
            {
                'nome': 'Shadar-kai',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum', 'Élfico']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Ancestralidade Feérica: Vantagem contra encantamento, imune a sono',
                    'Resistência Necrótica',
                    'Bênção da Rainha Corvo: Teleporte 9m + resistência (prof/descanso longo)',
                    'Transe: 4h = 8h sono'
                ]),
                'resistencias': json_dumps(['necrótico']),
            },
            
            # Shifter
            {
                'nome': 'Shifter',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Instintos Bestiais: Proficiência em Acrobacia, Atletismo, Intuição ou Sobrevivência',
                    'Mudar: HP temp + característica bestial (prof/descanso longo)'
                ]),
                'pericias_opcoes': json_dumps(['acrobacia', 'atletismo', 'intuicao', 'sobrevivencia']),
            },
            
            # Tabaxi
            {
                'nome': 'Tabaxi',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Garras de Gato: Ataque desarmado 1d6 + FOR cortante, escalada = velocidade',
                    'Talento Felino: Proficiência em Percepção e Furtividade',
                    'Agilidade Felina: Dobra velocidade até fim do turno (recarga)'
                ]),
                'pericias_bonus': json_dumps(['percepcao', 'furtividade']),
            },
            
            # Tortle
            {
                'nome': 'Tortle',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Garras: Ataque desarmado 1d6 + FOR cortante',
                    'Prender Respiração: 1 hora',
                    'Armadura Natural: CA 17 (não pode usar armadura)',
                    'Defesa do Casco: +4 CA quando entra no casco (ação)'
                ]),
            },
            
            # Triton
            {
                'nome': 'Tritão',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Anfíbio: Respira ar e água',
                    'Resistência a frio',
                    'Emissário do Mar: Comunicação com criaturas aquáticas',
                    'Guardião das Profundezas: Resistência a dano de profundidade',
                    'Controle de Ar e Água: Névoa Obscurecente, Rajada de Vento (nv3), Caminhar na Água (nv5)'
                ]),
                'resistencias': json_dumps(['gélido']),
            },
            
            # Yuan-ti
            {
                'nome': 'Yuan-ti',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'caracteristicas': json_dumps([
                    'Visão no Escuro (18m)',
                    'Resistência Mágica: Vantagem em salvaguardas contra magia',
                    'Resistência a veneno, imunidade a condição envenenado',
                    'Magia Serpentina: Veneno por Contato, Sugestão (nv3)'
                ]),
                'resistencias': json_dumps(['veneno']),
            },
            
            # Owlin
            {
                'nome': 'Owlin',
                'categoria': 'Monsters of the Multiverse',
                'bonus_atributos': json_dumps({}),
                'atributos_escolha': 3,
                'velocidade': 9,
                'tamanho': 'Médio ou Pequeno',
                'idiomas': json_dumps(['Comum']),
                'idiomas_escolha': 1,
                'pericias_bonus': json_dumps(['furtividade']),
                'caracteristicas': json_dumps([
                    'Visão no Escuro (36m)',
                    'Voo (velocidade igual à terrestre, não pode usar armadura média/pesada)',
                    'Voo Silencioso: Proficiência em Furtividade'
                ]),
            },
        ]
        
        for raca in racas_data:
            # Preencher campos ausentes com defaults
            raca.setdefault('proficiencias_armas', json_dumps([]))
            raca.setdefault('proficiencias_armaduras', json_dumps([]))
            raca.setdefault('proficiencias_ferramentas', json_dumps([]))
            raca.setdefault('pericias_bonus', json_dumps([]))
            raca.setdefault('resistencias', json_dumps([]))
            raca.setdefault('imunidades', json_dumps([]))
            raca.setdefault('atributos_escolha', 0)
            raca.setdefault('pericias_escolha', 0)
            raca.setdefault('idiomas_escolha', 0)
            raca.setdefault('pericias_opcoes', json_dumps([]))
            raca.setdefault('subraca_de', None)
            
            conn.execute("""
                INSERT INTO racas (
                    nome, categoria, bonus_atributos, velocidade, tamanho,
                    idiomas, proficiencias_armas, proficiencias_armaduras,
                    proficiencias_ferramentas, pericias_bonus, caracteristicas,
                    resistencias, imunidades, atributos_escolha, pericias_escolha,
                    idiomas_escolha, pericias_opcoes, subraca_de
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                raca['nome'], raca['categoria'], raca['bonus_atributos'],
                raca['velocidade'], raca['tamanho'], raca['idiomas'],
                raca['proficiencias_armas'], raca['proficiencias_armaduras'],
                raca['proficiencias_ferramentas'], raca['pericias_bonus'],
                raca['caracteristicas'], raca['resistencias'], raca['imunidades'],
                raca['atributos_escolha'], raca['pericias_escolha'],
                raca['idiomas_escolha'], raca['pericias_opcoes'], raca['subraca_de']
            ))
        
        # ==================== CLASSES ====================
        classes_data = [
            {
                'nome': 'Bárbaro',
                'dado_vida': 12,
                'hp_primeiro_nivel': '12 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['forca', 'constituicao']),
                'armaduras': json_dumps(['armaduras leves', 'armaduras médias', 'escudos']),
                'armas': json_dumps(['armas simples', 'armas marciais']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['adestrar_animais', 'atletismo', 'intimidacao', 'natureza', 'percepcao', 'sobrevivencia']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Fúria', 'Defesa sem Armadura']),
            },
            {
                'nome': 'Bardo',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['destreza', 'carisma']),
                'armaduras': json_dumps(['armaduras leves']),
                'armas': json_dumps(['armas simples', 'bestas de mão', 'espadas longas', 'rapieiras', 'espadas curtas']),
                'ferramentas': json_dumps(['três instrumentos musicais à escolha']),
                'pericias_disponiveis': json_dumps(['todas']),  # Bardos podem escolher qualquer perícia
                'qtd_pericias': 3,
                'caracteristicas_nivel_1': json_dumps(['Conjuração', 'Inspiração de Bardo (d6)']),
                'conjurador': 1,
                'atributo_conjuracao': 'carisma',
                'truques_nivel_1': 2,
                'magias_conhecidas_nivel_1': 4,
            },
            {
                'nome': 'Bruxo',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['sabedoria', 'carisma']),
                'armaduras': json_dumps(['armaduras leves']),
                'armas': json_dumps(['armas simples']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['arcanismo', 'enganacao', 'historia', 'intimidacao', 'investigacao', 'natureza', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Patrono Transcendental', 'Magia de Pacto']),
                'conjurador': 1,
                'atributo_conjuracao': 'carisma',
                'truques_nivel_1': 2,
                'magias_conhecidas_nivel_1': 2,
            },
            {
                'nome': 'Clérigo',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['sabedoria', 'carisma']),
                'armaduras': json_dumps(['armaduras leves', 'armaduras médias', 'escudos']),
                'armas': json_dumps(['armas simples']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['historia', 'intuicao', 'medicina', 'persuasao', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Conjuração', 'Domínio Divino']),
                'conjurador': 1,
                'atributo_conjuracao': 'sabedoria',
                'truques_nivel_1': 3,
            },
            {
                'nome': 'Druida',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['inteligencia', 'sabedoria']),
                'armaduras': json_dumps(['armaduras leves (não-metálicas)', 'armaduras médias (não-metálicas)', 'escudos (não-metálicos)']),
                'armas': json_dumps(['clavas', 'adagas', 'dardos', 'azagaias', 'maças', 'bordões', 'cimitarras', 'foices', 'fundas', 'lanças']),
                'ferramentas': json_dumps(['kit de herbalismo']),
                'pericias_disponiveis': json_dumps(['arcanismo', 'adestrar_animais', 'intuicao', 'medicina', 'natureza', 'percepcao', 'religiao', 'sobrevivencia']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Druídico', 'Conjuração']),
                'conjurador': 1,
                'atributo_conjuracao': 'sabedoria',
                'truques_nivel_1': 2,
            },
            {
                'nome': 'Feiticeiro',
                'dado_vida': 6,
                'hp_primeiro_nivel': '6 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['constituicao', 'carisma']),
                'armaduras': json_dumps([]),
                'armas': json_dumps(['adagas', 'dardos', 'fundas', 'bordões', 'bestas leves']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['arcanismo', 'enganacao', 'intuicao', 'intimidacao', 'persuasao', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Conjuração', 'Origem de Feitiçaria']),
                'conjurador': 1,
                'atributo_conjuracao': 'carisma',
                'truques_nivel_1': 4,
                'magias_conhecidas_nivel_1': 2,
            },
            {
                'nome': 'Guerreiro',
                'dado_vida': 10,
                'hp_primeiro_nivel': '10 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['forca', 'constituicao']),
                'armaduras': json_dumps(['todas as armaduras', 'escudos']),
                'armas': json_dumps(['armas simples', 'armas marciais']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['acrobacia', 'adestrar_animais', 'atletismo', 'historia', 'intuicao', 'intimidacao', 'percepcao', 'sobrevivencia']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Estilo de Luta', 'Retomar o Fôlego']),
            },
            {
                'nome': 'Ladino',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['destreza', 'inteligencia']),
                'armaduras': json_dumps(['armaduras leves']),
                'armas': json_dumps(['armas simples', 'bestas de mão', 'espadas longas', 'rapieiras', 'espadas curtas']),
                'ferramentas': json_dumps(['ferramentas de ladrão']),
                'pericias_disponiveis': json_dumps(['acrobacia', 'atletismo', 'atuacao', 'enganacao', 'furtividade', 'intimidacao', 'intuicao', 'investigacao', 'percepcao', 'persuasao', 'prestidigitacao']),
                'qtd_pericias': 4,
                'caracteristicas_nivel_1': json_dumps(['Especialização', 'Ataque Furtivo (1d6)', 'Gíria dos Ladrões']),
            },
            {
                'nome': 'Mago',
                'dado_vida': 6,
                'hp_primeiro_nivel': '6 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['inteligencia', 'sabedoria']),
                'armaduras': json_dumps([]),
                'armas': json_dumps(['adagas', 'dardos', 'fundas', 'bordões', 'bestas leves']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['arcanismo', 'historia', 'intuicao', 'investigacao', 'medicina', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Conjuração', 'Recuperação Arcana']),
                'conjurador': 1,
                'atributo_conjuracao': 'inteligencia',
                'truques_nivel_1': 3,
            },
            {
                'nome': 'Monge',
                'dado_vida': 8,
                'hp_primeiro_nivel': '8 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['forca', 'destreza']),
                'armaduras': json_dumps([]),
                'armas': json_dumps(['armas simples', 'espadas curtas']),
                'ferramentas': json_dumps(['uma ferramenta de artesão ou instrumento musical']),
                'pericias_disponiveis': json_dumps(['acrobacia', 'atletismo', 'furtividade', 'historia', 'intuicao', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Defesa sem Armadura', 'Artes Marciais']),
            },
            {
                'nome': 'Paladino',
                'dado_vida': 10,
                'hp_primeiro_nivel': '10 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['sabedoria', 'carisma']),
                'armaduras': json_dumps(['todas as armaduras', 'escudos']),
                'armas': json_dumps(['armas simples', 'armas marciais']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['atletismo', 'intimidacao', 'intuicao', 'medicina', 'persuasao', 'religiao']),
                'qtd_pericias': 2,
                'caracteristicas_nivel_1': json_dumps(['Sentido Divino', 'Cura pelas Mãos']),
            },
            {
                'nome': 'Patrulheiro',
                'dado_vida': 10,
                'hp_primeiro_nivel': '10 + modificador de Constituição',
                'salvaguardas_proficientes': json_dumps(['forca', 'destreza']),
                'armaduras': json_dumps(['armaduras leves', 'armaduras médias', 'escudos']),
                'armas': json_dumps(['armas simples', 'armas marciais']),
                'ferramentas': json_dumps([]),
                'pericias_disponiveis': json_dumps(['adestrar_animais', 'atletismo', 'furtividade', 'intuicao', 'investigacao', 'natureza', 'percepcao', 'sobrevivencia']),
                'qtd_pericias': 3,
                'caracteristicas_nivel_1': json_dumps(['Inimigo Favorito', 'Explorador Natural']),
            },
        ]
        
        for classe in classes_data:
            # Preencher campos ausentes com defaults
            classe.setdefault('conjurador', 0)
            classe.setdefault('atributo_conjuracao', None)
            classe.setdefault('truques_nivel_1', 0)
            classe.setdefault('magias_conhecidas_nivel_1', 0)
            
            conn.execute("""
                INSERT INTO classes (
                    nome, dado_vida, hp_primeiro_nivel, salvaguardas_proficientes,
                    armaduras, armas, ferramentas, pericias_disponiveis, qtd_pericias,
                    caracteristicas_nivel_1, conjurador, atributo_conjuracao,
                    truques_nivel_1, magias_conhecidas_nivel_1
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                classe['nome'], classe['dado_vida'], classe['hp_primeiro_nivel'],
                classe['salvaguardas_proficientes'], classe['armaduras'], classe['armas'],
                classe['ferramentas'], classe['pericias_disponiveis'], classe['qtd_pericias'],
                classe['caracteristicas_nivel_1'], classe['conjurador'],
                classe['atributo_conjuracao'], classe['truques_nivel_1'],
                classe['magias_conhecidas_nivel_1']
            ))
        
        # ==================== ANTECEDENTES ====================
        antecedentes_data = [
            {
                'nome': 'Acólito',
                'pericias': json_dumps(['intuicao', 'religiao']),
                'idiomas_escolha': 2,
                'caracteristica_nome': 'Abrigo dos Fiéis',
                'caracteristica_descricao': 'Você e seus companheiros podem receber cura gratuita e cuidados em templos de sua fé.',
            },
            {
                'nome': 'Charlatão',
                'pericias': json_dumps(['enganacao', 'prestidigitacao']),
                'ferramentas': json_dumps(['kit de disfarce', 'kit de falsificação']),
                'caracteristica_nome': 'Identidade Falsa',
                'caracteristica_descricao': 'Você criou uma segunda identidade com documentação, contatos e disfarces.',
            },
            {
                'nome': 'Criminoso',
                'pericias': json_dumps(['enganacao', 'furtividade']),
                'ferramentas': json_dumps(['um tipo de jogo', 'ferramentas de ladrão']),
                'caracteristica_nome': 'Contato Criminal',
                'caracteristica_descricao': 'Você tem um contato confiável que atua como intermediário para a rede criminosa.',
            },
            {
                'nome': 'Artista',
                'pericias': json_dumps(['acrobacia', 'atuacao']),
                'ferramentas': json_dumps(['kit de disfarce', 'um instrumento musical']),
                'caracteristica_nome': 'Por Demanda Popular',
                'caracteristica_descricao': 'Sempre pode encontrar um lugar para se apresentar e receber hospedagem gratuita.',
            },
            {
                'nome': 'Herói do Povo',
                'pericias': json_dumps(['adestrar_animais', 'sobrevivencia']),
                'ferramentas': json_dumps(['um tipo de ferramenta de artesão', 'veículos terrestres']),
                'caracteristica_nome': 'Hospitalidade Rústica',
                'caracteristica_descricao': 'Você pode encontrar lugar para se esconder entre pessoas comuns.',
            },
            {
                'nome': 'Artesão de Guilda',
                'pericias': json_dumps(['intuicao', 'persuasao']),
                'ferramentas': json_dumps(['um tipo de ferramenta de artesão']),
                'idiomas_escolha': 1,
                'caracteristica_nome': 'Associação de Guilda',
                'caracteristica_descricao': 'Você é membro de uma guilda que oferece hospedagem, assistência legal e política.',
            },
            {
                'nome': 'Eremita',
                'pericias': json_dumps(['medicina', 'religiao']),
                'ferramentas': json_dumps(['kit de herbalismo']),
                'idiomas_escolha': 1,
                'caracteristica_nome': 'Descoberta',
                'caracteristica_descricao': 'Durante seu isolamento, você descobriu algo importante ou teve uma revelação.',
            },
            {
                'nome': 'Nobre',
                'pericias': json_dumps(['historia', 'persuasao']),
                'ferramentas': json_dumps(['um tipo de jogo']),
                'idiomas_escolha': 1,
                'caracteristica_nome': 'Posição de Privilégio',
                'caracteristica_descricao': 'Pessoas comuns tentam agradá-lo e evitam seu desprazer.',
            },
            {
                'nome': 'Forasteiro',
                'pericias': json_dumps(['atletismo', 'sobrevivencia']),
                'ferramentas': json_dumps(['um instrumento musical']),
                'idiomas_escolha': 1,
                'caracteristica_nome': 'Andarilho',
                'caracteristica_descricao': 'Você tem excelente memória para mapas e pode sempre encontrar comida e água.',
            },
            {
                'nome': 'Sábio',
                'pericias': json_dumps(['arcanismo', 'historia']),
                'idiomas_escolha': 2,
                'caracteristica_nome': 'Pesquisador',
                'caracteristica_descricao': 'Quando tenta aprender algo, geralmente sabe onde encontrar a informação.',
            },
            {
                'nome': 'Marinheiro',
                'pericias': json_dumps(['atletismo', 'percepcao']),
                'ferramentas': json_dumps(['ferramentas de navegador', 'veículos aquáticos']),
                'caracteristica_nome': 'Passagem de Navio',
                'caracteristica_descricao': 'Pode garantir passagem gratuita em navios para você e companheiros.',
            },
            {
                'nome': 'Soldado',
                'pericias': json_dumps(['atletismo', 'intimidacao']),
                'ferramentas': json_dumps(['um tipo de jogo', 'veículos terrestres']),
                'caracteristica_nome': 'Patente Militar',
                'caracteristica_descricao': 'Soldados de menor patente reconhecem sua autoridade.',
            },
            {
                'nome': 'Órfão',
                'pericias': json_dumps(['furtividade', 'prestidigitacao']),
                'ferramentas': json_dumps(['kit de disfarce', 'ferramentas de ladrão']),
                'caracteristica_nome': 'Segredos da Cidade',
                'caracteristica_descricao': 'Conhece os padrões secretos de comunicação das cidades.',
            },
        ]
        
        for ant in antecedentes_data:
            ant.setdefault('ferramentas', json_dumps([]))
            ant.setdefault('idiomas_escolha', 0)
            ant.setdefault('caracteristica_nome', '')
            ant.setdefault('caracteristica_descricao', '')
            
            conn.execute("""
                INSERT INTO antecedentes (
                    nome, pericias, ferramentas, idiomas_escolha,
                    caracteristica_nome, caracteristica_descricao
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ant['nome'], ant['pericias'], ant['ferramentas'],
                ant['idiomas_escolha'], ant['caracteristica_nome'],
                ant['caracteristica_descricao']
            ))
        
        conn.commit()
        print("[DB] ✅ Regras D&D 5e carregadas com sucesso!")

# Nota: A função popular_tipos_criatura() foi movida para app/modulos/regras/base.py
# Use: from app.modulos.regras import popular_tipos_criatura
