"""
Script para restaurar banco de dados a partir do backup
"""
import json
from models.models import Veiculo, Vaga, Ocupacao, Funcionario
from db import get_db, init_db

def restore_data(backup_file):
    """Restaura dados do backup"""
    # Carregar dados do backup
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup = json.load(f)
    
    with next(get_db()) as db:
        try:
            # Restaurar funcionários
            for f_data in backup['funcionarios']:
                funcionario = Funcionario(**f_data)
                db.add(funcionario)
            
            # Restaurar vagas
            for v_data in backup['vagas']:
                vaga = Vaga(**v_data)
                db.add(vaga)
            
            # Restaurar veículos
            for v_data in backup['veiculos']:
                veiculo = Veiculo(**v_data)
                db.add(veiculo)
            
            # Restaurar ocupações
            for o_data in backup['ocupacoes']:
                ocupacao = Ocupacao(**o_data)
                db.add(ocupacao)
            
            db.commit()
            print("Dados restaurados com sucesso!")
            
        except Exception as e:
            db.rollback()
            print(f"Erro ao restaurar dados: {e}")
            raise

def setup_new_db():
    """Configura novo banco de dados"""
    try:
        # Criar tabelas
        init_db()
        print("Tabelas criadas com sucesso!")
        
        # Se houver backup, restaurar dados
        try:
            from glob import glob
            backups = glob('backups/backup_*.json')
            if backups:
                latest_backup = max(backups)  # Pega o backup mais recente
                restore_data(latest_backup)
            else:
                print("Nenhum backup encontrado. Iniciando banco vazio.")
                
                # Importar e executar inicialização de dados padrão
                from scripts.init_data import init_all
                init_all()
                
        except Exception as e:
            print(f"Erro ao restaurar dados: {e}")
            raise
            
    except Exception as e:
        print(f"Erro ao configurar novo banco: {e}")
        raise

if __name__ == "__main__":
    try:
        setup_new_db()
        print("Banco de dados configurado com sucesso!")
    except Exception as e:
        print(f"Erro na configuração do banco: {e}")
