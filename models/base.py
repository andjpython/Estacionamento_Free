"""
Modelo base para todas as entidades
"""
from datetime import datetime
import pytz
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
from db import Base

class ModelBase:
    """Classe base para todos os modelos"""
    
    @declared_attr
    def __tablename__(cls):
        """Define nome da tabela automaticamente"""
        return cls.__name__.lower()
    
    # Campos comuns para auditoria
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC), 
                       onupdate=lambda: datetime.now(pytz.UTC))
    
    def to_dict(self):
        """Converte modelo para dicionário"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria modelo a partir de dicionário"""
        return cls(**{
            key: value
            for key, value in data.items()
            if key in cls.__table__.columns.keys()
        })
