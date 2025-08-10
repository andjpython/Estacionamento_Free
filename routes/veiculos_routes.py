from flask import Blueprint, request, jsonify
from datetime import datetime
import pytz

from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error
from db import SessionLocal
from repositories import VeiculoRepository, VagaRepository, FuncionarioRepository, HistoricoRepository
from services import veiculo_service, vaga_service
from services.veiculo_service import normalizar_placa
from routes.funcionarios_routes import funcionarios_logados

# Configurar logger
logger = setup_logger(__name__)

veiculos_bp = Blueprint('veiculos', __name__)

# Cadastro de veículo
@veiculos_bp.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        cpf = data.get('cpf', '').strip()
        modelo = data.get('modelo', '').strip()
        nome = data.get('nome', '').strip()
        bloco = data.get('bloco', '').strip()
        apartamento = data.get('apartamento', '').strip()
        matricula_func = data.get('matricula', '').strip()
        
        # Validações básicas
        if not placa or not cpf or not matricula_func or not nome:
            return jsonify({'mensagem': 'Placa, CPF, matrícula e nome são obrigatórios!'}), 400
            
        db = SessionLocal()
        try:
            funcionario_repo = FuncionarioRepository(db)
            historico_repo = HistoricoRepository(db)
            
            # Verificar se funcionário existe
            funcionario = funcionario_repo.get_by_matricula(matricula_func)
            if not funcionario:
                return jsonify({'mensagem': 'Funcionário não encontrado!'}), 403
                
            # Verificar se funcionário está logado
            if matricula_func not in funcionarios_logados:
                return jsonify({'mensagem': 'Funcionário precisa estar logado para cadastrar veículo!'}), 403
                
            # Cadastrar veículo
            resposta = veiculo_service.cadastrar_veiculo(
                db=db,
                placa=placa,
                cpf=cpf,
                modelo=modelo,
                nome=nome,
                bloco=bloco,
                apartamento=apartamento
            )
            
            # Se cadastro foi bem-sucedido, registrar no histórico
            if "✅" in resposta:
                historico_repo.create(
                    acao="cadastro_veiculo",
                    placa=normalizar_placa(placa),
                    nome=nome,
                    tipo="morador" if modelo else "visitante",
                    funcionario_nome=funcionario.nome,
                    matricula=matricula_func
                )
                
                logger.info(f"Veículo {normalizar_placa(placa)} cadastrado por {funcionario.nome}")
                
            return jsonify({'mensagem': resposta})
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao cadastrar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Listar veículos
@veiculos_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    try:
        db = SessionLocal()
        try:
            veiculos = veiculo_service.listar_veiculos_cadastrados(db)
            return jsonify([{
                'id': v.id,
                'placa': v.placa,
                'cpf': v.cpf,
                'nome': v.nome,
                'modelo': v.modelo,
                'tipo': v.tipo,
                'bloco': v.bloco,
                'apartamento': v.apartamento,
                'criado_em': v.criado_em.isoformat() if v.criado_em else None
            } for v in veiculos])
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Estacionar veículo
@veiculos_bp.route('/estacionar', methods=['POST'])
def estacionar():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not placa or not matricula:
            return jsonify({'mensagem': 'Placa e matrícula são obrigatórios!'}), 400
            
        db = SessionLocal()
        try:
            veiculo_repo = VeiculoRepository(db)
            funcionario_repo = FuncionarioRepository(db)
            
            # Verificar veículo e funcionário
            veiculo = veiculo_repo.get_by_placa(placa)
            funcionario = funcionario_repo.get_by_matricula(matricula)
            
            if not veiculo:
                return jsonify({'mensagem': '❌ Veículo não cadastrado. Faça o cadastro primeiro.'}), 404
            if not funcionario:
                return jsonify({'mensagem': '❌ Funcionário não cadastrado.'}), 403
            if matricula not in funcionarios_logados:
                return jsonify({'mensagem': '❌ Funcionário precisa estar logado.'}), 403
                
            from estacionamento import estacionar_veiculo
            resposta = estacionar_veiculo(db, placa)
            
            if "✅" in resposta:
                logger.info(f"Veículo {normalizar_placa(placa)} estacionado por {funcionario.nome}")
                
                # Buscar informações da vaga
                vaga_repo = VagaRepository(db)
                vaga = next(
                    (v for v in vaga_repo.get_vagas_ocupadas() if v.veiculo and v.veiculo.placa == placa),
                    None
                )
                
                proprietario = {
                    'cpf': veiculo.cpf,
                    'nome': veiculo.nome,
                    'bloco': veiculo.bloco,
                    'apartamento': veiculo.apartamento,
                    'hora_entrada': vaga.entrada.isoformat() if vaga and vaga.entrada else None
                }
                
                return jsonify({
                    'mensagem': resposta,
                    'proprietario': proprietario,
                    'vaga': vaga.numero if vaga else None
                })
            else:
                return jsonify({'mensagem': resposta}), 400
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao estacionar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Liberar veículo
@veiculos_bp.route('/liberar', methods=['POST'])
def liberar_veiculo():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not placa or not matricula:
            return jsonify({'mensagem': 'Placa e matrícula são obrigatórios!'}), 400
            
        db = SessionLocal()
        try:
            veiculo_repo = VeiculoRepository(db)
            funcionario_repo = FuncionarioRepository(db)
            
            # Verificar veículo e funcionário
            veiculo = veiculo_repo.get_by_placa(placa)
            funcionario = funcionario_repo.get_by_matricula(matricula)
            
            if not veiculo:
                return jsonify({'mensagem': '❌ Veículo não cadastrado.'}), 404
            if not funcionario:
                return jsonify({'mensagem': '❌ Funcionário não cadastrado.'}), 403
            if matricula not in funcionarios_logados:
                return jsonify({'mensagem': '❌ Funcionário precisa estar logado.'}), 403
                
            from estacionamento import liberar_vaga
            resposta = liberar_vaga(db, placa, matricula)
            
            if "✅" in resposta:
                logger.info(f"Veículo {normalizar_placa(placa)} liberado por {funcionario.nome}")
                
                # Buscar hora de saída no histórico
                historico_repo = HistoricoRepository(db)
                historico = historico_repo.get_by_placa(placa)
                saida = None
                for h in reversed(historico):
                    if h.acao == 'saida' and h.placa == placa:
                        saida = h.data_evento
                        break
                        
                proprietario = {
                    'cpf': veiculo.cpf,
                    'nome': veiculo.nome,
                    'bloco': veiculo.bloco,
                    'apartamento': veiculo.apartamento,
                    'hora_saida': saida.isoformat() if saida else None
                }
                
                return jsonify({'mensagem': resposta, 'proprietario': proprietario})
            else:
                return jsonify({'mensagem': resposta}), 400
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao liberar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Remover veículo por CPF
@veiculos_bp.route('/remover-veiculo-cpf', methods=['POST'])
def remover_veiculo_cpf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        cpf = data.get('cpf', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not cpf or not matricula:
            return jsonify({'mensagem': 'CPF e matrícula são obrigatórios!'}), 400
            
        db = SessionLocal()
        try:
            funcionario_repo = FuncionarioRepository(db)
            
            # Verificar se funcionário está logado
            if matricula not in funcionarios_logados:
                return jsonify({'mensagem': 'Funcionário precisa estar logado!'}), 403
                
            from estacionamento import remover_veiculo_por_cpf
            resposta = remover_veiculo_por_cpf(db, cpf, matricula)
            
            if "🗑️" in resposta:  # Remoção bem-sucedida
                funcionario = funcionario_repo.get_by_matricula(matricula)
                if funcionario:
                    logger.info(f"Veículo removido por CPF {cpf} por {funcionario.nome}")
                    
            return jsonify({'mensagem': resposta})
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao remover veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Histórico por matrícula
@veiculos_bp.route('/historico-matricula')
def historico_matricula():
    try:
        matricula = request.args.get('matricula', '').strip()
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        db = SessionLocal()
        try:
            historico_repo = HistoricoRepository(db)
            historico = historico_repo.get_by_matricula(matricula)
            
            return jsonify([{
                'id': h.id,
                'acao': h.acao,
                'placa': h.placa,
                'nome': h.nome,
                'tipo': h.tipo,
                'vaga_numero': h.vaga_numero,
                'tempo_min': h.tempo_min,
                'funcionario_nome': h.funcionario_nome,
                'matricula': h.matricula,
                'data_evento': h.data_evento.isoformat() if h.data_evento else None
            } for h in historico])
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Listar status das vagas
@veiculos_bp.route('/vagas', methods=['GET'])
def listar_vagas():
    try:
        db = SessionLocal()
        try:
            vaga_repo = VagaRepository(db)
            vagas = vaga_repo.get_vagas_completas()
            
            return jsonify([{
                'id': v.id,
                'numero': v.numero,
                'tipo': v.tipo,
                'ocupada': v.ocupada,
                'veiculo': v.veiculo.placa if v.veiculo else None,
                'entrada': v.entrada.isoformat() if v.entrada else None
            } for v in vagas])
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro ao listar vagas: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Verificar tempo excedido
@veiculos_bp.route('/tempo-excedido', methods=['GET'])
def tempo_excedido():
    try:
        db = SessionLocal()
        try:
            excedidos = vaga_service.verificar_tempo_excedido(db)
            
            if not excedidos:
                return jsonify({
                    'mensagem': '✅ Nenhuma vaga excedeu o tempo.',
                    'excedidos': [],
                    'veiculos_excedidos': []
                })
            else:
                mensagens = []
                veiculos_excedidos = []
                
                for excedido in excedidos:
                    mensagens.append(
                        f"⚠️ Vaga {excedido['numero']} com veículo {excedido['veiculo']} "
                        f"está há {excedido['horas']} horas!"
                    )
                    
                    # Buscar informações completas do veículo
                    veiculo_repo = VeiculoRepository(db)
                    veiculo = veiculo_repo.get_by_placa(excedido['veiculo'])
                    if veiculo:
                        veiculos_excedidos.append({
                            'placa': excedido['veiculo'],
                            'nome': veiculo.nome,
                            'vaga': excedido['numero'],
                            'tempo_excedido': excedido['horas'] * 60,  # Converter para minutos
                            'bloco': veiculo.bloco,
                            'apartamento': veiculo.apartamento
                        })
                
                return jsonify({
                    'mensagem': '\n'.join(mensagens),
                    'excedidos': excedidos,
                    'veiculos_excedidos': veiculos_excedidos
                })
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao verificar tempo excedido: {e}")
        return jsonify({
            'mensagem': f'Erro ao verificar tempo excedido: {str(e)}',
            'excedidos': [],
            'veiculos_excedidos': []
        }), 500