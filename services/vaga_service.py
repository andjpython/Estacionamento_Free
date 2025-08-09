from datetime import datetime
import pytz
from config import active_config
from utils.logging_config import setup_logger, log_error

# Configurar logger
logger = setup_logger(__name__)

# === Listar status das vagas ===
def ver_status_vagas(vagas):
    """Retorna o status atual de todas as vagas"""
    if not vagas:
        return active_config.Mensagens.NENHUMA_VAGA_CADASTRADA
    
    status = ["📋 STATUS DAS VAGAS:"]
    for v in vagas:
        s = "🟢 Livre" if not v["ocupada"] else f"🔴 Ocupada por {v['veiculo']}"
        status.append(f"Vaga {v['numero']} ({v['tipo']}): {s}")
    
    return "\n".join(status)

# === Verificar tempo excedido ===
def verificar_tempo_excedido(vagas, limite_horas=None):
    """Verifica quais veículos excederam o tempo limite de estacionamento"""
    try:
        if limite_horas is None:
            limite_horas = active_config.LIMITE_HORAS_ESTACIONAMENTO
            
        agora = datetime.now(pytz.timezone(active_config.TIMEZONE))
        excedidos = []
        
        for v in vagas:
            if v['ocupada'] and v['entrada']:
                try:
                    entrada = datetime.fromisoformat(v['entrada'])
                    horas = (agora - entrada).total_seconds() / 3600
                    
                    if horas > limite_horas:
                        excedidos.append({
                            'numero': v['numero'],
                            'tipo': v['tipo'],
                            'veiculo': v['veiculo'],
                            'horas': round(horas, 1)
                        })
                        
                except (ValueError, TypeError) as e:
                    logger.warning(f"Erro ao processar data de entrada da vaga {v.get('numero', '?')}: {e}")
                    continue
                except Exception as e:
                    log_error(logger, e, f"processamento da vaga {v.get('numero', '?')}")
                    continue
        
        return excedidos
        
    except Exception as e:
        log_error(logger, e, "verificação de tempo excedido")
        return [] 