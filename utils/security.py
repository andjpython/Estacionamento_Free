"""
Utilitários de segurança
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import active_config

def hash_password(password: str) -> str:
    """Gera um hash da senha usando bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def verify_supervisor_password(password: str) -> bool:
    """Verifica se a senha do supervisor está correta"""
    expected = (active_config.SENHA_SUPERVISOR or "").strip()
    password = (password or "").strip()
    # Se a senha ainda não foi hasheada (primeira execução), usa comparação direta
    if not expected.startswith('$2b$'):
        return password == expected
    # Se a senha já foi hasheada, usa bcrypt para verificar
    return verify_password(password, expected)

def create_jwt_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=active_config.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, active_config.JWT_SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifica e decodifica um token JWT"""
    try:
        return jwt.decode(token, active_config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None
