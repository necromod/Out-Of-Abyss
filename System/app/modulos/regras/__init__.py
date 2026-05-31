"""
Módulo de Regras D&D 5e - Sistema Modular

Estrutura organizada por fonte/livro:
- base.py: Perícias, idiomas, tipos de criatura e funções utilitárias
- phb.py: Player's Handbook (Livro do Jogador)
- multiverse.py: Monsters of the Multiverse
- suplementos.py: Outros suplementos (Eberron, Ravnica, etc)
- antecedentes.py: Todos os antecedentes

Uso:
    from app.modulos.regras import popular_todas_regras
    popular_todas_regras()
"""

from .base import popular_dados_base, popular_tipos_criatura, PERICIAS, IDIOMAS, TIPOS_CRIATURA
from .phb import popular_racas_phb, popular_classes_phb
from .multiverse import popular_racas_multiverse
from .antecedentes import popular_antecedentes
from .suplementos import popular_racas_suplementos

__all__ = [
    'popular_todas_regras',
    'popular_dados_base',
    'popular_tipos_criatura',
    'popular_racas_phb',
    'popular_classes_phb',
    'popular_racas_multiverse',
    'popular_racas_suplementos',
    'popular_antecedentes',
    'PERICIAS',
    'IDIOMAS',
    'TIPOS_CRIATURA',
]


def popular_todas_regras():
    """Popula todas as regras D&D 5e de todos os livros"""
    from ..database import get_connection
    
    with get_connection() as conn:
        # Verifica se já tem dados
        cursor = conn.execute("SELECT COUNT(*) as total FROM racas")
        if cursor.fetchone()['total'] > 0:
            print("[DB] Regras D&D já carregadas")
            return
        
        print("[DB] Carregando regras D&D 5e...")
    
    # Ordem de população
    popular_dados_base()      # Perícias, idiomas
    popular_tipos_criatura()  # Tipos de criatura (aberração, besta, etc)
    popular_racas_phb()       # Raças do Livro do Jogador
    popular_classes_phb()     # Classes do Livro do Jogador
    popular_racas_multiverse() # Raças do Monsters of the Multiverse
    popular_racas_suplementos() # Raças de outros suplementos
    popular_antecedentes()    # Antecedentes
    
    print("[DB] [OK] Regras D&D 5e carregadas com sucesso!")
