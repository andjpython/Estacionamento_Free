"""
Configuração do SQLAlchemy e funções auxiliares para o banco de dados
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import active_config

# Cria o engine do SQLAlchemy usando a URL do banco de dados da configuração
engine = create_engine(
    active_config.DATABASE_URL,
    # Configurações recomendadas para produção
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Reconecta após 30 minutos
)

# Cria uma fábrica de sessões thread-safe
session_factory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Cria um escopo de sessão para garantir thread safety
SessionLocal = scoped_session(session_factory)

# Classe base para os modelos ORM
Base = declarative_base()

def get_db():
    """
    Função geradora de contexto para obter uma sessão do banco de dados.
    Uso:
        with get_db() as db:
            db.query(...)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    Normalmente não é necessário chamar diretamente, use Alembic para migrations.
    """
    Base.metadata.create_all(bind=engine)
