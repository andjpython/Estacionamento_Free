"""
Modelo de Veículo
"""
from sqlalchemy import Column, Integer, String, Boolean
from .base_model import BaseModel

class Veiculo(BaseModel):
    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True)
    placa = Column(String(7), unique=True, nullable=False, index=True)
    cpf = Column(String(11), nullable=False)
    nome = Column(String(100), nullable=False)
    modelo = Column(String(50), nullable=True)
    tipo = Column(String(20), nullable=False)  # morador ou visitante
    bloco = Column(String(10))
    apartamento = Column(String(10))

    def __repr__(self):
        return f"<Veiculo(placa='{self.placa}', nome='{self.nome}')>"
