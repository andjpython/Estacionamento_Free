"""
Lógica de negócio principal do Sistema de Estacionamento Rotativo
"""
import json
from datetime import datetime
import pytz
from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error

# Configurar logger
logger = setup_logger(__name__)

def inicializar_arquivos():
    """Inicializa os arquivos de dados JSON se não existirem"""
    try:
        active_config.DADOS_DIR.mkdir(exist_ok=True)
        
        # Inicializar arquivo de veículos
        if not active_config.VEICULOS_PATH.exists():
            with open(active_config.VEICULOS_PATH, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
                
        # Inicializar arquivo de vagas
        if not active_config.VAGAS_PATH.exists():
            vagas = [
                {"numero": i + 1, "tipo": "comum", "ocupada": False, "veiculo": None, "entrada": None}
                for i in range(active_config.VAGAS_COMUNS)
            ] + [
                {"numero": i + active_config.VAGAS_COMUNS + 1, "tipo": "visitante", "ocupada": False, "veiculo": None, "entrada": None}
                for i in range(active_config.VAGAS_VISITANTES)
            ]
            with open(active_config.VAGAS_PATH, "w", encoding='utf-8') as f:
                json.dump(vagas, f, ensure_ascii=False, indent=4)
                
        # Inicializar arquivo de histórico
        if not active_config.HISTORICO_PATH.exists():
            with open(active_config.HISTORICO_PATH, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
                
        # Inicializar arquivo de funcionários
        if not active_config.FUNCIONARIOS_PATH.exists():
            with open(active_config.FUNCIONARIOS_PATH, "w", encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
                
        log_operation(logger, "Arquivos de dados inicializados com sucesso")
        
    except Exception as e:
        log_error(logger, e, "inicialização de arquivos")
        raise

def carregar_dados():
    """Carrega todos os dados dos arquivos JSON"""
    try:
        inicializar_arquivos()
        
        with open(active_config.VEICULOS_PATH, 'r', encoding='utf-8') as f:
            veiculos = json.load(f)
        with open(active_config.VAGAS_PATH, 'r', encoding='utf-8') as f:
            vagas = json.load(f)
        with open(active_config.HISTORICO_PATH, 'r', encoding='utf-8') as f:
            historico = json.load(f)
        with open(active_config.FUNCIONARIOS_PATH, 'r', encoding='utf-8') as f:
            funcionarios = json.load(f)
            
        return veiculos, vagas, historico, funcionarios
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_error(logger, e, "carregamento de dados")
        # Retorna dados vazios se houver erro
        return [], [], [], []
    except Exception as e:
        log_error(logger, e, "carregamento de dados (erro inesperado)")
        return [], [], [], []

def salvar_dados(veiculos, vagas, historico, funcionarios):
    """Salva todos os dados nos arquivos JSON"""
    try:
        with open(active_config.VEICULOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(veiculos, f, indent=4, ensure_ascii=False)
        with open(active_config.VAGAS_PATH, 'w', encoding='utf-8') as f:
            json.dump(vagas, f, indent=4, default=str, ensure_ascii=False)
        with open(active_config.HISTORICO_PATH, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=4, default=str, ensure_ascii=False)
        with open(active_config.FUNCIONARIOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(funcionarios, f, indent=4, ensure_ascii=False)
            
        logger.debug("Dados salvos com sucesso")
        
    except Exception as e:
        log_error(logger, e, "salvamento de dados")
        raise

def normalizar_placa(placa):
    """Normaliza placa removendo espaços e convertendo para maiúscula"""
    if not placa:
        return ""
    return placa.replace(" ", "").upper().strip()

def estacionar_veiculo(placa, veiculos, vagas, historico):
    """Estaciona um veículo em uma vaga disponível"""
    try:
        placa = normalizar_placa(placa)
        veiculo = next((v for v in veiculos if v['placa'] == placa), None)
        
        if not veiculo:
            return active_config.Mensagens.VEICULO_NAO_CADASTRADO
            
        if any(v['veiculo'] == placa for v in vagas if v['ocupada']):
            return active_config.Mensagens.VEICULO_JA_ESTACIONADO
            
        tipo_vaga = "comum" if veiculo["tipo"] == "morador" else "visitante"
        
        for vaga in vagas:
            if not vaga["ocupada"] and vaga["tipo"] == tipo_vaga:
                vaga["ocupada"] = True
                vaga["veiculo"] = placa
                vaga["entrada"] = datetime.now(pytz.timezone(active_config.TIMEZONE)).isoformat()
                
                historico.append({
                    "acao": "entrada_veiculo",
                    "placa": placa,
                    "nome": veiculo["nome"],
                    "tipo": veiculo["tipo"],
                    "vaga": vaga["numero"],
                    "data": vaga["entrada"]
                })
                
                log_operation(logger, f"Veículo {placa} estacionado na vaga {vaga['numero']}")
                return active_config.Mensagens.VEICULO_ESTACIONADO.format(
                    placa=placa, numero=vaga["numero"], tipo=tipo_vaga
                )
                
        return active_config.Mensagens.VAGA_NAO_DISPONIVEL.format(tipo=tipo_vaga)
        
    except Exception as e:
        log_error(logger, e, f"estacionamento do veículo {placa}")
        return active_config.Mensagens.ERRO_INTERNO

def estacionar_veiculo_por_dados(placa, veiculos, vagas, historico):
    """Estaciona veículo apenas por placa (compatibilidade)"""
    placa = normalizar_placa(placa)
    veiculo = next((v for v in veiculos if v['placa'] == placa), None)
    
    if not veiculo:
        return "❌ Veículo não cadastrado. Faça o cadastro primeiro."
        
    return estacionar_veiculo(placa, veiculos, vagas, historico)

def liberar_vaga(placa, matricula, veiculos, vagas, historico, funcionarios):
    """Libera uma vaga ocupada por um veículo"""
    try:
        placa = normalizar_placa(placa)
        vaga = next((v for v in vagas if v["ocupada"] and v["veiculo"] == placa), None)
        veiculo = next((v for v in veiculos if v["placa"] == placa), None)
        funcionario = next((f for f in funcionarios if f["matricula"] == matricula), None)
        
        if not vaga:
            return "❌ Veículo não encontrado em nenhuma vaga ocupada."
        if not veiculo:
            return active_config.Mensagens.VEICULO_NAO_CADASTRADO
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
            
        try:
            entrada = datetime.fromisoformat(vaga["entrada"])
            saida = datetime.now(pytz.timezone(active_config.TIMEZONE))
            tempo = (saida - entrada).total_seconds() / 60
        except (ValueError, TypeError) as e:
            logger.warning(f"Erro ao processar data de entrada para vaga {vaga['numero']}: {e}")
            tempo = 0
            
        historico.append({
            "acao": "saida_veiculo",
            "placa": placa,
            "nome": veiculo["nome"],
            "vaga": vaga["numero"],
            "tempo_min": round(tempo),
            "funcionario": funcionario["nome"],
            "matricula": matricula,
            "data_saida": saida.isoformat()
        })
        
        vaga["ocupada"] = False
        vaga["veiculo"] = None
        vaga["entrada"] = None
        
        log_operation(logger, f"Veículo {placa} liberado da vaga {vaga['numero']} por {funcionario['nome']}")
        return active_config.Mensagens.VEICULO_LIBERADO.format(
            placa=placa, numero=vaga["numero"], tempo=round(tempo)
        )
        
    except Exception as e:
        log_error(logger, e, f"liberação de vaga para veículo {placa}")
        return active_config.Mensagens.ERRO_INTERNO

def remover_veiculo_por_cpf(cpf, matricula, veiculos, vagas, historico, funcionarios):
    """Remove um veículo do sistema baseado no CPF"""
    try:
        from services.veiculo_service import normalizar_cpf
        
        cpf_normalizado = normalizar_cpf(cpf)
        
        veiculo = next((v for v in veiculos if normalizar_cpf(v["cpf"]) == cpf_normalizado), None)
        funcionario = next((f for f in funcionarios if f["matricula"] == matricula), None)
        
        if not veiculo:
            return "❌ Nenhum veículo encontrado com este CPF."
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
            
        placa = veiculo["placa"]
        vaga = next((v for v in vagas if v["ocupada"] and v["veiculo"] == placa), None)
        
        # Liberar vaga se estiver ocupada
        if vaga:
            vaga["ocupada"] = False
            vaga["veiculo"] = None
            vaga["entrada"] = None
            
        veiculos.remove(veiculo)
        
        historico.append({
            "acao": "remocao_manual",
            "placa": placa,
            "cpf": cpf_normalizado,
            "funcionario": funcionario["nome"],
            "matricula": matricula,
            "data": datetime.now(pytz.timezone(active_config.TIMEZONE)).isoformat()
        })
        
        log_operation(logger, f"Veículo {placa} removido por CPF {cpf_normalizado} por {funcionario['nome']}")
        return f"🗑️ Veículo {placa} removido por {funcionario['nome']}."
        
    except Exception as e:
        log_error(logger, e, f"remoção de veículo por CPF {cpf}")
        return active_config.Mensagens.ERRO_INTERNO

def registrar_entrada(matricula, funcionarios, historico):
    """Registra a entrada (login) de um funcionário"""
    try:
        funcionario = next((f for f in funcionarios if f['matricula'] == matricula), None)
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
            
        historico.append({
            "acao": "login",
            "matricula": matricula,
            "nome": funcionario['nome'],
            "data": datetime.now(pytz.timezone(active_config.TIMEZONE)).isoformat()
        })
        
        log_operation(logger, f"Login registrado para funcionário {funcionario['nome']}")
        return active_config.Mensagens.LOGIN_REALIZADO.format(nome=funcionario['nome'])
        
    except Exception as e:
        log_error(logger, e, f"registro de entrada do funcionário {matricula}")
        return active_config.Mensagens.ERRO_INTERNO

def registrar_saida(matricula, funcionarios, historico):
    """Registra a saída (logout) de um funcionário"""
    try:
        funcionario = next((f for f in funcionarios if f['matricula'] == matricula), None)
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
            
        historico.append({
            "acao": "logout",
            "matricula": matricula,
            "nome": funcionario['nome'],
            "data": datetime.now(pytz.timezone(active_config.TIMEZONE)).isoformat()
        })
        
        log_operation(logger, f"Logout registrado para funcionário {funcionario['nome']}")
        return active_config.Mensagens.LOGOUT_REALIZADO.format(nome=funcionario['nome'])
        
    except Exception as e:
        log_error(logger, e, f"registro de saída do funcionário {matricula}")
        return active_config.Mensagens.ERRO_INTERNO
