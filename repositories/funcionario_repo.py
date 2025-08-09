"""
Repositório de Funcionários
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Funcionario
from .base_repo import BaseRepository

class FuncionarioRepository(BaseRepository[Funcionario]):
    def __init__(self, session: Session):
        super().__init__(session, Funcionario)

    def get_by_matricula(self, matricula: str) -> Optional[Funcionario]:
        """Busca um funcionário pela matrícula"""
        return (
            self.session.query(Funcionario)
            .filter(Funcionario.matricula == matricula)
            .first()
        )

    def get_ativos(self) -> List[Funcionario]:
        """Retorna todos os funcionários ativos"""
        return (
            self.session.query(Funcionario)
            .filter(Funcionario.ativo == True)
            .all()
        )

    def desativar(self, matricula: str) -> bool:
        """Desativa um funcionário"""
        funcionario = self.get_by_matricula(matricula)
        if funcionario:
            funcionario.ativo = False
            self.session.commit()
            return True
        return False

    def reativar(self, matricula: str) -> bool:
        """Reativa um funcionário"""
        funcionario = self.get_by_matricula(matricula)
        if funcionario:
            funcionario.ativo = True
            self.session.commit()
            return True
        return False
