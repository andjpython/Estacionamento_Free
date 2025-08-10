"""
Gerenciador de contexto para sessões do banco de dados
"""
from contextlib import contextmanager
from sqlalchemy.orm import Session
from db import SessionLocal

@contextmanager
def get_db_session() -> Session:
    """Gerenciador de contexto para sessões do banco de dados"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

