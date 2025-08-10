"""
Configurações específicas para produção no Render
"""
from config import Config

class ProductionConfig(Config):
    """Configurações otimizadas para produção"""
    
    # Desabilitar debug
    DEBUG = False
    
    # Logging mais restritivo
    LOG_LEVEL = "WARNING"
    
    # Configurações de segurança
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configurações de banco otimizadas
    DATABASE_POOL_SIZE = 10
    DATABASE_MAX_OVERFLOW = 20
    DATABASE_POOL_RECYCLE = 3600
    
    # Configurações de cache
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Configurações de rate limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_DEFAULT = "200 per day;50 per hour"
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora
    SESSION_REFRESH_EACH_REQUEST = True
