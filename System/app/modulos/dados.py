"""
Módulo de Dados - Rolagem de dados D&D 5e
"""

import random
import re
from typing import Dict, List, Any, Optional


def rolar_dado(faces: int) -> int:
    """Rola um dado com número específico de faces"""
    return random.randint(1, faces)


def rolar_dados(quantidade: int, faces: int) -> List[int]:
    """Rola múltiplos dados e retorna lista de resultados"""
    return [rolar_dado(faces) for _ in range(quantidade)]


def rolar_expressao(expressao: str) -> Dict[str, Any]:
    """
    Interpreta e rola uma expressão de dados no formato D&D
    Exemplos: "1d20", "2d6+3", "4d8-2", "1d20+5"
    
    Retorna:
    {
        'expressao': '2d6+3',
        'dados': [4, 2],
        'soma_dados': 6,
        'modificador': 3,
        'total': 9
    }
    """
    expressao = expressao.lower().replace(' ', '')
    
    # Padrão: XdY+Z ou XdY-Z ou XdY
    padrao = r'^(\d+)d(\d+)([+-]\d+)?$'
    match = re.match(padrao, expressao)
    
    if not match:
        return {
            'erro': f'Expressão inválida: {expressao}',
            'expressao': expressao,
            'total': 0
        }
    
    quantidade = int(match.group(1))
    faces = int(match.group(2))
    modificador_str = match.group(3)
    modificador = int(modificador_str) if modificador_str else 0
    
    dados = rolar_dados(quantidade, faces)
    soma_dados = sum(dados)
    total = soma_dados + modificador
    
    return {
        'expressao': expressao,
        'dados': dados,
        'soma_dados': soma_dados,
        'modificador': modificador,
        'total': total,
        'critico': dados[0] == faces if quantidade == 1 and faces == 20 else None,
        'falha_critica': dados[0] == 1 if quantidade == 1 and faces == 20 else None
    }


def rolar_com_vantagem(modificador: int = 0) -> Dict[str, Any]:
    """Rola 1d20 com vantagem (maior dos dois)"""
    dado1 = rolar_dado(20)
    dado2 = rolar_dado(20)
    escolhido = max(dado1, dado2)
    
    return {
        'tipo': 'vantagem',
        'dados': [dado1, dado2],
        'escolhido': escolhido,
        'modificador': modificador,
        'total': escolhido + modificador,
        'critico': escolhido == 20,
        'falha_critica': escolhido == 1
    }


def rolar_com_desvantagem(modificador: int = 0) -> Dict[str, Any]:
    """Rola 1d20 com desvantagem (menor dos dois)"""
    dado1 = rolar_dado(20)
    dado2 = rolar_dado(20)
    escolhido = min(dado1, dado2)
    
    return {
        'tipo': 'desvantagem',
        'dados': [dado1, dado2],
        'escolhido': escolhido,
        'modificador': modificador,
        'total': escolhido + modificador,
        'critico': escolhido == 20,
        'falha_critica': escolhido == 1
    }


def calcular_modificador_atributo(valor: int) -> int:
    """Calcula o modificador de um atributo (D&D 5e)"""
    return (valor - 10) // 2
