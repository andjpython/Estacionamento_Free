"""
Script para inicialização de dados no banco
"""
from datetime import datetime
import pytz
from models.models import Vaga, TipoVaga, Funcionario
from db import get_db, init_db

def init_vagas():
    """Inicializa vagas padrão"""
    with next(get_db()) as db:
        # Verificar se já existem vagas
        if db.query(Vaga).count() > 0:
            print("Vagas já inicializadas")
            return
        
        # Criar vagas comuns
        for i in range(1, 21):
            vaga = Vaga(
                numero=i,
                tipo=TipoVaga.COMUM,
                ocupada=False
            )
            db.add(vaga)
        
        # Criar vagas de visitantes
        for i in range(21, 31):
            vaga = Vaga(
                numero=i,
                tipo=TipoVaga.VISITANTE,
                ocupada=False
            )
            db.add(vaga)
        
        db.commit()
        print("Vagas inicializadas com sucesso")

def init_funcionario():
    """Inicializa funcionário padrão"""
    with next(get_db()) as db:
        # Verificar se já existe funcionário
        if db.query(Funcionario).count() > 0:
            print("Funcionário já inicializado")
            return
        
        # Criar funcionário padrão
        funcionario = Funcionario(
            matricula="1234",
            nome="Administrador",
            ativo=True,
            ultimo_login=datetime.now(pytz.UTC)
        )
        db.add(funcionario)
        db.commit()
        print("Funcionário inicializado com sucesso")

def init_all():
    """Inicializa todos os dados"""
    try:
        init_db()  # Cria tabelas se não existirem
        init_vagas()
        init_funcionario()
        print("Dados inicializados com sucesso")
    except Exception as e:
        print(f"Erro ao inicializar dados: {e}")

if __name__ == "__main__":
    init_all()
