"""
Script para popular o banco de dados com dados iniciais
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from db import SessionLocal, init_db
from models import Vaga, Funcionario, Veiculo
from config import active_config

def criar_vagas():
    """Cria as vagas iniciais"""
    session = SessionLocal()
    try:
        # Criar vagas comuns (1-20)
        for i in range(1, 21):
            vaga = Vaga(
                numero=i,
                tipo="comum",
                ocupada=False
            )
            session.add(vaga)

        # Criar vagas de visitantes (21-30)
        for i in range(21, 31):
            vaga = Vaga(
                numero=i,
                tipo="visitante",
                ocupada=False
            )
            session.add(vaga)

        session.commit()
        print("✅ Vagas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar vagas: {str(e)}")
        session.rollback()
    finally:
        session.close()

def criar_funcionarios_exemplo():
    """Cria alguns funcionários de exemplo"""
    session = SessionLocal()
    try:
        funcionarios = [
            {"nome": "João Silva", "matricula": "1234"},
            {"nome": "Maria Santos", "matricula": "5678"},
            {"nome": "Pedro Oliveira", "matricula": "9012"}
        ]
        
        for func in funcionarios:
            funcionario = Funcionario(
                nome=func["nome"],
                matricula=func["matricula"],
                ativo=True
            )
            session.add(funcionario)

        session.commit()
        print("✅ Funcionários de exemplo criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar funcionários: {str(e)}")
        session.rollback()
    finally:
        session.close()

def criar_veiculos_exemplo():
    """Cria alguns veículos de exemplo"""
    session = SessionLocal()
    try:
        veiculos = [
            {
                "placa": "ABC1234",
                "cpf": "12345678901",
                "nome": "José Santos",
                "modelo": "Civic",
                "tipo": "morador",
                "bloco": "A",
                "apartamento": "101"
            },
            {
                "placa": "XYZ5678",
                "cpf": "98765432101",
                "nome": "Ana Silva",
                "modelo": "Corolla",
                "tipo": "morador",
                "bloco": "B",
                "apartamento": "202"
            }
        ]
        
        for veiculo_data in veiculos:
            veiculo = Veiculo(**veiculo_data)
            session.add(veiculo)

        session.commit()
        print("✅ Veículos de exemplo criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar veículos: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("🔄 Iniciando seed do banco de dados...")
    
    # Criar as tabelas (caso não existam)
    init_db()
    print("✅ Tabelas criadas/verificadas!")
    
    # Popular com dados iniciais
    criar_vagas()
    criar_funcionarios_exemplo()
    criar_veiculos_exemplo()
    
    print("✅ Seed concluído com sucesso!")
