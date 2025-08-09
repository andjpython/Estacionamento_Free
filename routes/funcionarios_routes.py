from flask import Blueprint, request, jsonify
from services.funcionario_service import cadastrar_funcionario, listar_funcionarios, buscar_funcionario_por_matricula
from estacionamento import carregar_dados, salvar_dados, registrar_entrada, registrar_saida
from datetime import datetime
import pytz
import os
from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error

# Configurar logger
logger = setup_logger(__name__)

funcionarios_bp = Blueprint('funcionarios', __name__)

# Controle de funcionários logados (thread-safe)
funcionarios_logados = set()

# Cadastro de funcionário
@funcionarios_bp.route('/cadastrar-funcionario', methods=['POST'])
def cadastrar_funcionario_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        nome = data.get('nome', '').strip()
        matricula = data.get('matricula', '').strip()
        senha = data.get('senha_supervisor', '')
        senha_master = active_config.SENHA_SUPERVISOR
        
        if not nome or not matricula:
            return jsonify({'mensagem': active_config.Mensagens.DADOS_NAO_FORNECIDOS}), 400
            
        if senha != senha_master:
            return jsonify({'mensagem': active_config.Mensagens.SENHA_INCORRETA}), 403
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        resposta = cadastrar_funcionario(funcionarios, nome, matricula)
        
        if "✅" in resposta:  # Cadastro bem-sucedido
            salvar_dados(veiculos, vagas, historico, funcionarios)
            log_operation(logger, f"Funcionário {nome} cadastrado com matrícula {matricula}")
            
        return jsonify({'mensagem': resposta})
        
    except Exception as e:
        log_error(logger, e, "cadastro de funcionário")
        return jsonify({'mensagem': active_config.Mensagens.ERRO_INTERNO}), 500

# Listar funcionários
@funcionarios_bp.route('/funcionarios', methods=['GET'])
def listar_funcionarios_route():
    try:
        senha = request.args.get('senha_supervisor', '')
        senha_master = active_config.SENHA_SUPERVISOR
        
        if senha != senha_master:
            return jsonify({'mensagem': 'Acesso negado. Senha incorreta!'}), 403
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        return jsonify(funcionarios)
        
    except Exception as e:
        logger.error(f"Erro ao listar funcionários: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Login funcionário
@funcionarios_bp.route('/login-funcionario', methods=['POST'])
def login_funcionario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        matricula = str(data.get('matricula', '')).strip()
        
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        funcionario = next((f for f in funcionarios if str(f['matricula']).strip() == matricula), None)
        
        if not funcionario:
            return jsonify({'mensagem': 'Matrícula não encontrada!'}), 404
            
        if matricula in funcionarios_logados:
            return jsonify({'mensagem': f'Funcionário {funcionario["nome"]} já está logado!'}), 200
            
        # Registrar login
        funcionarios_logados.add(matricula)
        registrar_entrada(matricula, funcionarios, historico)
        salvar_dados(veiculos, vagas, historico, funcionarios)
        
        logger.info(f"Funcionário {funcionario['nome']} (matrícula {matricula}) fez login")
        return jsonify({'mensagem': f'Funcionário {funcionario["nome"]} logado com sucesso!'}), 200
        
    except Exception as e:
        logger.error(f"Erro no login do funcionário: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Logout funcionário
@funcionarios_bp.route('/logout-funcionario', methods=['POST'])
def logout_funcionario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        matricula = str(data.get('matricula', '')).strip()
        
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        if matricula not in funcionarios_logados:
            return jsonify({'mensagem': 'Funcionário não estava logado.'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        funcionario = next((f for f in funcionarios if str(f['matricula']).strip() == matricula), None)
        
        # Registrar logout
        funcionarios_logados.discard(matricula)
        if funcionario:
            registrar_saida(matricula, funcionarios, historico)
            salvar_dados(veiculos, vagas, historico, funcionarios)
            logger.info(f"Funcionário {funcionario['nome']} (matrícula {matricula}) fez logout")
            return jsonify({'mensagem': f'Funcionário {funcionario["nome"]} deslogado com sucesso!'}), 200
        else:
            return jsonify({'mensagem': f'Funcionário {matricula} deslogado com sucesso!'}), 200
            
    except Exception as e:
        logger.error(f"Erro no logout do funcionário: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Listar funcionários logados
@funcionarios_bp.route('/funcionarios-logados')
def funcionarios_logados_route():
    try:
        veiculos, vagas, historico, funcionarios = carregar_dados()
        logados = [f for f in funcionarios if str(f['matricula']).strip() in funcionarios_logados]
        return jsonify(logados)
        
    except Exception as e:
        logger.error(f"Erro ao listar funcionários logados: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Verificar se funcionário está logado
@funcionarios_bp.route('/verificar-login/<matricula>')
def verificar_login(matricula):
    try:
        matricula = str(matricula).strip()
        logado = matricula in funcionarios_logados
        return jsonify({'logado': logado, 'matricula': matricula})
        
    except Exception as e:
        logger.error(f"Erro ao verificar login: {e}")
        return jsonify({'logado': False, 'mensagem': 'Erro interno do servidor!'}), 500 