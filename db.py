"""
Configuração do SQLAlchemy 2 e funções auxiliares para o banco de dados
"""
import os
from sqlalchemy.ext.declarative import declarative_base
from db.connection import DatabaseManager
from config import active_config

# Obter URL do banco de dados
database_url = os.getenv('DATABASE_URL', str(active_config.DATABASE_URL))

# Normalizar esquemas compatíveis
if database_url.startswith('postgres://'):
    # Render/Heroku usam postgres://; SQLAlchemy aceita postgresql+psycopg
    database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
elif database_url.startswith('postgresql://') and '+psycopg' not in database_url:
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)

# Configurações do engine otimizadas para SQLAlchemy 2
engine_config = {
    'pool_pre_ping': True,
    'pool_size': 5,  # Reduzido para evitar sobrecarga
    'max_overflow': 10,  # Reduzido para evitar sobrecarga
    'pool_timeout': 60,  # Aumentado para dar mais tempo
    'pool_recycle': 1800,  # Reduzido para 30 minutos
    'echo': False,  # Desabilitar logs SQL em produção
    'future': True,  # Habilitar recursos futuros do SQLAlchemy 2
    'connect_args': {
        'connect_timeout': 10,  # Timeout de conexão em segundos
        'keepalives': 1,  # Manter conexões vivas
        'keepalives_idle': 30,  # Tempo ocioso antes de enviar keepalive
        'keepalives_interval': 10,  # Intervalo entre keepalives
        'keepalives_count': 5  # Número de tentativas de keepalive
    }
}

# Classe base para os modelos
Base = declarative_base()

# Criar gerenciador de banco de dados
db_manager = DatabaseManager(
    database_url,
    connect_args={'connect_timeout': 10} if not database_url.startswith('sqlite:') else {}
)

# Inicializar banco de dados
db_manager.init_app()

# Aliases para compatibilidade
engine = db_manager.engine
SessionLocal = db_manager.Session

def get_db():
    """Contexto de banco de dados para uso com 'with'"""
    with db_manager.session_scope() as session:
        yield session

def init_db():
    """Inicializa o banco de dados"""
    Base.metadata.create_all(bind=engine)