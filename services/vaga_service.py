"""
Serviço de gerenciamento de vagas
"""
from datetime import datetime
import pytz
from sqlalchemy.orm import Session
from config import active_config
from models import Vaga
from repositories import VagaRepository
from utils.logging_config import setup_logger, log_error

# Configurar logger
logger = setup_logger(__name__)

# === Listar status das vagas ===
def ver_status_vagas(db: Session) -> str:
    """Retorna o status atual de todas as vagas"""
    repo = VagaRepository(db)
    vagas = repo.get_vagas_completas()
    
    if not vagas:
        return active_config.Mensagens.NENHUMA_VAGA_CADASTRADA
    
    status = ["📋 STATUS DAS VAGAS:"]
    for v in vagas:
        if v.ocupada and v.veiculo:
            s = f"🔴 Ocupada por {v.veiculo.placa}"
        else:
            s = "🟢 Livre"
        status.append(f"Vaga {v.numero} ({v.tipo}): {s}")
    
    return "\n".join(status)

# === Verificar tempo excedido ===
def verificar_tempo_excedido(db: Session, limite_horas: int = None) -> list:
    """Verifica quais veículos excederam o tempo limite de estacionamento"""
    try:
        if limite_horas is None:
            limite_horas = active_config.LIMITE_HORAS_ESTACIONAMENTO
            
        agora = datetime.now(pytz.timezone(active_config.TIMEZONE))
        excedidos = []
        
        repo = VagaRepository(db)
        vagas_ocupadas = repo.get_vagas_ocupadas()
        
        for v in vagas_ocupadas:
            if v.entrada:
                try:
                    horas = (agora - v.entrada).total_seconds() / 3600
                    
                    if horas > limite_horas:
                        excedidos.append({
                            'numero': v.numero,
                            'tipo': v.tipo,
                            'veiculo': v.veiculo.placa if v.veiculo else "Desconhecido",
                            'horas': round(horas, 1)
                        })
                        
                except (ValueError, TypeError) as e:
                    logger.warning(f"Erro ao processar data de entrada da vaga {v.numero}: {e}")
                    continue
                except Exception as e:
                    log_error(logger, e, f"processamento da vaga {v.numero}")
                    continue
        
        return excedidos
        
    except Exception as e:
        log_error(logger, e, "verificação de tempo excedido")
        return []