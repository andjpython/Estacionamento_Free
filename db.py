"""
Configuração do SQLAlchemy 2 e funções auxiliares para o banco de dados
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from config import active_config

# Obter URL do banco de dados
database_url = os.getenv('DATABASE_URL', str(active_config.DATABASE_URL))

# Corrigir URL do PostgreSQL se necessário (Render usa postgres://, SQLAlchemy precisa de postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

# Configurações do engine otimizadas para SQLAlchemy 2
engine_config = {
    'pool_pre_ping': True,
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'echo': False,  # Desabilitar logs SQL em produção
    'future': True  # Habilitar recursos futuros do SQLAlchemy 2
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