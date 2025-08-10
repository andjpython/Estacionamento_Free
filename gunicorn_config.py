# Configuração do Gunicorn para o Render
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
threads = 4
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
worker_connections = 1000

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# SSL
keyfile = None
certfile = None

# Process Naming
proc_name = "estacionamento_rotativo"

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None