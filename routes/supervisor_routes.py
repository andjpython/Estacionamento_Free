from flask import Blueprint, request, jsonify, url_for
from services.historico_service import ver_historico
import os

supervisor_bp = Blueprint('supervisor', __name__)

# Senha do supervisor (usando variável de ambiente)
senha_master = os.environ.get("SENHA_SUPERVISOR", "290479")

# Variável global para controlar login do supervisor
supervisor_logado = False

@supervisor_bp.route('/login-supervisor', methods=['POST'])
def login_supervisor():
    global supervisor_logado
    data = request.get_json()
    senha = data.get('senha')
    if senha == senha_master:
        supervisor_logado = True
        return jsonify({'mensagem': 'Login confirmado com sucesso!', 'nome': 'Anderson J Silveira', 'redirect': url_for('sistema')}), 200
    return jsonify({'mensagem': 'Senha incorreta!'}), 401

@supervisor_bp.route('/logout-supervisor', methods=['POST'])
def logout_supervisor():
    global supervisor_logado
    supervisor_logado = False
    return jsonify({'mensagem': 'Supervisor deslogado com sucesso!'}), 200

# Ver histórico completo
@supervisor_bp.route('/historico', methods=['GET'])
def historico():
    from estacionamento import carregar_dados
    veiculos, vagas, historico, funcionarios = carregar_dados()
    return jsonify({'historico': ver_historico(historico)}) 