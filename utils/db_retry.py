"""
Utilitário para retry de conexões com banco de dados
"""
import time
from functools import wraps
from sqlalchemy.exc import OperationalError, DatabaseError
from utils.error_logger import ErrorLogger

def with_db_retry(max_retries=3, delay=1):
    """
    Decorator para retry de operações de banco de dados
    
    Args:
        max_retries: Número máximo de tentativas
        delay: Tempo de espera entre tentativas em segundos
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DatabaseError) as e:
                    last_error = e
                    if attempt < max_retries - 1:  # Não logar na última tentativa
                        ErrorLogger.log_warning(
                            'DATABASE',
                            f'Tentativa {attempt + 1} de {max_retries} falhou',
                            {'error': str(e)}
                        )
                        time.sleep(delay * (attempt + 1))  # Backoff exponencial
                    continue
            
            # Se chegou aqui, todas as tentativas falharam
            ErrorLogger.log_error(
                'DATABASE',
                'Todas as tentativas de conexão falharam',
                {'error': str(last_error), 'max_retries': max_retries}
            )
            raise last_error
        return wrapper
    return decorator
