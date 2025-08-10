"""
Decoradores para proteção de rotas
"""
from functools import wraps
from flask import request, jsonify
from utils.security import verify_jwt_token

def require_auth(f):
    """Decorador que verifica se o usuário está autenticado via JWT"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'mensagem': 'Token de autenticação não fornecido!'}), 401
        
        token = token.split(' ')[1]
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'mensagem': 'Token de autenticação inválido!'}), 401
        
        # Adiciona o payload do token ao request para uso na rota
        request.auth_payload = payload
        return f(*args, **kwargs)
    return decorated

def require_supervisor(f):
    """Decorador que verifica se o usuário é um supervisor"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'mensagem': 'Token de autenticação não fornecido!'}), 401
        
        token = token.split(' ')[1]
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'mensagem': 'Token de autenticação inválido!'}), 401
        
        if not payload.get('is_supervisor'):
            return jsonify({'mensagem': 'Acesso negado. Apenas supervisores podem acessar esta rota!'}), 403
        
        request.auth_payload = payload
        return f(*args, **kwargs)
    return decorated
