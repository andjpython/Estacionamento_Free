"""
Repositório de Histórico
"""
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from models import Historico
from .base_repo import BaseRepository

class HistoricoRepository(BaseRepository[Historico]):
    def __init__(self, session: Session):
        super().__init__(session, Historico)

    def get_by_placa(self, placa: str) -> List[Historico]:
        """Busca histórico por placa do veículo"""
        return (
            self.session.query(Historico)
            .filter(Historico.placa == placa)
            .order_by(Historico.data_evento.desc())
            .all()
        )

    def get_by_matricula(self, matricula: str) -> List[Historico]:
        """Busca histórico por matrícula do funcionário"""
        return (
            self.session.query(Historico)
            .filter(Historico.matricula == matricula)
            .order_by(Historico.data_evento.desc())
            .all()
        )

    def get_by_periodo(self, inicio: datetime, fim: datetime) -> List[Historico]:
        """Busca histórico por período"""
        return (
            self.session.query(Historico)
            .filter(Historico.data_evento.between(inicio, fim))
            .order_by(Historico.data_evento.desc())
            .all()
        )

    def create_from_dict(self, data: dict) -> Historico:
        """Cria um registro de histórico a partir de um dicionário"""
        historico = Historico(
            acao=data.get('acao'),
            placa=data.get('placa'),
            nome=data.get('nome'),
            tipo=data.get('tipo'),
            vaga_numero=data.get('vaga_numero'),
            tempo_min=data.get('tempo_min'),
            funcionario_nome=data.get('funcionario_nome'),
            matricula=data.get('matricula')
        )
        return self.create(historico)

    def registrar_entrada(
        self,
        placa: str,
        nome: str,
        tipo: str,
        vaga_numero: int,
        funcionario_nome: str,
        matricula: str
    ) -> Historico:
        """Registra entrada de veículo"""
        historico = Historico(
            acao="entrada",
            placa=placa,
            nome=nome,
            tipo=tipo,
            vaga_numero=vaga_numero,
            funcionario_nome=funcionario_nome,
            matricula=matricula
        )
        return self.create(historico)

    def registrar_saida(
        self,
        placa: str,
        nome: str,
        tipo: str,
        vaga_numero: int,
        tempo_min: int,
        funcionario_nome: str,
        matricula: str
    ) -> Historico:
        """Registra saída de veículo"""
        historico = Historico(
            acao="saida",
            placa=placa,
            nome=nome,
            tipo=tipo,
            vaga_numero=vaga_numero,
            tempo_min=tempo_min,
            funcionario_nome=funcionario_nome,
            matricula=matricula
        )
        return self.create(historico)
