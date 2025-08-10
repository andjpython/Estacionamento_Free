"""
Lógica de negócio principal do Sistema de Estacionamento Rotativo
"""
from datetime import datetime
import pytz
from sqlalchemy.orm import Session
from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error
from models import Veiculo, Vaga, Funcionario
from repositories import VeiculoRepository, VagaRepository, FuncionarioRepository, HistoricoRepository
from services.veiculo_service import normalizar_placa

# Configurar logger
logger = setup_logger(__name__)

def estacionar_veiculo(db: Session, placa: str) -> str:
    """Estaciona um veículo em uma vaga disponível"""
    try:
        placa = normalizar_placa(placa)
        veiculo_repo = VeiculoRepository(db)
        vaga_repo = VagaRepository(db)
        historico_repo = HistoricoRepository(db)
        
        veiculo = veiculo_repo.get_by_placa(placa)
        if not veiculo:
            return active_config.Mensagens.VEICULO_NAO_CADASTRADO
        
        # Verificar se já está estacionado
        vagas_ocupadas = vaga_repo.get_vagas_ocupadas()
        if any(bool(v.veiculo) and v.veiculo.placa == placa for v in vagas_ocupadas):
            return active_config.Mensagens.VEICULO_JA_ESTACIONADO
        
        tipo_vaga = "comum" if str(veiculo.tipo) == "morador" else "visitante"
        vagas_livres = vaga_repo.get_vagas_livres(tipo_vaga)
        
        if not vagas_livres:
            return active_config.Mensagens.VAGA_NAO_DISPONIVEL.format(tipo=tipo_vaga)
        
        vaga = vagas_livres[0]  # Pega a primeira vaga livre
        vaga_repo.ocupar_vaga(vaga, veiculo.id)
        
        # Registrar no histórico
        historico_repo.registrar_entrada(
            placa=placa,
            nome=str(veiculo.nome),
            tipo=str(veiculo.tipo),
            vaga_numero=vaga.numero,
            funcionario_nome="Sistema",  # TODO: Passar funcionário
            matricula="0000"  # TODO: Passar matrícula
        )
        
        log_operation(logger, f"Veículo {placa} estacionado na vaga {vaga.numero}")
        return active_config.Mensagens.VEICULO_ESTACIONADO.format(
            placa=placa,
            numero=vaga.numero,
            tipo=tipo_vaga
        )
        
    except Exception as e:
        log_error(logger, e, f"estacionamento do veículo {placa}")
        return active_config.Mensagens.ERRO_INTERNO

def estacionar_veiculo_por_dados(db: Session, placa: str) -> str:
    """Estaciona veículo apenas por placa (compatibilidade)"""
    placa = normalizar_placa(placa)
    veiculo_repo = VeiculoRepository(db)
    veiculo = veiculo_repo.get_by_placa(placa)
    
    if not veiculo:
        return "❌ Veículo não cadastrado. Faça o cadastro primeiro."
    
    return estacionar_veiculo(db, placa)

def liberar_vaga(db: Session, placa: str, matricula: str) -> str:
    """Libera uma vaga ocupada por um veículo"""
    try:
        placa = normalizar_placa(placa)
        veiculo_repo = VeiculoRepository(db)
        vaga_repo = VagaRepository(db)
        funcionario_repo = FuncionarioRepository(db)
        historico_repo = HistoricoRepository(db)
        
        veiculo = veiculo_repo.get_by_placa(placa)
        funcionario = funcionario_repo.get_by_matricula(matricula)
        
        if not veiculo:
            return active_config.Mensagens.VEICULO_NAO_CADASTRADO
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
        
        # Buscar vaga ocupada pelo veículo
        vagas_ocupadas = vaga_repo.get_vagas_ocupadas()
        vaga = next((v for v in vagas_ocupadas if v.veiculo and v.veiculo.placa == placa), None)
        
        if not vaga:
            return "❌ Veículo não encontrado em nenhuma vaga ocupada."
        
        try:
            tempo = int((datetime.now(pytz.timezone(active_config.TIMEZONE)) - vaga.entrada).total_seconds() / 60)
        except (ValueError, TypeError) as e:
            logger.warning(f"Erro ao processar data de entrada para vaga {vaga.numero}: {e}")
            tempo = 0
        
        # Registrar saída no histórico
        historico_repo.registrar_saida(
            placa=placa,
            nome=str(veiculo.nome),
            tipo=str(veiculo.tipo),
            vaga_numero=vaga.numero,
            tempo_min=tempo,
            funcionario_nome=str(funcionario.nome),
            matricula=matricula
        )
        
        # Liberar a vaga
        vaga_repo.liberar_vaga(vaga)
        
        log_operation(logger, f"Veículo {placa} liberado da vaga {vaga.numero} por {funcionario.nome}")
        return active_config.Mensagens.VEICULO_LIBERADO.format(
            placa=placa,
            numero=vaga.numero,
            tempo=tempo
        )
        
    except Exception as e:
        log_error(logger, e, f"liberação de vaga para veículo {placa}")
        return active_config.Mensagens.ERRO_INTERNO

def remover_veiculo_por_cpf(db: Session, cpf: str, matricula: str) -> str:
    """Remove um veículo do sistema baseado no CPF"""
    try:
        from services.veiculo_service import normalizar_cpf
        
        cpf_normalizado = normalizar_cpf(cpf)
        veiculo_repo = VeiculoRepository(db)
        vaga_repo = VagaRepository(db)
        funcionario_repo = FuncionarioRepository(db)
        historico_repo = HistoricoRepository(db)
        
        veiculos = veiculo_repo.get_by_cpf(cpf_normalizado)
        funcionario = funcionario_repo.get_by_matricula(matricula)
        
        if not veiculos:
            return "❌ Nenhum veículo encontrado com este CPF."
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
        
        for veiculo in veiculos:
            # Verificar se está estacionado
            vagas_ocupadas = vaga_repo.get_vagas_ocupadas()
            vaga = next((v for v in vagas_ocupadas if v.veiculo and v.veiculo.id == veiculo.id), None)
            
            # Liberar vaga se estiver ocupada
            if vaga:
                vaga_repo.liberar_vaga(vaga)
            
            # Registrar no histórico
            historico_repo.create_from_dict({
                'acao': "remocao_manual",
                'placa': veiculo.placa,
                'nome': str(veiculo.nome),
                'tipo': str(veiculo.tipo),
                'funcionario_nome': str(funcionario.nome),
                'matricula': matricula
            })
            
            # Remover veículo
            veiculo_repo.delete(veiculo.id)
            
            log_operation(logger, f"Veículo {veiculo.placa} removido por CPF {cpf_normalizado} por {funcionario.nome}")
        
        return f"🗑️ Veículo(s) removido(s) por {funcionario.nome}."
        
    except Exception as e:
        log_error(logger, e, f"remoção de veículo por CPF {cpf}")
        return active_config.Mensagens.ERRO_INTERNO

def registrar_entrada(db: Session, matricula: str) -> str:
    """Registra a entrada (login) de um funcionário"""
    try:
        funcionario_repo = FuncionarioRepository(db)
        historico_repo = HistoricoRepository(db)
        
        funcionario = funcionario_repo.get_by_matricula(matricula)
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
        
        historico_repo.create_from_dict({
            'acao': "login",
            'placa': "N/A",
            'nome': str(funcionario.nome),
            'tipo': "funcionario",
            'funcionario_nome': str(funcionario.nome),
            'matricula': matricula
        })
        
        log_operation(logger, f"Login registrado para funcionário {funcionario.nome}")
        return active_config.Mensagens.LOGIN_REALIZADO.format(nome=funcionario.nome)
        
    except Exception as e:
        log_error(logger, e, f"registro de entrada do funcionário {matricula}")
        return active_config.Mensagens.ERRO_INTERNO

def registrar_saida(db: Session, matricula: str) -> str:
    """Registra a saída (logout) de um funcionário"""
    try:
        funcionario_repo = FuncionarioRepository(db)
        historico_repo = HistoricoRepository(db)
        
        funcionario = funcionario_repo.get_by_matricula(matricula)
        if not funcionario:
            return active_config.Mensagens.FUNCIONARIO_NAO_ENCONTRADO
        
        historico_repo.create_from_dict({
            'acao': "logout",
            'placa': "N/A",
            'nome': str(funcionario.nome),
            'tipo': "funcionario",
            'funcionario_nome': str(funcionario.nome),
            'matricula': matricula
        })
        
        log_operation(logger, f"Logout registrado para funcionário {funcionario.nome}")
        return active_config.Mensagens.LOGOUT_REALIZADO.format(nome=funcionario.nome)
        
    except Exception as e:
        log_error(logger, e, f"registro de saída do funcionário {matricula}")
        return active_config.Mensagens.ERRO_INTERNO