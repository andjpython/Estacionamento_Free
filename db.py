"""
Configuração do SQLAlchemy 2 e funções auxiliares para o banco de dados
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
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

# Criar engine com base no tipo de banco
if database_url.startswith('sqlite:'):
    engine = create_engine(
        database_url,
        connect_args={'check_same_thread': False}
    )
else:
    engine = create_engine(database_url, **engine_config)

# Configurar sessão
session_factory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Criar escopo de sessão thread-safe
SessionLocal = scoped_session(session_factory)

# Classe base para os modelos
Base = declarative_base()

def get_db():
    """Contexto de banco de dados para uso com 'with'"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados"""
    Base.metadata.create_all(bind=engine)