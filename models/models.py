"""
Modelos do sistema de estacionamento
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timedelta
import enum
import pytz
from models.base import ModelBase, Base

class TipoVaga(enum.Enum):
    """Tipos de vaga disponíveis"""
    COMUM = "comum"
    VISITANTE = "visitante"

class StatusVeiculo(enum.Enum):
    """Status possíveis para um veículo"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    BLOQUEADO = "bloqueado"

class Veiculo(ModelBase, Base):
    """Modelo para veículos"""
    __tablename__ = 'veiculos'
    
    id = Column(Integer, primary_key=True)
    placa = Column(String(7), unique=True, nullable=False)
    modelo = Column(String(50), nullable=False)
    proprietario = Column(String(100), nullable=False)
    cpf = Column(String(11), nullable=False)
    bloco = Column(String(10), nullable=False)
    apartamento = Column(String(10), nullable=False)
    status = Column(Enum(StatusVeiculo), default=StatusVeiculo.ATIVO)
    
    # Relacionamentos
    ocupacoes = relationship("Ocupacao", back_populates="veiculo")
    
    __table_args__ = (
        CheckConstraint('length(placa) = 7', name='check_placa_length'),
        CheckConstraint('length(cpf) = 11', name='check_cpf_length'),
    )

class Vaga(ModelBase, Base):
    """Modelo para vagas"""
    __tablename__ = 'vagas'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, unique=True, nullable=False)
    tipo = Column(Enum(TipoVaga), nullable=False)
    ocupada = Column(Boolean, default=False)
    
    # Relacionamentos
    ocupacao_atual = relationship(
        "Ocupacao",
        back_populates="vaga",
        uselist=False,
        primaryjoin="and_(Vaga.id==Ocupacao.vaga_id, Ocupacao.saida==None)"
    )
    
    @hybrid_property
    def disponivel(self):
        """Verifica se a vaga está disponível"""
        return not self.ocupada

class Ocupacao(ModelBase, Base):
    """Modelo para registro de ocupação de vagas"""
    __tablename__ = 'ocupacoes'
    
    id = Column(Integer, primary_key=True)
    vaga_id = Column(Integer, ForeignKey('vagas.id'), nullable=False)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=False)
    entrada = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(pytz.UTC))
    saida = Column(DateTime(timezone=True))
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=False)
    
    # Relacionamentos
    vaga = relationship("Vaga", back_populates="ocupacao_atual")
    veiculo = relationship("Veiculo", back_populates="ocupacoes")
    funcionario = relationship("Funcionario", back_populates="ocupacoes")
    
    @hybrid_property
    def duracao(self):
        """Calcula duração da ocupação"""
        if not self.saida:
            return datetime.now(pytz.UTC) - self.entrada
        return self.saida - self.entrada
    
    @hybrid_property
    def tempo_excedido(self):
        """Verifica se o tempo foi excedido (72h)"""
        limite = timedelta(hours=72)
        return self.duracao > limite

class Funcionario(ModelBase, Base):
    """Modelo para funcionários"""
    __tablename__ = 'funcionarios'
    
    id = Column(Integer, primary_key=True)
    matricula = Column(String(4), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True)
    ultimo_login = Column(DateTime(timezone=True))
    
    # Relacionamentos
    ocupacoes = relationship("Ocupacao", back_populates="funcionario")
    
    __table_args__ = (
        CheckConstraint('length(matricula) = 4', name='check_matricula_length'),
    )
