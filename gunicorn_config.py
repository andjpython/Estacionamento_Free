# Configuração do Gunicorn para o Render
bind = "0.0.0.0:10000"
workers = 1
worker_class = "sync"  # Mudamos de 'gevent' para 'sync'
threads = 2
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None

# SSL
keyfile = None
certfile = None