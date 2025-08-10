"""Configuração do Gunicorn para o Render"""
import multiprocessing

# Configurações do servidor
bind = "0.0.0.0:10000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
timeout = 120

# Configurações de logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"
