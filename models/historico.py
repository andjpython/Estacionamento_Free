"""
Modelo de Histórico
"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base_model import BaseModel

class Historico(BaseModel):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    acao = Column(String(50), nullable=False)  # entrada, saida, cadastro, etc
    placa = Column(String(7), nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)  # morador ou visitante
    vaga_numero = Column(Integer, nullable=True)
    tempo_min = Column(Integer, nullable=True)  # tempo de permanência em minutos
    funcionario_nome = Column(String(100), nullable=False)
    matricula = Column(String(4), nullable=False)
    data_evento = Column(DateTime(timezone=True), default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Historico(acao='{self.acao}', placa='{self.placa}', data='{self.data_evento}')>"
