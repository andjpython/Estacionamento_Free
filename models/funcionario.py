"""
Modelo de Funcionário
"""
from sqlalchemy import Column, Integer, String, Boolean
from .base_model import BaseModel

class Funcionario(BaseModel):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(4), unique=True, nullable=False, index=True)
    ativo = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        status = "ativo" if self.ativo else "inativo"
        return f"<Funcionario(matricula='{self.matricula}', nome='{self.nome}', status='{status}')>"
