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
    Suporta múltiplos modificadores: "1d20", "2d6+3", "4d8-2", "1d6+6+2", "2d8+3-1"
    
    Retorna:
    {
        'expressao': '2d6+3+2',
        'dados': [4, 2],
        'soma_dados': 6,
        'modificador': 5,
        'total': 11
    }
    """
    expressao = expressao.lower().replace(' ', '')
    
    # Padrão para o dado: XdY
    padrao_dado = r'^(\d+)d(\d+)'
    match_dado = re.match(padrao_dado, expressao)
    
    if not match_dado:
        return {
            'erro': f'Expressão inválida: {expressao}',
            'expressao': expressao,
            'total': 0
        }
    
    quantidade = int(match_dado.group(1))
    faces = int(match_dado.group(2))
    
    # Extrai todos os modificadores após o dado (ex: +3+2-1)
    resto_expressao = expressao[match_dado.end():]
    modificadores = re.findall(r'[+-]\d+', resto_expressao)
    modificador = sum(int(m) for m in modificadores) if modificadores else 0
    
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
