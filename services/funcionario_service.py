"""
Serviço para gerenciamento de funcionários
"""
from sqlalchemy.orm import Session
from models import Funcionario
from repositories import FuncionarioRepository, HistoricoRepository
from utils.state import funcionarios_logados

def cadastrar_funcionario(db: Session, nome: str, matricula: str) -> str:
    """Cadastra um novo funcionário"""
    funcionario_repo = FuncionarioRepository(db)
    
    # Verificar se matrícula já existe
    if funcionario_repo.get_by_matricula(matricula):
        return "❌ Matrícula já cadastrada!"
        
    # Criar funcionário
    funcionario = Funcionario(
        nome=nome,
        matricula=matricula,
        ativo=True
    )
    funcionario_repo.create(funcionario)
    
    return f"✅ Funcionário {nome} cadastrado com matrícula {matricula}."

def listar_funcionarios(db: Session) -> list:
    """Lista todos os funcionários"""
    funcionario_repo = FuncionarioRepository(db)
    return funcionario_repo.get_all()

def remover_funcionario(db: Session, matricula: str) -> str:
    """Remove completamente um funcionário do banco de dados"""
    funcionario_repo = FuncionarioRepository(db)
    historico_repo = HistoricoRepository(db)
    
    # Verificar se funcionário existe
    funcionario = funcionario_repo.get_by_matricula(matricula)
    if not funcionario:
        return "❌ Funcionário não encontrado!"
        
    # Se funcionário estiver logado, fazer logout
    if matricula in funcionarios_logados:
        funcionarios_logados.discard(matricula)
        
    # Registrar no histórico antes de remover
    historico_repo.create_from_dict({
        'acao': 'remocao_funcionario',
        'placa': 'N/A',
        'nome': funcionario.nome,
        'tipo': 'funcionario',
        'funcionario_nome': funcionario.nome,
        'matricula': matricula
    })
    
    # Remover funcionário completamente
    if funcionario_repo.remover_por_matricula(matricula):
        return f"✅ Funcionário {funcionario.nome} removido permanentemente!"
    else:
        return "❌ Erro ao remover funcionário!"