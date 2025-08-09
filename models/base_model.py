"""
Modelo base com campos comuns
"""
from datetime import datetime
from sqlalchemy import Column, DateTime
from db import Base

class BaseModel(Base):
    """Classe base com campos de auditoria"""
    __abstract__ = True

    criado_em = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    atualizado_em = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )
