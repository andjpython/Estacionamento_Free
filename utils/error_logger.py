"""
Sistema de logs para erros e monitoramento
"""
import logging
import os
from datetime import datetime
import pytz
from logging.handlers import RotatingFileHandler

# Configurar timezone
tz = pytz.timezone('America/Sao_Paulo')

# Criar diretório de logs se não existir
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar logger principal
logger = logging.getLogger('estacionamento_rotativo')
logger.setLevel(logging.DEBUG)

# Formato do log
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(extra_info)s'
)

# Handler para arquivo
file_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=1024 * 1024,  # 1MB
    backupCount=10,
    encoding='utf-8'
)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Adicionar handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class ErrorLogger:
    @staticmethod
    def log_error(error_type, message, extra_info=None):
        """
        Registra um erro no log
        
        Args:
            error_type: Tipo do erro (ex: 'DATABASE', 'AUTH', 'NETWORK')
            message: Mensagem descritiva do erro
            extra_info: Informações adicionais em formato dict
        """
        if extra_info is None:
            extra_info = {}
            
        # Adicionar timestamp
        extra_info['timestamp'] = datetime.now(tz).isoformat()
        
        logger.error(
            f"{error_type}: {message}",
            extra={'extra_info': extra_info}
        )
    
    @staticmethod
    def log_warning(warning_type, message, extra_info=None):
        """
        Registra um aviso no log
        """
        if extra_info is None:
            extra_info = {}
            
        extra_info['timestamp'] = datetime.now(tz).isoformat()
        
        logger.warning(
            f"{warning_type}: {message}",
            extra={'extra_info': extra_info}
        )
    
    @staticmethod
    def log_info(info_type, message, extra_info=None):
        """
        Registra uma informação no log
        """
        if extra_info is None:
            extra_info = {}
            
        extra_info['timestamp'] = datetime.now(tz).isoformat()
        
        logger.info(
            f"{info_type}: {message}",
            extra={'extra_info': extra_info}
        )
