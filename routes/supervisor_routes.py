from flask import Blueprint, request, jsonify, url_for
from services import historico_service
from config import active_config
from db import SessionLocal
from utils.security import verify_supervisor_password, create_jwt_token
from utils.decorators import require_supervisor
from utils.rate_limiter import login_limit, api_limit

supervisor_bp = Blueprint('supervisor', __name__)

# Variável global para controlar login do supervisor
supervisor_logado = False

@supervisor_bp.route('/login-supervisor', methods=['POST'])
@login_limit()
def login_supervisor():
    global supervisor_logado
    data = request.get_json()
    senha = data.get('senha')
    if verify_supervisor_password(senha):
        supervisor_logado = True
        # Criar token JWT
        token = create_jwt_token({
            'is_supervisor': True,
            'nome': 'Anderson J Silveira'
        })
        return jsonify({
            'mensagem': 'Login confirmado com sucesso!',
            'nome': 'Anderson J Silveira',
            'token': token,
            'redirect': url_for('sistema')
        }), 200
    return jsonify({'mensagem': 'Senha incorreta!'}), 401

@supervisor_bp.route('/logout-supervisor', methods=['POST'])
def logout_supervisor():
    global supervisor_logado
    supervisor_logado = False
    return jsonify({'mensagem': 'Supervisor deslogado com sucesso!'}), 200

# Ver histórico completo
@supervisor_bp.route('/historico', methods=['GET'])
def historico():
    db = SessionLocal()
    try:
        historico = historico_service.ver_historico(db)
        return jsonify({'historico': historico})
    finally:
        db.close()