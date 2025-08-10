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

def listar_funcionarios(db: Session) -> str:
    """Lista todos os funcionários cadastrados"""
    repo = FuncionarioRepository(db)
    funcionarios = sorted(repo.get_all(), key=lambda f: f.nome)
    
    if not funcionarios:
        return active_config.Mensagens.NENHUM_FUNCIONARIO_CADASTRADO
    
    return "\n".join([
        f"👤 {f.nome} - Matrícula: {f.matricula}" +
        (" (inativo)" if not f.ativo else "")
        for f in funcionarios
    ])

def buscar_funcionario_por_matricula(db: Session, matricula: str) -> Funcionario:
    """Busca um funcionário pela matrícula"""
    repo = FuncionarioRepository(db)
    return repo.get_by_matricula(matricula)

def remover_funcionario(db: Session, matricula: str) -> str:
    """Remove um funcionário do sistema"""
    repo = FuncionarioRepository(db)
    funcionario = repo.get_by_matricula(matricula)
    
    if not funcionario:
        return "❌ Funcionário não encontrado."
    
    funcionario.ativo = False
    repo.update(funcionario)
    
    return f"🗑️ Funcionário {funcionario.nome} removido."