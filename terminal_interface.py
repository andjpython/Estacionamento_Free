"""
Interface de terminal para o Sistema de Estacionamento Rotativo
"""
from sqlalchemy.orm import Session
from utils.db_context import get_db_session
from utils.validators import validar_placa, validar_matricula, validar_cpf
from estacionamento import (
    estacionar_veiculo, liberar_vaga, remover_veiculo_por_cpf,
    registrar_entrada, registrar_saida
)
from services.veiculo_service import cadastrar_veiculo, listar_veiculos_cadastrados
from services.funcionario_service import cadastrar_funcionario, listar_funcionarios  
from services.vaga_service import ver_status_vagas, verificar_tempo_excedido
from utils.logging_config import setup_logger

# Configurar logger
logger = setup_logger(__name__)

def menu_principal():
    """Menu principal do sistema (interface de terminal)"""
    while True:
        print("\n==== SISTEMA DE ESTACIONAMENTO ROTATIVO ====")
        print("0. Área do Supervisor 🔐")
        print("1. Cadastrar veículo")
        print("2. Estacionar veículo")
        print("3. Registrar saída")
        print("4. Ver status de vagas")
        print("5. Verificar tempo excedido")
        print("6. Remover veículo por CPF")
        print("7. Cadastrar funcionário")
        print("8. Listar funcionários")
        print("9. Login funcionário")
        print("10. Logout funcionário")
        print("11. Listar veículos cadastrados")
        print("12. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "12":
            print("🚪 Saindo... Até logo!")
            break
            
        try:
            with get_db_session() as db:
                if opcao == "0":
                    menu_supervisor_interface(db)
                elif opcao == "1":
                    cadastrar_veiculo_interface(db)
                elif opcao == "2":
                    estacionar_veiculo_interface(db)
                elif opcao == "3":
                    liberar_vaga_interface(db)
                elif opcao == "4":
                    print(ver_status_vagas(db))
                elif opcao == "5":
                    excedidos = verificar_tempo_excedido(db)
                    if excedidos:
                        print("⚠️ VEÍCULOS COM TEMPO EXCEDIDO:")
                        for item in excedidos:
                            print(f"Vaga {item['numero']} - {item['veiculo']} - {item['horas']}h")
                    else:
                        print("✅ Nenhum veículo com tempo excedido.")
                elif opcao == "6":
                    remover_veiculo_interface(db)
                elif opcao == "7":
                    cadastrar_funcionario_interface(db)
                elif opcao == "8":
                    print(listar_funcionarios(db))
                elif opcao == "9":
                    login_funcionario_interface(db)
                elif opcao == "10":
                    logout_funcionario_interface(db)
                elif opcao == "11":
                    print(listar_veiculos_cadastrados(db))
                else:
                    print("❌ Opção inválida!")
                    
        except Exception as e:
            logger.error(f"Erro no menu principal: {e}")
            print("❌ Erro interno do sistema!")

def cadastrar_veiculo_interface(db: Session):
    """Interface para cadastro de veículo"""
    print("\n=== CADASTRAR VEÍCULO ===")
    
    # Validar placa
    while True:
        placa = input("Placa: ").strip().upper()
        valido, msg = validar_placa(placa)
        if valido:
            break
        print(msg)
    
    # Validar CPF
    while True:
        cpf = input("CPF: ").strip()
        valido, msg = validar_cpf(cpf)
        if valido:
            break
        print(msg)
    
    modelo = input("Modelo (deixe vazio se visitante): ").strip()
    nome = input("Nome: ").strip()
    if not nome:
        print("❌ Nome é obrigatório!")
        return
        
    bloco = input("Bloco: ").strip()
    apartamento = input("Apartamento: ").strip()
    
    resultado = cadastrar_veiculo(db, placa, cpf, modelo, nome, bloco, apartamento)
    print(resultado)

def estacionar_veiculo_interface(db: Session):
    """Interface para estacionar veículo"""
    print("\n=== ESTACIONAR VEÍCULO ===")
    
    # Validar placa
    while True:
        placa = input("Digite a placa do veículo: ").strip().upper()
        valido, msg = validar_placa(placa)
        if valido:
            break
        print(msg)
    
    resultado = estacionar_veiculo(db, placa)
    print(resultado)

def liberar_vaga_interface(db: Session):
    """Interface para liberar vaga"""
    print("\n=== REGISTRAR SAÍDA ===")
    
    # Validar placa
    while True:
        placa = input("Placa do veículo: ").strip().upper()
        valido, msg = validar_placa(placa)
        if valido:
            break
        print(msg)
    
    # Validar matrícula
    while True:
        matricula = input("Matrícula do funcionário: ").strip()
        valido, msg = validar_matricula(matricula)
        if valido:
            break
        print(msg)
    
    resultado = liberar_vaga(db, placa, matricula)
    print(resultado)

def remover_veiculo_interface(db: Session):
    """Interface para remoção de veículo por CPF"""
    print("\n=== REMOVER VEÍCULO POR CPF ===")
    
    # Validar CPF
    while True:
        cpf = input("CPF do proprietário: ").strip()
        valido, msg = validar_cpf(cpf)
        if valido:
            break
        print(msg)
    
    # Validar matrícula
    while True:
        matricula = input("Matrícula do funcionário: ").strip()
        valido, msg = validar_matricula(matricula)
        if valido:
            break
        print(msg)
    
    resultado = remover_veiculo_por_cpf(db, cpf, matricula)
    print(resultado)

def cadastrar_funcionario_interface(db: Session):
    """Interface para cadastro de funcionário"""
    print("\n=== CADASTRAR FUNCIONÁRIO ===")
    
    nome = input("Nome do funcionário: ").strip()
    if not nome:
        print("❌ Nome é obrigatório!")
        return
    
    # Validar matrícula
    while True:
        matricula = input("Matrícula (4 dígitos): ").strip()
        valido, msg = validar_matricula(matricula)
        if valido:
            break
        print(msg)
    
    resultado = cadastrar_funcionario(db, nome, matricula)
    print(resultado)

def login_funcionario_interface(db: Session):
    """Interface para login de funcionário"""
    print("\n=== LOGIN FUNCIONÁRIO ===")
    
    # Validar matrícula
    while True:
        matricula = input("Digite sua matrícula: ").strip()
        valido, msg = validar_matricula(matricula)
        if valido:
            break
        print(msg)
    
    resultado = registrar_entrada(db, matricula)
    print(resultado)

def logout_funcionario_interface(db: Session):
    """Interface para logout de funcionário"""
    print("\n=== LOGOUT FUNCIONÁRIO ===")
    
    # Validar matrícula
    while True:
        matricula = input("Digite sua matrícula: ").strip()
        valido, msg = validar_matricula(matricula)
        if valido:
            break
        print(msg)
    
    resultado = registrar_saida(db, matricula)
    print(resultado)

def menu_supervisor_interface(db: Session):
    """Interface para área do supervisor"""
    print("\n=== ACESSO RESTRITO - SUPERVISOR ===")
    from supervisor import menu_supervisor
    menu_supervisor(db)

if __name__ == "__main__":
    menu_principal()