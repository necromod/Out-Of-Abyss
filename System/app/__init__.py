"""
Out of the Abyss - Sistema de Mestragem D&D 5e
Aplicação Flask principal
"""

from flask import Flask
from .config import Config


def create_app(config_class=Config):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='static')
    
    app.config.from_object(config_class)
    
    # Inicializar banco de dados SQLite
    with app.app_context():
        from .modulos.db_init import inicializar_banco
        inicializar_banco()
    
    # Registrar Blueprints
    from .routes.main import main_bp
    from .routes.sessao import sessao_bp
    from .routes.combate import combate_bp
    from .routes.fichas import fichas_bp
    from .routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(sessao_bp, url_prefix='/sessao')
    app.register_blueprint(combate_bp, url_prefix='/combate')
    app.register_blueprint(fichas_bp, url_prefix='/fichas')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
