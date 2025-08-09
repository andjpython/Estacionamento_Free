"""
Serviços para gerenciamento do histórico
"""
from sqlalchemy.orm import Session
from models import Historico
from repositories import HistoricoRepository

def ver_historico(db: Session) -> str:
    """Retorna o histórico completo de eventos"""
    repo = HistoricoRepository(db)
    historico = repo.get_all()
    
    if not historico:
        return "📭 Nenhum registro no histórico."
    
    return "\n".join([
        f"{h.data_evento}: {h.acao} - {h.placa} - {h.nome}"
        for h in historico
    ])

def filtrar_historico_por_matricula(db: Session, matricula: str) -> list:
    """Filtra o histórico por matrícula do funcionário"""
    repo = HistoricoRepository(db)
    return repo.get_by_matricula(matricula)

def registrar_entrada(
    db: Session,
    placa: str,
    nome: str,
    tipo: str,
    vaga_numero: int,
    funcionario_nome: str,
    matricula: str
) -> Historico:
    """Registra entrada de veículo no histórico"""
    repo = HistoricoRepository(db)
    return repo.registrar_entrada(
        placa=placa,
        nome=nome,
        tipo=tipo,
        vaga_numero=vaga_numero,
        funcionario_nome=funcionario_nome,
        matricula=matricula
    )

def registrar_saida(
    db: Session,
    placa: str,
    nome: str,
    tipo: str,
    vaga_numero: int,
    tempo_min: int,
    funcionario_nome: str,
    matricula: str
) -> Historico:
    """Registra saída de veículo no histórico"""
    repo = HistoricoRepository(db)
    return repo.registrar_saida(
        placa=placa,
        nome=nome,
        tipo=tipo,
        vaga_numero=vaga_numero,
        tempo_min=tempo_min,
        funcionario_nome=funcionario_nome,
        matricula=matricula
    )