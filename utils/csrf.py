"""
Configuração do CSRF
"""
from flask_wtf.csrf import CSRFProtect

# Criar instância do CSRF
csrf = CSRFProtect()

def init_csrf(app):
    """Inicializa a proteção CSRF"""
    csrf.init_app(app)
    
    # Configurar chave secreta para tokens CSRF
    app.config['WTF_CSRF_SECRET_KEY'] = app.config.get('SECRET_KEY', 'seu_segredo_super_secreto_aqui')
    
    # Configurar tempo de expiração do token CSRF (1 hora)
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600
