"""
Configuração padronizada de logging para todo o sistema
"""
import logging
import sys
from config import active_config

def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger padronizado para o módulo especificado.
    
    Args:
        name: Nome do módulo (geralmente __name__)
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evita configuração duplicada
    if logger.handlers:
        return logger
    
    # Configurar nível baseado na configuração ativa
    level = getattr(logging, active_config.LOG_LEVEL.upper())
    logger.setLevel(level)
    
    # Criar handler para console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Criar formatter
    formatter = logging.Formatter(active_config.LOG_FORMAT)
    handler.setFormatter(formatter)
    
    # Adicionar handler ao logger
    logger.addHandler(handler)
    
    # Evitar propagação para loggers pai
    logger.propagate = False
    
    return logger

def log_operation(logger: logging.Logger, operation: str, details: dict = None):
    """
    Log padronizado para operações do sistema.
    
    Args:
        logger: Logger configurado
        operation: Descrição da operação
        details: Detalhes adicionais (opcional)
    """
    if details:
        message = f"{operation} - {details}"
    else:
        message = operation
        
    logger.info(message)

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log padronizado para erros.
    
    Args:
        logger: Logger configurado
        error: Exceção capturada
        context: Contexto onde o erro ocorreu
    """
    if context:
        message = f"Erro em {context}: {str(error)}"
    else:
        message = f"Erro: {str(error)}"
        
    logger.error(message, exc_info=True) 