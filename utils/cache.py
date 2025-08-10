"""
Sistema de cache para o Sistema de Estacionamento
"""
import json
import hashlib
from typing import Any, Optional, Union
from functools import wraps
from datetime import datetime, timedelta

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class CacheManager:
    """Gerenciador de cache com fallback para memória"""
    
    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        self.memory_cache = {}
        
        if redis_url and REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
            except Exception:
                self.redis_client = None
        
        if not self.redis_client:
            print("⚠️ Redis não disponível, usando cache em memória")
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Gera chave única para o cache"""
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache"""
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                return json.loads(value) if value else None
            except Exception:
                pass
        
        # Fallback para memória
        if key in self.memory_cache:
            data = self.memory_cache[key]
            if data['expires_at'] > datetime.now():
                return data['value']
            else:
                del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Define valor no cache com TTL"""
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        if self.redis_client:
            try:
                return self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(value, default=str)
                )
            except Exception:
                pass
        
        # Fallback para memória
        self.memory_cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
        return True
    
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        if self.redis_client:
            try:
                return bool(self.redis_client.delete(key))
            except Exception:
                pass
        
        # Fallback para memória
        if key in self.memory_cache:
            del self.memory_cache[key]
            return True
        
        return False
    
    def clear(self) -> bool:
        """Limpa todo o cache"""
        if self.redis_client:
            try:
                return bool(self.redis_client.flushdb())
            except Exception:
                pass
        
        # Fallback para memória
        self.memory_cache.clear()
        return True

def cache_result(ttl: int = 300, key_prefix: str = "func"):
    """Decorator para cachear resultados de funções"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Usar cache global se disponível
            cache = getattr(wrapper, '_cache', None)
            if not cache:
                return func(*args, **kwargs)
            
            # Gerar chave única
            cache_key = cache._generate_key(key_prefix, func.__name__, *args, **kwargs)
            
            # Tentar recuperar do cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Executar função e cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator

# Instância global do cache
cache_manager = CacheManager()

# Decorator para usar com a instância global
def cached(ttl: int = 300, key_prefix: str = "func"):
    """Decorator para cachear resultados usando cache global"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = cache_manager._generate_key(key_prefix, func.__name__, *args, **kwargs)
            
            result = cache_manager.get(cache_key)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
