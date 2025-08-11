"""
Sistema de monitoramento e verificação de status
"""
import psutil
import requests
from datetime import datetime
import pytz
from sqlalchemy import text
from db import engine
from utils.error_logger import ErrorLogger

class SystemMonitor:
    @staticmethod
    def check_database():
        """Verifica a conexão com o banco de dados"""
        try:
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            return {
                "status": "ok",
                "message": "Conexão com banco de dados estabelecida"
            }
        except Exception as e:
            ErrorLogger.log_error(
                'DATABASE',
                'Falha na conexão com o banco de dados',
                {'error': str(e)}
            )
            return {
                "status": "error",
                "message": "Falha na conexão com banco de dados",
                "error": str(e)
            }

    @staticmethod
    def check_system_resources():
        """Verifica recursos do sistema"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "status": "ok",
                "resources": {
                    "cpu_percent": cpu,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent
                }
            }
        except Exception as e:
            ErrorLogger.log_error(
                'SYSTEM',
                'Falha ao verificar recursos do sistema',
                {'error': str(e)}
            )
            return {
                "status": "error",
                "message": "Falha ao verificar recursos do sistema",
                "error": str(e)
            }

    @staticmethod
    def check_external_services():
        """Verifica serviços externos necessários"""
        services = {
            "database": "http://localhost:5432",  # Exemplo - ajuste para URL real
        }
        
        results = {}
        for service_name, url in services.items():
            try:
                response = requests.get(url, timeout=5)
                results[service_name] = {
                    "status": "ok" if response.status_code == 200 else "error",
                    "response_time": response.elapsed.total_seconds()
                }
            except requests.RequestException as e:
                ErrorLogger.log_error(
                    'SERVICE',
                    f'Falha ao conectar com serviço {service_name}',
                    {'error': str(e)}
                )
                results[service_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

    @staticmethod
    def full_system_check():
        """Realiza verificação completa do sistema"""
        return {
            "timestamp": datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat(),
            "database": SystemMonitor.check_database(),
            "system_resources": SystemMonitor.check_system_resources(),
            "external_services": SystemMonitor.check_external_services()
        }
