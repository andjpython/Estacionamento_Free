"""
Modelos ORM do Sistema de Estacionamento Rotativo
"""
from db import Base
from .veiculo import Veiculo
from .vaga import Vaga
from .funcionario import Funcionario
from .historico import Historico

__all__ = ['Base', 'Veiculo', 'Vaga', 'Funcionario', 'Historico']