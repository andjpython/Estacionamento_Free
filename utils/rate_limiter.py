"""
Configuração do rate limiter
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Criar instância do limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Decorador para limitar tentativas de login
def login_limit():
    """Limita tentativas de login para prevenir força bruta"""
    return limiter.limit(
        "5 per minute, 20 per hour",
        error_message="Muitas tentativas de login. Por favor, aguarde um momento."
    )

# Decorador para limitar requisições de API
def api_limit():
    """Limita requisições de API para prevenir sobrecarga"""
    return limiter.limit(
        "30 per minute",
        error_message="Muitas requisições. Por favor, aguarde um momento."
    )
