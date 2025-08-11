"""
Script de gerenciamento do projeto Estacionamento Rotativo
"""
import click
import os
import sys
from datetime import datetime
import pytz
from utils.error_logger import ErrorLogger
from utils.monitoring import SystemMonitor
from db import init_db, engine
from sqlalchemy import text

@click.group()
def cli():
    """Sistema de Gerenciamento do Estacionamento Rotativo"""
    pass

@cli.command()
def init():
    """Inicializa o banco de dados"""
    try:
        init_db()
        click.echo('✅ Banco de dados inicializado com sucesso!')
    except Exception as e:
        click.echo(f'❌ Erro ao inicializar banco de dados: {str(e)}')
        sys.exit(1)

@cli.command()
def check():
    """Verifica o status do sistema"""
    click.echo('🔍 Verificando status do sistema...\n')
    
    # Verifica banco de dados
    db_status = SystemMonitor.check_database()
    if db_status['status'] == 'ok':
        click.echo('✅ Banco de dados: Conectado')
    else:
        click.echo(f'❌ Banco de dados: {db_status["message"]}')
    
    # Verifica recursos do sistema
    resources = SystemMonitor.check_system_resources()
    if resources['status'] == 'ok':
        click.echo('\n📊 Recursos do Sistema:')
        click.echo(f'   CPU: {resources["resources"]["cpu_percent"]}%')
        click.echo(f'   Memória: {resources["resources"]["memory_percent"]}%')
        click.echo(f'   Disco: {resources["resources"]["disk_percent"]}%')
    else:
        click.echo(f'❌ Recursos: {resources["message"]}')

@cli.command()
def logs():
    """Mostra os últimos logs do sistema"""
    log_file = 'logs/error.log'
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.readlines()
            if logs:
                click.echo('📝 Últimos logs do sistema:\n')
                for log in logs[-10:]:  # Mostra últimos 10 logs
                    click.echo(log.strip())
            else:
                click.echo('ℹ️ Nenhum log encontrado.')
    else:
        click.echo('ℹ️ Arquivo de log não encontrado.')

@cli.command()
@click.option('--level', default='info', help='Nível de log (debug/info/warning/error)')
def test_log(level):
    """Testa o sistema de logs"""
    message = f'Teste de log - {datetime.now(pytz.timezone("America/Sao_Paulo"))}'
    
    if level == 'error':
        ErrorLogger.log_error('TEST', message)
    elif level == 'warning':
        ErrorLogger.log_warning('TEST', message)
    else:
        ErrorLogger.log_info('TEST', message)
    
    click.echo(f'✅ Log de {level} registrado com sucesso!')

@cli.command()
def clear_logs():
    """Limpa os arquivos de log"""
    try:
        if os.path.exists('logs/error.log'):
            os.remove('logs/error.log')
            click.echo('✅ Logs limpos com sucesso!')
        else:
            click.echo('ℹ️ Não há logs para limpar.')
    except Exception as e:
        click.echo(f'❌ Erro ao limpar logs: {str(e)}')

@cli.command()
def run():
    """Executa o servidor de desenvolvimento"""
    try:
        from app import app
        click.echo('🚀 Iniciando servidor de desenvolvimento...')
        app.run(debug=True)
    except Exception as e:
        click.echo(f'❌ Erro ao iniciar servidor: {str(e)}')

if __name__ == '__main__':
    cli()
