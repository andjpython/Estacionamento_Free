# Configuração do Gunicorn para o Render
bind = "0.0.0.0:10000"
workers = 2
worker_class = "sync"
threads = 2
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True
enable_stdio_inheritance = True

# Server Mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None

# SSL
keyfile = None
certfile = None