"""
Arquivo WSGI para inicialização no Render
"""
import os
from app import app
from db import init_db

# Configurar ambiente
os.environ['FLASK_ENV'] = 'production'

# Inicializar banco de dados se necessário
if os.environ.get('AUTO_INIT_DB', '1') == '1':
    try:
        init_db()
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

# Aplicação para o Gunicorn
application = app
