"""
Serviços para gerenciamento de funcionários
"""
from typing import List
from sqlalchemy.orm import Session
from config import active_config
from models import Funcionario
from repositories import FuncionarioRepository

def cadastrar_funcionario(db: Session, nome: str, matricula: str) -> str:
    """Cadastra um novo funcionário no sistema"""
    repo = FuncionarioRepository(db)
    
    if repo.get_by_matricula(matricula):
        return "❌ Matrícula já cadastrada."
    
    if not matricula or len(matricula) != 4 or not matricula.isdigit():
        return active_config.Mensagens.MATRICULA_INVALIDA
    
    if not nome:
        return "❌ Nome do funcionário é obrigatório."
    
    funcionario = Funcionario(
        nome=nome.strip(),
        matricula=matricula.strip(),
        ativo=True
    )
    repo.create(funcionario)
    
    return active_config.Mensagens.FUNCIONARIO_CADASTRADO.format(
        nome=nome,
        matricula=matricula
    )

def listar_funcionarios(db: Session) -> List[Funcionario]:
    """Lista todos os funcionários cadastrados"""
    repo = FuncionarioRepository(db)
    return repo.get_ativos()

def buscar_funcionario_por_matricula(db: Session, matricula: str) -> Funcionario:
    """Busca um funcionário pela matrícula"""
    repo = FuncionarioRepository(db)
    return repo.get_by_matricula(matricula)