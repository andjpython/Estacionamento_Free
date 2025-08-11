"""
Configuração do Gunicorn para produção
"""
import multiprocessing
import os

# Configurações básicas
bind = "0.0.0.0:" + os.getenv("PORT", "8000")
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"  # Usando workers síncronos para compatibilidade com SQLAlchemy
threads = 1  # Single thread por worker para evitar problemas de concorrência

# Timeouts
timeout = 120  # 2 minutos
keepalive = 5
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "warning"

# Configurações de processo
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Hooks de processo
def on_starting(server):
    """Executado quando o servidor está iniciando"""
    pass

def on_reload(server):
    """Executado em reload do código"""
    pass

def on_exit(server):
    """Executado quando o servidor está encerrando"""
    pass

# Configurações de SSL (se necessário)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Configurações de segurança
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190