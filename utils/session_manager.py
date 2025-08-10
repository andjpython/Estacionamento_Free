"""
Gerenciador de sessões thread-safe
"""
from threading import Lock
from typing import Set, Dict, Optional
from datetime import datetime, timedelta

class SessionManager:
    """Gerencia sessões de login com thread safety"""
    def __init__(self):
        self._lock = Lock()
        self._sessions: Dict[str, datetime] = {}
        self._timeout = timedelta(hours=8)  # Sessão expira em 8h
        
    def login(self, user_id: str) -> bool:
        """Registra login de usuário"""
        with self._lock:
            if user_id in self._sessions:
                return False
            self._sessions[user_id] = datetime.now()
            return True
            
    def logout(self, user_id: str) -> bool:
        """Registra logout de usuário"""
        with self._lock:
            if user_id not in self._sessions:
                return False
            del self._sessions[user_id]
            return True
            
    def is_logged_in(self, user_id: str) -> bool:
        """Verifica se usuário está logado"""
        with self._lock:
            if user_id not in self._sessions:
                return False
            # Verificar timeout
            if datetime.now() - self._sessions[user_id] > self._timeout:
                del self._sessions[user_id]
                return False
            return True
            
    def get_active_sessions(self) -> Set[str]:
        """Retorna IDs dos usuários com sessão ativa"""
        with self._lock:
            now = datetime.now()
            active = {
                user_id
                for user_id, login_time in self._sessions.items()
                if now - login_time <= self._timeout
            }
            # Limpar sessões expiradas
            expired = set(self._sessions.keys()) - active
            for user_id in expired:
                del self._sessions[user_id]
            return active
            
    def clear_all(self):
        """Limpa todas as sessões"""
        with self._lock:
            self._sessions.clear()

# Instância global
session_manager = SessionManager()

