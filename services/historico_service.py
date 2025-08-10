"""
Serviços para gerenciamento do histórico
"""
from sqlalchemy.orm import Session
from models import Historico
from repositories import HistoricoRepository

def ver_historico(db: Session, limit: int = 100) -> str:
    """Retorna o histórico completo de eventos, ordenado por data (mais recentes primeiro)"""
    repo = HistoricoRepository(db)
    historico = repo.get_all()
    
    if not historico:
        return "📭 Nenhum registro no histórico."
    
    # Ordenar por data (mais recentes primeiro) e limitar quantidade
    historico = sorted(historico, key=lambda h: h.data_evento, reverse=True)[:limit]
    
    # Emojis para cada tipo de ação
    emojis = {
        "entrada": "🅿️",
        "saida": "🚗",
        "login": "🔓",
        "logout": "🔒",
        "remocao_manual": "🗑️"
    }
    
    return "\n".join([
        f"{h.data_evento.strftime('%d/%m/%Y %H:%M:%S')}: " +
        f"{emojis.get(h.acao, '❓')} {h.acao.title()} - " +
        (f"Veículo: {h.placa}" if h.placa != "N/A" else "") +
        (f" - {h.nome}" if h.nome else "") +
        (f" ({h.tempo_min} min)" if h.tempo_min else "") +
        (f" - Por: {h.funcionario_nome}" if h.funcionario_nome != h.nome else "")
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