"""
Modelo de Vaga
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel

class Vaga(BaseModel):
    __tablename__ = 'vagas'

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False, index=True)
    tipo = Column(String(20), nullable=False)  # comum ou visitante
    ocupada = Column(Boolean, default=False, nullable=False)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=True)
    entrada = Column(DateTime(timezone=True), nullable=True)

    # Relacionamento com Veículo
    veiculo = relationship("Veiculo", backref="vaga_atual", uselist=False)

    def __repr__(self):
        status = "ocupada" if self.ocupada else "livre"
        return f"<Vaga(numero={self.numero}, tipo='{self.tipo}', status='{status}')>"
