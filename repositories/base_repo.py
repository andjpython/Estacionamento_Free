"""
Repositório base com operações comuns
"""
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from db import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        """Busca um registro pelo ID"""
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        """Retorna todos os registros"""
        return self.session.query(self.model).all()

    def create(self, obj: T) -> T:
        """Cria um novo registro"""
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        """Atualiza um registro existente"""
        self.session.merge(obj)
        self.session.commit()
        return obj

    def delete(self, id: int) -> bool:
        """Remove um registro pelo ID"""
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return True
        return False
