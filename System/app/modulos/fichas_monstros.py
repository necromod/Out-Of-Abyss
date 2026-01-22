"""
Módulo de Fichas de Monstros
Gerencia monstros base e instâncias de combate
"""

from typing import Dict, List, Any, Optional
from uuid import uuid4
from .dados import calcular_modificador_atributo, rolar_expressao


class Monstro:
    """Representa um monstro base (template)"""
    
    def __init__(self, dados: Dict[str, Any] = None):
        dados = dados or {}
        
        self.id = dados.get('id', str(uuid4()))
        self.nome = dados.get('nome', 'Monstro Desconhecido')
        self.tipo = dados.get('tipo', 'aberração')  # aberração, besta, constructo, etc
        self.tamanho = dados.get('tamanho', 'Médio')
        self.alinhamento = dados.get('alinhamento', 'neutro')
        
        # Nível de Desafio
        self.nd = dados.get('nd', 0)  # Pode ser 0, 1/8, 1/4, 1/2, 1, 2, etc
        self.xp = dados.get('xp', 0)
        
        # Atributos
        self.atributos = dados.get('atributos', {
            'forca': 10,
            'destreza': 10,
            'constituicao': 10,
            'inteligencia': 10,
            'sabedoria': 10,
            'carisma': 10
        })
        
        # Combate
        self.ca = dados.get('ca', 10)
        self.ca_tipo = dados.get('ca_tipo', '')  # Ex: "armadura natural", "couro"
        self.hp_formula = dados.get('hp_formula', '2d8')  # Ex: "4d10+12"
        self.hp_medio = dados.get('hp_medio', None)
        self.velocidade = dados.get('velocidade', {'terrestre': 9})
        
        # Salvaguardas com bônus
        self.salvaguardas = dados.get('salvaguardas', {})
        
        # Perícias com bônus
        self.pericias = dados.get('pericias', {})
        
        # Resistências, Imunidades, Vulnerabilidades
        self.resistencias = dados.get('resistencias', [])
        self.imunidades_dano = dados.get('imunidades_dano', [])
        self.imunidades_condicao = dados.get('imunidades_condicao', [])
        self.vulnerabilidades = dados.get('vulnerabilidades', [])
        
        # Sentidos
        self.sentidos = dados.get('sentidos', {})
        self.percepcao_passiva = dados.get('percepcao_passiva', 10)
        
        # Idiomas
        self.idiomas = dados.get('idiomas', [])
        
        # Habilidades especiais
        self.habilidades = dados.get('habilidades', [])
        
        # Ações
        self.acoes = dados.get('acoes', [])
        self.acoes_bonus = dados.get('acoes_bonus', [])
        self.reacoes = dados.get('reacoes', [])
        self.acoes_lendarias = dados.get('acoes_lendarias', [])
        
        # Imagem
        self.imagem = dados.get('imagem', None)
        
        # Notas
        self.notas = dados.get('notas', '')
        
        # Fonte (livro)
        self.fonte = dados.get('fonte', 'Livro do Mestre')
    
    def modificador(self, atributo: str) -> int:
        """Retorna o modificador de um atributo"""
        valor = self.atributos.get(atributo, 10)
        return calcular_modificador_atributo(valor)
    
    def calcular_hp(self) -> int:
        """Rola HP baseado na fórmula"""
        if self.hp_medio:
            return self.hp_medio
        resultado = rolar_expressao(self.hp_formula)
        return resultado.get('total', 1)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'tamanho': self.tamanho,
            'alinhamento': self.alinhamento,
            'nd': self.nd,
            'xp': self.xp,
            'atributos': self.atributos,
            'ca': self.ca,
            'ca_tipo': self.ca_tipo,
            'hp_formula': self.hp_formula,
            'hp_medio': self.hp_medio,
            'velocidade': self.velocidade,
            'salvaguardas': self.salvaguardas,
            'pericias': self.pericias,
            'resistencias': self.resistencias,
            'imunidades_dano': self.imunidades_dano,
            'imunidades_condicao': self.imunidades_condicao,
            'vulnerabilidades': self.vulnerabilidades,
            'sentidos': self.sentidos,
            'percepcao_passiva': self.percepcao_passiva,
            'idiomas': self.idiomas,
            'habilidades': self.habilidades,
            'acoes': self.acoes,
            'acoes_bonus': self.acoes_bonus,
            'reacoes': self.reacoes,
            'acoes_lendarias': self.acoes_lendarias,
            'imagem': self.imagem,
            'notas': self.notas,
            'fonte': self.fonte
        }


class InstanciaMonstro:
    """Instância de monstro para combate (com HP próprio, condições, etc)"""
    
    def __init__(self, monstro_base: Monstro, nome_instancia: str = None):
        self.id = str(uuid4())
        self.monstro_base_id = monstro_base.id
        self.nome = nome_instancia or monstro_base.nome
        
        # Copia dados do monstro base
        self.monstro_base = monstro_base
        
        # Estado de combate (editável)
        self.hp_maximo = monstro_base.calcular_hp()
        self.hp_atual = self.hp_maximo
        self.ca = monstro_base.ca
        
        # Condições ativas
        self.condicoes = []
        
        # Concentração em magia
        self.concentrando = None
        
        # Notas de combate
        self.notas_combate = ''
        
        # Ações usadas (para ações lendárias, recarga, etc)
        self.acoes_usadas = {}
    
    def receber_dano(self, dano: int, tipo: str = None) -> Dict[str, Any]:
        """Aplica dano considerando resistências e vulnerabilidades"""
        dano_final = dano
        modificador = 'normal'
        
        if tipo:
            if tipo in self.monstro_base.imunidades_dano:
                dano_final = 0
                modificador = 'imune'
            elif tipo in self.monstro_base.resistencias:
                dano_final = dano // 2
                modificador = 'resistência'
            elif tipo in self.monstro_base.vulnerabilidades:
                dano_final = dano * 2
                modificador = 'vulnerável'
        
        self.hp_atual = max(0, self.hp_atual - dano_final)
        
        return {
            'dano_original': dano,
            'tipo_dano': tipo,
            'modificador': modificador,
            'dano_aplicado': dano_final,
            'hp_atual': self.hp_atual,
            'morto': self.hp_atual == 0
        }
    
    def curar(self, quantidade: int) -> Dict[str, Any]:
        """Cura a instância"""
        hp_antes = self.hp_atual
        self.hp_atual = min(self.hp_maximo, self.hp_atual + quantidade)
        
        return {
            'cura_aplicada': self.hp_atual - hp_antes,
            'hp_atual': self.hp_atual
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário (inclui dados do monstro base)"""
        base = self.monstro_base.to_dict()
        return {
            **base,
            'instancia_id': self.id,
            'nome_instancia': self.nome,
            'hp_maximo': self.hp_maximo,
            'hp_atual': self.hp_atual,
            'ca': self.ca,
            'condicoes': self.condicoes,
            'concentrando': self.concentrando,
            'notas_combate': self.notas_combate,
            'acoes_usadas': self.acoes_usadas
        }


class GerenciadorMonstros:
    """Gerencia monstros base e instâncias"""
    
    def __init__(self):
        self._monstros_base: Dict[str, Monstro] = {}
        self._instancias: Dict[str, InstanciaMonstro] = {}
        
        # Carrega alguns monstros de exemplo
        self._carregar_monstros_exemplo()
    
    def _carregar_monstros_exemplo(self):
        """Carrega monstros básicos para teste"""
        goblin = Monstro({
            'nome': 'Goblin',
            'tipo': 'humanoide',
            'tamanho': 'Pequeno',
            'alinhamento': 'neutro e mau',
            'nd': 0.25,
            'xp': 50,
            'atributos': {
                'forca': 8, 'destreza': 14, 'constituicao': 10,
                'inteligencia': 10, 'sabedoria': 8, 'carisma': 8
            },
            'ca': 15,
            'ca_tipo': 'couro, escudo',
            'hp_formula': '2d6',
            'hp_medio': 7,
            'velocidade': {'terrestre': 9},
            'pericias': {'furtividade': 6},
            'sentidos': {'visão no escuro': '18m'},
            'percepcao_passiva': 9,
            'idiomas': ['comum', 'goblin'],
            'habilidades': [
                {'nome': 'Fuga Ardilosa', 'descricao': 'O goblin pode realizar a ação de Desengajar ou Esconder como ação bônus em cada um de seus turnos.'}
            ],
            'acoes': [
                {
                    'nome': 'Cimitarra',
                    'tipo': 'ataque_arma',
                    'bonus_ataque': 4,
                    'alcance': '1,5m',
                    'alvo': 'uma criatura',
                    'dano': '1d6+2',
                    'tipo_dano': 'cortante'
                },
                {
                    'nome': 'Arco Curto',
                    'tipo': 'ataque_arma',
                    'bonus_ataque': 4,
                    'alcance': '24/96m',
                    'alvo': 'uma criatura',
                    'dano': '1d6+2',
                    'tipo_dano': 'perfurante'
                }
            ],
            'fonte': 'Livro do Mestre'
        })
        self._monstros_base[goblin.id] = goblin
    
    def adicionar_monstro_base(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Adiciona um novo monstro base"""
        monstro = Monstro(dados)
        self._monstros_base[monstro.id] = monstro
        return {'sucesso': True, 'monstro': monstro.to_dict()}
    
    def obter(self, id: str) -> Optional[Dict[str, Any]]:
        """Obtém monstro base ou instância"""
        if id in self._monstros_base:
            return self._monstros_base[id].to_dict()
        if id in self._instancias:
            return self._instancias[id].to_dict()
        return None
    
    def listar_todos(self) -> List[Dict[str, Any]]:
        """Lista todos os monstros base"""
        return [m.to_dict() for m in self._monstros_base.values()]
    
    def criar_instancia(self, monstro_base_id: str, nome_instancia: str = None) -> Dict[str, Any]:
        """Cria uma instância de monstro para combate"""
        monstro_base = self._monstros_base.get(monstro_base_id)
        if not monstro_base:
            return {'sucesso': False, 'erro': 'Monstro base não encontrado'}
        
        instancia = InstanciaMonstro(monstro_base, nome_instancia)
        self._instancias[instancia.id] = instancia
        
        return {'sucesso': True, 'instancia': instancia.to_dict()}
    
    def editar_campo_instancia(self, id: str, campo: str, valor: Any) -> Dict[str, Any]:
        """Edita um campo de uma instância"""
        instancia = self._instancias.get(id)
        if not instancia:
            return {'sucesso': False, 'erro': 'Instância não encontrada'}
        
        if hasattr(instancia, campo):
            setattr(instancia, campo, valor)
            return {'sucesso': True, 'campo': campo, 'valor': valor}
        
        return {'sucesso': False, 'erro': f'Campo {campo} não existe'}
    
    def remover_instancia(self, id: str) -> Dict[str, Any]:
        """Remove uma instância"""
        if id in self._instancias:
            del self._instancias[id]
            return {'sucesso': True}
        return {'sucesso': False, 'erro': 'Instância não encontrada'}
    
    def listar_instancias(self) -> List[Dict[str, Any]]:
        """Lista todas as instâncias ativas"""
        return [i.to_dict() for i in self._instancias.values()]
