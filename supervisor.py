"""
Interface do supervisor para o Sistema de Estacionamento Rotativo
"""
from getpass import getpass
from sqlalchemy.orm import Session
from services.historico_service import ver_historico
from services.veiculo_service import listar_veiculos_cadastrados
from services.funcionario_service import (
    listar_funcionarios, cadastrar_funcionario,
    remover_funcionario as service_remover_funcionario
)
from config import active_config

def menu_supervisor(db: Session):
    """Menu do supervisor com acesso a funções administrativas"""
    senha = getpass("Digite a senha de supervisor: ")
    if senha != active_config.SENHA_SUPERVISOR:
        print("❌ Senha incorreta!")
        return

    while True:
        print("\n==== MENU DO SUPERVISOR ====")
        print("1. Cadastrar funcionário")
        print("2. Listar funcionários")
        print("3. Ver histórico completo")
        print("4. Remover funcionário")
        print("5. Listar veículos cadastrados")
        print("6. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do funcionário: ").strip()
            matricula = input("Matrícula (4 dígitos): ").strip()
            resultado = cadastrar_funcionario(db, nome, matricula)
            print(resultado)
            if "✅" in resultado:
                db.commit()
        elif opcao == "2":
            print(listar_funcionarios(db))
        elif opcao == "3":
            print(ver_historico(db))
        elif opcao == "4":
            matricula = input("Matrícula do funcionário a remover: ").strip()
            resultado = service_remover_funcionario(db, matricula)
            print(resultado)
            if "🗑️" in resultado:
                db.commit()
        elif opcao == "5":
            print(listar_veiculos_cadastrados(db))
        elif opcao == "6":
            print("🔙 Retornando ao menu principal...")
            break
        else:
            print("❌ Opção inválida!")