"""
Gerenciamento de conexões com o banco de dados
"""
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import DBAPIError
from utils.error_logger import ErrorLogger

class DatabaseManager:
    """Gerenciador de conexões com o banco de dados"""
    
    def __init__(self, database_url, **kwargs):
        self.database_url = database_url
        self.engine = None
        self.Session = None
        self.kwargs = kwargs
    
    def init_engine(self):
        """Inicializa o engine do SQLAlchemy"""
        if not self.engine:
            self.engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_size=5,
                max_overflow=10,
                pool_recycle=1800,
                **self.kwargs
            )
            
            # Eventos de conexão
            @event.listens_for(self.engine, 'connect')
            def receive_connect(dbapi_connection, connection_record):
                """Log de conexão estabelecida"""
                ErrorLogger.log_info('DATABASE', 'Conexão estabelecida com o banco')
            
            @event.listens_for(self.engine, 'checkout')
            def receive_checkout(dbapi_connection, connection_record, connection_proxy):
                """Verificação de conexão no checkout"""
                try:
                    dbapi_connection.ping(reconnect=True)
                except DBAPIError as e:
                    ErrorLogger.log_error('DATABASE', 'Erro ao verificar conexão', {'error': str(e)})
                    raise
    
    def init_session(self):
        """Inicializa a sessão do SQLAlchemy"""
        if not self.Session:
            session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(session_factory)
    
    def init_app(self):
        """Inicializa o gerenciador de banco de dados"""
        self.init_engine()
        self.init_session()
    
    @contextmanager
    def session_scope(self):
        """Contexto para gerenciamento de sessão"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            ErrorLogger.log_error('DATABASE', 'Erro na transação', {'error': str(e)})
            raise
        finally:
            session.close()
    
    def check_connection(self):
        """Verifica conexão com o banco"""
        try:
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            return True
        except Exception as e:
            ErrorLogger.log_error('DATABASE', 'Erro ao verificar conexão', {'error': str(e)})
            return False
