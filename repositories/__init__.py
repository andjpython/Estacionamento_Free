"""
Repositórios do Sistema de Estacionamento Rotativo
"""
from .veiculo_repo import VeiculoRepository
from .vaga_repo import VagaRepository
from .funcionario_repo import FuncionarioRepository
from .historico_repo import HistoricoRepository

__all__ = [
    'VeiculoRepository',
    'VagaRepository',
    'FuncionarioRepository',
    'HistoricoRepository'
]
