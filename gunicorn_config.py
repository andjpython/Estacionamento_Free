# Configuração do Gunicorn para o Render
# Render fornece a porta via variável de ambiente PORT
import os
port = os.environ.get("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Ajusta workers dinamicamente quando disponível (Render/Heroku)
import multiprocessing
web_concurrency = os.getenv("WEB_CONCURRENCY")
workers = int(web_concurrency) if web_concurrency else max(2, multiprocessing.cpu_count())
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