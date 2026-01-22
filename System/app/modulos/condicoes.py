"""
Módulo de Condições - Estados e condições D&D 5e
"""

from typing import Dict, List, Any, Optional
from .regras_base import CONDICOES


class GerenciadorCondicoes:
    """Gerencia condições aplicadas a criaturas"""
    
    @staticmethod
    def obter_condicao(nome: str) -> Optional[Dict[str, Any]]:
        """Retorna informações de uma condição"""
        return CONDICOES.get(nome.lower())
    
    @staticmethod
    def listar_todas() -> List[Dict[str, Any]]:
        """Lista todas as condições disponíveis"""
        return [
            {'id': k, **v}
            for k, v in CONDICOES.items()
        ]
    
    @staticmethod
    def aplicar_condicao(criatura: Dict, condicao: str, detalhes: Dict = None) -> Dict[str, Any]:
        """
        Aplica uma condição a uma criatura
        
        detalhes pode conter:
        - nivel (para exaustão)
        - duracao
        - fonte
        """
        detalhes = detalhes or {}
        
        info_condicao = CONDICOES.get(condicao.lower())
        if not info_condicao:
            return {'sucesso': False, 'erro': f'Condição {condicao} não existe'}
        
        condicao_aplicada = {
            'nome': condicao.lower(),
            'nivel': detalhes.get('nivel', 1) if condicao.lower() == 'exausto' else None,
            'duracao': detalhes.get('duracao'),
            'fonte': detalhes.get('fonte'),
            'efeitos': info_condicao.get('efeitos', [])
        }
        
        return {
            'sucesso': True,
            'condicao': condicao_aplicada,
            'info': info_condicao
        }
    
    @staticmethod
    def remover_condicao(criatura_condicoes: List, condicao: str) -> Dict[str, Any]:
        """Remove uma condição de uma criatura"""
        for i, c in enumerate(criatura_condicoes):
            if c.get('nome') == condicao.lower():
                removida = criatura_condicoes.pop(i)
                return {'sucesso': True, 'removida': removida}
        
        return {'sucesso': False, 'erro': f'Criatura não possui a condição {condicao}'}
    
    @staticmethod
    def verificar_imunidade(imunidades_condicao: List[str], condicao: str) -> bool:
        """Verifica se a criatura é imune a uma condição"""
        return condicao.lower() in [i.lower() for i in imunidades_condicao]
    
    @staticmethod
    def aumentar_exaustao(nivel_atual: int) -> Dict[str, Any]:
        """Aumenta o nível de exaustão"""
        novo_nivel = min(6, nivel_atual + 1)
        info = CONDICOES.get('exausto', {}).get('niveis', {})
        
        return {
            'nivel_anterior': nivel_atual,
            'nivel_atual': novo_nivel,
            'efeito': info.get(novo_nivel, ''),
            'morte': novo_nivel >= 6
        }
    
    @staticmethod
    def reduzir_exaustao(nivel_atual: int) -> Dict[str, Any]:
        """Reduz o nível de exaustão (geralmente após descanso longo)"""
        novo_nivel = max(0, nivel_atual - 1)
        
        return {
            'nivel_anterior': nivel_atual,
            'nivel_atual': novo_nivel,
            'curado': novo_nivel == 0
        }
