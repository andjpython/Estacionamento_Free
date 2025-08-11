from flask import Blueprint, request, jsonify
from datetime import datetime
import pytz
import os
from sqlalchemy.orm import Session

from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error
from utils.security import verify_supervisor_password
from utils.rate_limiter import login_limit, api_limit
from utils.state import funcionarios_logados
from db import SessionLocal
from repositories import FuncionarioRepository, HistoricoRepository
from services import funcionario_service

# Configurar logger
logger = setup_logger(__name__)

funcionarios_bp = Blueprint('funcionarios', __name__)

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
        
        if not nome or not matricula:
            return jsonify({'mensagem': active_config.Mensagens.DADOS_NAO_FORNECIDOS}), 400
            
        if not verify_supervisor_password(senha):
            return jsonify({'mensagem': active_config.Mensagens.SENHA_INCORRETA}), 403
            
        db = SessionLocal()
        try:
            resposta = funcionario_service.cadastrar_funcionario(db, nome, matricula)
            log_operation(logger, f"Funcionário {nome} cadastrado com matrícula {matricula}")
            return jsonify({'mensagem': resposta})
        finally:
            db.close()
            
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
            
        db = SessionLocal()
        try:
            funcionarios = funcionario_service.listar_funcionarios(db)
            if not funcionarios:
                return jsonify({'mensagem': 'Nenhum funcionário cadastrado.'}), 404
                
            return jsonify([{
                'id': f.id.scalar() if hasattr(f.id, 'scalar') else f.id,
                'nome': f.nome.scalar() if hasattr(f.nome, 'scalar') else f.nome,
                'matricula': f.matricula.scalar() if hasattr(f.matricula, 'scalar') else f.matricula,
                'ativo': f.ativo.scalar() if hasattr(f.ativo, 'scalar') else f.ativo,
                'criado_em': f.criado_em.isoformat() if f.criado_em else None
            } for f in funcionarios])
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao listar funcionários: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Login funcionário
@funcionarios_bp.route('/login-funcionario', methods=['POST'])
@login_limit()
def login_funcionario():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        matricula = str(data.get('matricula', '')).strip()
        
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        db = SessionLocal()
        try:
            funcionario_repo = FuncionarioRepository(db)
            historico_repo = HistoricoRepository(db)
            
            funcionario = funcionario_repo.get_by_matricula(matricula)
            
            if not funcionario:
                return jsonify({'mensagem': 'Matrícula não encontrada!'}), 404
                
            if matricula in funcionarios_logados:
                return jsonify({'mensagem': f'Funcionário {funcionario.nome} já está logado!'}), 200
                
            # Registrar login
            funcionarios_logados.add(matricula)
            historico_repo.create_from_dict({
                'acao': "login",
                'placa': "N/A",
                'nome': funcionario.nome,
                'tipo': "funcionario",
                'funcionario_nome': funcionario.nome,
                'matricula': matricula
            })
            
            logger.info(f"Funcionário {funcionario.nome} (matrícula {matricula}) fez login")
            return jsonify({'mensagem': f'Funcionário {funcionario.nome} logado com sucesso!'}), 200
            
        finally:
            db.close()
            
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
            
        db = SessionLocal()
        try:
            funcionario_repo = FuncionarioRepository(db)
            historico_repo = HistoricoRepository(db)
            
            funcionario = funcionario_repo.get_by_matricula(matricula)
            
            # Registrar logout
            funcionarios_logados.discard(matricula)
            if funcionario:
                historico_repo.create_from_dict({
                    'acao': "logout",
                    'placa': "N/A",
                    'nome': funcionario.nome,
                    'tipo': "funcionario",
                    'funcionario_nome': funcionario.nome,
                    'matricula': matricula
                })
                
                logger.info(f"Funcionário {funcionario.nome} (matrícula {matricula}) fez logout")
                return jsonify({'mensagem': f'Funcionário {funcionario.nome} deslogado com sucesso!'}), 200
            else:
                return jsonify({'mensagem': f'Funcionário {matricula} deslogado com sucesso!'}), 200
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro no logout do funcionário: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Remover funcionário
@funcionarios_bp.route('/remover-funcionario', methods=['POST'])
def remover_funcionario_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        matricula = str(data.get('matricula', '')).strip()
        senha = data.get('senha_supervisor', '')
        
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        if not verify_supervisor_password(senha):
            return jsonify({'mensagem': 'Senha incorreta!'}), 403
            
        db = SessionLocal()
        try:
            resposta = funcionario_service.remover_funcionario(db, matricula)
            return jsonify({'mensagem': resposta})
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao remover funcionário: {e}")
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

# Listar funcionários logados
@funcionarios_bp.route('/funcionarios-logados')
def listar_funcionarios_logados():
    try:
        db = SessionLocal()
        try:
            funcionario_repo = FuncionarioRepository(db)
            funcionarios = []
            
            for matricula in funcionarios_logados:
                funcionario = funcionario_repo.get_by_matricula(matricula)
                if funcionario:
                    funcionarios.append({
                        'matricula': matricula,
                        'nome': funcionario.nome
                    })
            
            return jsonify(funcionarios)
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Erro ao listar funcionários logados: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# ====== Rotas utilitárias (sem Shell) ======
# Permitem cadastrar funcionário via GET e fazer seed básico protegido pela senha do supervisor.

@funcionarios_bp.route('/cadastrar-funcionario-get', methods=['GET'])
def cadastrar_funcionario_get():
    try:
        nome = request.args.get('nome', '').strip()
        matricula = request.args.get('matricula', '').strip()
        senha = request.args.get('senha_supervisor', '')

        if not verify_supervisor_password(senha):
            return jsonify({'mensagem': 'Acesso negado. Senha incorreta!'}), 403
        if not nome or not matricula:
            return jsonify({'mensagem': 'Nome e matrícula são obrigatórios!'}), 400

        db = SessionLocal()
        try:
            resposta = funcionario_service.cadastrar_funcionario(db, nome, matricula)
            return jsonify({'mensagem': resposta})
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro no cadastro GET do funcionário: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

@funcionarios_bp.route('/bootstrap-dados', methods=['GET'])
def bootstrap_dados():
    """Cria funcionários básicos sem precisar de Shell/Console.
    Protegido pela senha do supervisor via querystring.
    """
    try:
        senha = request.args.get('senha_supervisor', '')
        if not verify_supervisor_password(senha):
            return jsonify({'mensagem': 'Acesso negado. Senha incorreta!'}), 403

        db = SessionLocal()
        criados = []
        try:
            repo = FuncionarioRepository(db)

            def ensure(nome: str, matricula: str):
                if not repo.get_by_matricula(matricula):
                    funcionario_service.cadastrar_funcionario(db, nome, matricula)
                    criados.append(matricula)

            ensure('João Teste', '0001')
            ensure('Maria Teste', '0002')

            return jsonify({'status': 'ok', 'criados': criados})
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Erro no bootstrap de dados: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500