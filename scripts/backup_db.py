"""
Script para fazer backup do banco de dados
"""
import os
import json
from datetime import datetime
import pytz
from models.models import Veiculo, Vaga, Ocupacao, Funcionario
from db import get_db

def backup_data():
    """Faz backup de todos os dados do banco"""
    backup = {
        'veiculos': [],
        'vagas': [],
        'ocupacoes': [],
        'funcionarios': []
    }
    
    with next(get_db()) as db:
        # Backup de veículos
        veiculos = db.query(Veiculo).all()
        for v in veiculos:
            backup['veiculos'].append(v.to_dict())
        
        # Backup de vagas
        vagas = db.query(Vaga).all()
        for v in vagas:
            backup['vagas'].append(v.to_dict())
        
        # Backup de ocupações
        ocupacoes = db.query(Ocupacao).all()
        for o in ocupacoes:
            backup['ocupacoes'].append(o.to_dict())
        
        # Backup de funcionários
        funcionarios = db.query(Funcionario).all()
        for f in funcionarios:
            backup['funcionarios'].append(f.to_dict())
    
    # Criar diretório de backup se não existir
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    # Salvar backup
    timestamp = datetime.now(pytz.UTC).strftime('%Y%m%d_%H%M%S')
    filename = f'backups/backup_{timestamp}.json'
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup, f, indent=2, ensure_ascii=False)
    
    print(f"Backup salvo em {filename}")
    return filename

if __name__ == "__main__":
    try:
        backup_file = backup_data()
        print("Backup realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao fazer backup: {e}")
