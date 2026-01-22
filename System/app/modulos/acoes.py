"""
Módulo de Ações - Tipos de ações em combate D&D 5e
"""

from typing import Dict, List, Any


# ==================== AÇÕES PADRÃO ====================

ACOES_COMBATE = {
    'atacar': {
        'nome': 'Atacar',
        'tipo': 'acao',
        'descricao': 'Fazer um ataque corpo a corpo ou à distância',
        'requer_alvo': True
    },
    'conjurar_magia': {
        'nome': 'Conjurar Magia',
        'tipo': 'acao',
        'descricao': 'Conjurar uma magia com tempo de conjuração de 1 ação',
        'requer_alvo': 'depende'
    },
    'correr': {
        'nome': 'Correr',
        'tipo': 'acao',
        'descricao': 'Ganhar movimento extra igual à velocidade',
        'requer_alvo': False,
        'efeito': 'velocidade_dobrada'
    },
    'desengajar': {
        'nome': 'Desengajar',
        'tipo': 'acao',
        'descricao': 'Movimento não provoca ataques de oportunidade pelo resto do turno',
        'requer_alvo': False,
        'efeito': 'sem_ataque_oportunidade'
    },
    'esquivar': {
        'nome': 'Esquivar',
        'tipo': 'acao',
        'descricao': 'Até o próximo turno: ataques têm desvantagem, salvaguardas de Destreza com vantagem',
        'requer_alvo': False,
        'efeito': 'esquivando',
        'duracao': 'ate_proximo_turno'
    },
    'ajudar': {
        'nome': 'Ajudar',
        'tipo': 'acao',
        'descricao': 'Dar vantagem a um aliado em teste de habilidade ou ataque',
        'requer_alvo': True,
        'efeito': 'vantagem_aliado'
    },
    'esconder': {
        'nome': 'Esconder',
        'tipo': 'acao',
        'descricao': 'Fazer teste de Furtividade para se esconder',
        'requer_alvo': False,
        'teste': {'pericia': 'furtividade'}
    },
    'preparar': {
        'nome': 'Preparar',
        'tipo': 'acao',
        'descricao': 'Preparar uma ação para executar como reação',
        'requer_alvo': False,
        'efeito': 'acao_preparada'
    },
    'procurar': {
        'nome': 'Procurar',
        'tipo': 'acao',
        'descricao': 'Fazer teste de Percepção ou Investigação',
        'requer_alvo': False,
        'teste': {'pericia': ['percepcao', 'investigacao']}
    },
    'usar_objeto': {
        'nome': 'Usar Objeto',
        'tipo': 'acao',
        'descricao': 'Interagir com um objeto que requer ação',
        'requer_alvo': False
    }
}


# ==================== AÇÕES BÔNUS COMUNS ====================

ACOES_BONUS_COMUNS = {
    'ataque_segunda_arma': {
        'nome': 'Ataque com Segunda Arma',
        'descricao': 'Ataque com arma leve na outra mão (sem mod de atributo no dano)',
        'requisito': 'duas_armas_leves'
    },
    'conjurar_magia_bonus': {
        'nome': 'Conjurar Magia (Bônus)',
        'descricao': 'Conjurar magia com tempo de conjuração de 1 ação bônus'
    }
}


# ==================== REAÇÕES COMUNS ====================

REACOES_COMUNS = {
    'ataque_oportunidade': {
        'nome': 'Ataque de Oportunidade',
        'descricao': 'Atacar criatura que sai do seu alcance sem Desengajar',
        'gatilho': 'criatura_sai_alcance'
    },
    'acao_preparada': {
        'nome': 'Ação Preparada',
        'descricao': 'Executar ação preparada quando gatilho ocorre',
        'gatilho': 'definido_pelo_jogador'
    }
}


class GerenciadorAcoes:
    """Gerencia tipos de ações disponíveis"""
    
    @staticmethod
    def obter_acao(nome: str) -> Dict[str, Any]:
        """Retorna informações de uma ação"""
        return ACOES_COMBATE.get(nome.lower())
    
    @staticmethod
    def listar_acoes() -> List[Dict[str, Any]]:
        """Lista todas as ações padrão de combate"""
        return [{'id': k, **v} for k, v in ACOES_COMBATE.items()]
    
    @staticmethod
    def listar_acoes_bonus() -> List[Dict[str, Any]]:
        """Lista ações bônus comuns"""
        return [{'id': k, **v} for k, v in ACOES_BONUS_COMUNS.items()]
    
    @staticmethod
    def listar_reacoes() -> List[Dict[str, Any]]:
        """Lista reações comuns"""
        return [{'id': k, **v} for k, v in REACOES_COMUNS.items()]
    
    @staticmethod
    def verificar_ataque_oportunidade(
        criatura_posicao_inicial: tuple,
        criatura_posicao_final: tuple,
        inimigo_posicao: tuple,
        alcance_inimigo: float = 1.5
    ) -> bool:
        """
        Verifica se movimento provoca ataque de oportunidade
        Simplificado: verifica se saiu do alcance
        """
        def distancia(p1, p2):
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
        
        dist_inicial = distancia(criatura_posicao_inicial, inimigo_posicao)
        dist_final = distancia(criatura_posicao_final, inimigo_posicao)
        
        # Se estava no alcance e saiu, provoca ataque de oportunidade
        estava_no_alcance = dist_inicial <= alcance_inimigo
        saiu_do_alcance = dist_final > alcance_inimigo
        
        return estava_no_alcance and saiu_do_alcance
