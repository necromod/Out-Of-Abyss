"""
Configurações da aplicação Flask
"""

import os


class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento-oota'
    
    # Caminhos do projeto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SYSTEM_DIR = BASE_DIR
    CAMPAIGN_DIR = os.path.dirname(BASE_DIR)
    
    # Pastas de conteúdo da campanha (somente leitura)
    IMAGENS_DIR = os.path.join(CAMPAIGN_DIR, 'Imagens')
    ITENS_DIR = os.path.join(CAMPAIGN_DIR, 'Itens')
    MONSTROS_DIR = os.path.join(CAMPAIGN_DIR, 'Monstros')
    LIVROS_DIR = os.path.join(CAMPAIGN_DIR, 'Livros')
    NPCS_DIR = os.path.join(CAMPAIGN_DIR, 'NPCS')
    
    # Pasta de dados do sistema
    DATA_DIR = os.path.join(SYSTEM_DIR, 'data')
    
    # Configurações de regras (todas opcionais)
    REGRAS_ATIVAS = {
        'livro_jogador': True,      # Obrigatório - base do sistema
        'xanathar': False,          # Guia de Xanathar
        'tasha': False,             # Caldeirão de Tasha
        'multiverso': False,        # Monstros do Multiverso
        'valdas': False,            # Valda's Spire of Secrets
        'fora_abismo': True         # Out of the Abyss - campanha
    }
    
    # Debug mode
    DEBUG = True


class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False


class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
