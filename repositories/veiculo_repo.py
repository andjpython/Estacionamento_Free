"""
Repositório de Veículos
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Veiculo
from .base_repo import BaseRepository

class VeiculoRepository(BaseRepository[Veiculo]):
    def __init__(self, session: Session):
        super().__init__(session, Veiculo)

    def get_by_placa(self, placa: str) -> Optional[Veiculo]:
        """Busca um veículo pela placa"""
        return self.session.query(Veiculo).filter(Veiculo.placa == placa).first()

    def get_by_cpf(self, cpf: str) -> List[Veiculo]:
        """Busca veículos pelo CPF do proprietário"""
        return self.session.query(Veiculo).filter(Veiculo.cpf == cpf).all()

    def get_by_tipo(self, tipo: str) -> List[Veiculo]:
        """Busca veículos por tipo (morador/visitante)"""
        return self.session.query(Veiculo).filter(Veiculo.tipo == tipo).all()

    def get_by_bloco(self, bloco: str) -> List[Veiculo]:
        """Busca veículos por bloco"""
        return self.session.query(Veiculo).filter(Veiculo.bloco == bloco).all()
