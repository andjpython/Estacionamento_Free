"""
Sistema de logging estruturado para o Sistema de Estacionamento
"""
import logging
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class StructuredFormatter(logging.Formatter):
    """Formatador de logs estruturado em JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Adicionar dados extras se existirem
        if hasattr(record, 'extra_data'):
            log_entry.update(record.extra_data)
            
        # Adicionar exceção se existir
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logger(
    name: str = "estacionamento",
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """Configura e retorna um logger estruturado"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    formatter = StructuredFormatter()
    
    # Handler para console
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_operation(
    logger: logging.Logger,
    operation: str,
    user: str,
    details: Dict[str, Any],
    level: str = "INFO"
) -> None:
    """Log de operações do sistema com contexto estruturado"""
    
    extra_data = {
        "operation": operation,
        "user": user,
        "details": details,
        "session_id": getattr(details, 'session_id', None)
    }
    
    log_method = getattr(logger, level.lower())
    log_method(f"Operação: {operation}", extra={"extra_data": extra_data})

# Logger padrão do sistema
system_logger = setup_logger("estacionamento.system")
security_logger = setup_logger("estacionamento.security")
database_logger = setup_logger("estacionamento.database")
