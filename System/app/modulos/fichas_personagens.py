"""
Módulo de Fichas de Personagens
Gerencia criação, edição e consulta de personagens jogadores
"""

from typing import Dict, List, Any, Optional
from uuid import uuid4
from .regras_base import ATRIBUTOS, PERICIAS, calcular_bonus_proficiencia
from .dados import calcular_modificador_atributo


class Personagem:
    """Representa um personagem jogador"""
    
    def __init__(self, dados: Dict[str, Any] = None):
        dados = dados or {}
        
        self.id = dados.get('id', str(uuid4()))
        self.nome = dados.get('nome', 'Sem Nome')
        self.jogador = dados.get('jogador', '')
        
        # Informações básicas
        self.raca = dados.get('raca', '')
        self.classe = dados.get('classe', '')
        self.nivel = dados.get('nivel', 1)
        self.antecedente = dados.get('antecedente', '')
        self.alinhamento = dados.get('alinhamento', '')
        
        # Atributos (valores de 1 a 20+)
        self.atributos = dados.get('atributos', {
            'forca': 10,
            'destreza': 10,
            'constituicao': 10,
            'inteligencia': 10,
            'sabedoria': 10,
            'carisma': 10
        })
        
        # Perícias com proficiência
        self.pericias_proficientes = dados.get('pericias_proficientes', [])
        self.pericias_expertise = dados.get('pericias_expertise', [])
        
        # Salvaguardas com proficiência
        self.salvaguardas_proficientes = dados.get('salvaguardas_proficientes', [])
        
        # Combate
        self.hp_maximo = dados.get('hp_maximo', 10)
        self.hp_atual = dados.get('hp_atual', self.hp_maximo)
        self.hp_temporario = dados.get('hp_temporario', 0)
        self.dados_vida = dados.get('dados_vida', '1d8')
        self.dados_vida_restantes = dados.get('dados_vida_restantes', self.nivel)
        
        # Classe de Armadura (pode ser editado manualmente)
        self.ca = dados.get('ca', 10)
        self.ca_bonus = dados.get('ca_bonus', 0)
        
        # Movimento
        self.velocidade = dados.get('velocidade', 9)  # metros
        
        # Iniciativa (pode ter bônus adicional)
        self.iniciativa_bonus = dados.get('iniciativa_bonus', 0)
        
        # Condições ativas
        self.condicoes = dados.get('condicoes', [])
        
        # Equipamento
        self.equipamento = dados.get('equipamento', [])
        self.armas = dados.get('armas', [])
        self.armadura = dados.get('armadura', None)
        self.escudo = dados.get('escudo', False)
        
        # Magias (se aplicável)
        self.conjurador = dados.get('conjurador', False)
        self.atributo_conjuracao = dados.get('atributo_conjuracao', None)
        self.espacos_magia = dados.get('espacos_magia', {})
        self.espacos_usados = dados.get('espacos_usados', {})
        self.magias_conhecidas = dados.get('magias_conhecidas', [])
        self.magias_preparadas = dados.get('magias_preparadas', [])
        
        # Habilidades de classe
        self.habilidades = dados.get('habilidades', [])
        
        # Notas do mestre
        self.notas = dados.get('notas', '')
        
        # Morte
        self.sucesso_morte = dados.get('sucesso_morte', 0)
        self.falha_morte = dados.get('falha_morte', 0)
    
    def modificador(self, atributo: str) -> int:
        """Retorna o modificador de um atributo"""
        valor = self.atributos.get(atributo, 10)
        return calcular_modificador_atributo(valor)
    
    def bonus_proficiencia(self) -> int:
        """Retorna o bônus de proficiência baseado no nível"""
        return calcular_bonus_proficiencia(self.nivel)
    
    def modificador_pericia(self, pericia: str) -> int:
        """Calcula o modificador total de uma perícia"""
        atributo = PERICIAS.get(pericia)
        if not atributo:
            return 0
        
        mod = self.modificador(atributo)
        
        if pericia in self.pericias_expertise:
            mod += self.bonus_proficiencia() * 2
        elif pericia in self.pericias_proficientes:
            mod += self.bonus_proficiencia()
        
        return mod
    
    def modificador_salvaguarda(self, atributo: str) -> int:
        """Calcula o modificador de salvaguarda"""
        mod = self.modificador(atributo)
        
        if atributo in self.salvaguardas_proficientes:
            mod += self.bonus_proficiencia()
        
        return mod
    
    def iniciativa(self) -> int:
        """Calcula o bônus de iniciativa"""
        return self.modificador('destreza') + self.iniciativa_bonus
    
    def ca_total(self) -> int:
        """Calcula a CA total"""
        return self.ca + self.ca_bonus
    
    def receber_dano(self, dano: int, tipo: str = None) -> Dict[str, Any]:
        """
        Aplica dano ao personagem
        Retorna informações sobre o resultado
        """
        # Primeiro remove HP temporário
        if self.hp_temporario > 0:
            if dano <= self.hp_temporario:
                self.hp_temporario -= dano
                return {'dano_aplicado': 0, 'hp_temp_perdido': dano, 'hp_atual': self.hp_atual}
            else:
                dano_restante = dano - self.hp_temporario
                hp_temp_perdido = self.hp_temporario
                self.hp_temporario = 0
                dano = dano_restante
        else:
            hp_temp_perdido = 0
        
        self.hp_atual = max(0, self.hp_atual - dano)
        
        return {
            'dano_aplicado': dano,
            'hp_temp_perdido': hp_temp_perdido,
            'hp_atual': self.hp_atual,
            'inconsciente': self.hp_atual == 0
        }
    
    def curar(self, quantidade: int) -> Dict[str, Any]:
        """Cura o personagem"""
        hp_antes = self.hp_atual
        self.hp_atual = min(self.hp_maximo, self.hp_atual + quantidade)
        
        return {
            'cura_aplicada': self.hp_atual - hp_antes,
            'hp_atual': self.hp_atual
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o personagem para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'jogador': self.jogador,
            'raca': self.raca,
            'classe': self.classe,
            'nivel': self.nivel,
            'antecedente': self.antecedente,
            'alinhamento': self.alinhamento,
            'atributos': self.atributos,
            'pericias_proficientes': self.pericias_proficientes,
            'pericias_expertise': self.pericias_expertise,
            'salvaguardas_proficientes': self.salvaguardas_proficientes,
            'hp_maximo': self.hp_maximo,
            'hp_atual': self.hp_atual,
            'hp_temporario': self.hp_temporario,
            'dados_vida': self.dados_vida,
            'dados_vida_restantes': self.dados_vida_restantes,
            'ca': self.ca,
            'ca_bonus': self.ca_bonus,
            'velocidade': self.velocidade,
            'iniciativa_bonus': self.iniciativa_bonus,
            'condicoes': self.condicoes,
            'equipamento': self.equipamento,
            'armas': self.armas,
            'armadura': self.armadura,
            'escudo': self.escudo,
            'conjurador': self.conjurador,
            'atributo_conjuracao': self.atributo_conjuracao,
            'espacos_magia': self.espacos_magia,
            'espacos_usados': self.espacos_usados,
            'magias_conhecidas': self.magias_conhecidas,
            'magias_preparadas': self.magias_preparadas,
            'habilidades': self.habilidades,
            'notas': self.notas,
            'sucesso_morte': self.sucesso_morte,
            'falha_morte': self.falha_morte,
            # Valores calculados
            'bonus_proficiencia': self.bonus_proficiencia(),
            'iniciativa': self.iniciativa(),
            'ca_total': self.ca_total()
        }


class GerenciadorPersonagens:
    """Gerencia todos os personagens da sessão"""
    
    def __init__(self):
        self._personagens: Dict[str, Personagem] = {}
    
    def criar(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo personagem"""
        personagem = Personagem(dados)
        self._personagens[personagem.id] = personagem
        return {'sucesso': True, 'personagem': personagem.to_dict()}
    
    def obter(self, id: str) -> Optional[Dict[str, Any]]:
        """Obtém um personagem pelo ID"""
        personagem = self._personagens.get(id)
        return personagem.to_dict() if personagem else None
    
    def listar_todos(self) -> List[Dict[str, Any]]:
        """Lista todos os personagens"""
        return [p.to_dict() for p in self._personagens.values()]
    
    def atualizar(self, id: str, dados: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza dados de um personagem"""
        personagem = self._personagens.get(id)
        if not personagem:
            return {'sucesso': False, 'erro': 'Personagem não encontrado'}
        
        # Atualiza campos presentes nos dados
        for campo, valor in dados.items():
            if hasattr(personagem, campo):
                setattr(personagem, campo, valor)
        
        return {'sucesso': True, 'personagem': personagem.to_dict()}
    
    def editar_campo(self, id: str, campo: str, valor: Any) -> Dict[str, Any]:
        """Edita um campo específico em tempo real"""
        personagem = self._personagens.get(id)
        if not personagem:
            return {'sucesso': False, 'erro': 'Personagem não encontrado'}
        
        # Suporta campos aninhados como "atributos.forca"
        if '.' in campo:
            partes = campo.split('.')
            obj = personagem
            for parte in partes[:-1]:
                if isinstance(obj, dict):
                    obj = obj.get(parte, {})
                else:
                    obj = getattr(obj, parte, {})
            
            if isinstance(obj, dict):
                obj[partes[-1]] = valor
            else:
                setattr(obj, partes[-1], valor)
        else:
            if hasattr(personagem, campo):
                setattr(personagem, campo, valor)
        
        return {'sucesso': True, 'campo': campo, 'valor': valor, 'personagem': personagem.to_dict()}
    
    def remover(self, id: str) -> Dict[str, Any]:
        """Remove um personagem"""
        if id in self._personagens:
            del self._personagens[id]
            return {'sucesso': True}
        return {'sucesso': False, 'erro': 'Personagem não encontrado'}
