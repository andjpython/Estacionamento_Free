"""
Repositório de Vagas
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from models import Vaga
from .base_repo import BaseRepository

class VagaRepository(BaseRepository[Vaga]):
    def __init__(self, session: Session):
        super().__init__(session, Vaga)

    def get_by_numero(self, numero: int) -> Optional[Vaga]:
        """Busca uma vaga pelo número"""
        return self.session.query(Vaga).filter(Vaga.numero == numero).first()

    def get_vagas_livres(self, tipo: str) -> List[Vaga]:
        """Busca vagas livres por tipo"""
        return (
            self.session.query(Vaga)
            .filter(Vaga.tipo == tipo, Vaga.ocupada == False)
            .order_by(Vaga.numero)
            .all()
        )

    def get_vagas_ocupadas(self) -> List[Vaga]:
        """Busca todas as vagas ocupadas"""
        return (
            self.session.query(Vaga)
            .filter(Vaga.ocupada == True)
            .order_by(Vaga.numero)
            .all()
        )

    def ocupar_vaga(self, vaga: Vaga, veiculo_id: int) -> Vaga:
        """Ocupa uma vaga com um veículo"""
        vaga.ocupada = True
        vaga.veiculo_id = veiculo_id
        vaga.entrada = datetime.now()
        self.session.commit()
        return vaga

    def liberar_vaga(self, vaga: Vaga) -> Vaga:
        """Libera uma vaga"""
        vaga.ocupada = False
        vaga.veiculo_id = None
        vaga.entrada = None
        self.session.commit()
        return vaga

    def get_vagas_completas(self) -> List[Vaga]:
        """Retorna todas as vagas com informações do veículo quando ocupadas"""
        return (
            self.session.query(Vaga)
            .order_by(Vaga.numero)
            .all()
        )
