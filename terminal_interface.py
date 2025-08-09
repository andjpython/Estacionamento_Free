"""
Interface de terminal para o Sistema de Estacionamento Rotativo
"""
from estacionamento import (
    carregar_dados, salvar_dados, estacionar_veiculo, liberar_vaga,
    remover_veiculo_por_cpf, registrar_entrada, registrar_saida
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
        
        try:
            veiculos, vagas, historico, funcionarios = carregar_dados()
            
            if opcao == "0":
                menu_supervisor_interface()
            elif opcao == "1":
                cadastrar_veiculo_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "2":
                estacionar_veiculo_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "3":
                liberar_vaga_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "4":
                print(ver_status_vagas(vagas))
            elif opcao == "5":
                excedidos = verificar_tempo_excedido(vagas)
                if excedidos:
                    print("⚠️ VEÍCULOS COM TEMPO EXCEDIDO:")
                    for item in excedidos:
                        print(f"Vaga {item['numero']} - {item['veiculo']} - {item['horas']}h")
                else:
                    print("✅ Nenhum veículo com tempo excedido.")
            elif opcao == "6":
                remover_veiculo_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "7":
                cadastrar_funcionario_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "8":
                print(listar_funcionarios(funcionarios))
            elif opcao == "9":
                login_funcionario_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "10":
                logout_funcionario_interface(veiculos, vagas, historico, funcionarios)
            elif opcao == "11":
                print(listar_veiculos_cadastrados(veiculos))
            elif opcao == "12":
                salvar_dados(veiculos, vagas, historico, funcionarios)
                print("🚪 Saindo... Até logo!")
                break
            else:
                print("❌ Opção inválida!")
                
        except Exception as e:
            logger.error(f"Erro no menu principal: {e}")
            print("❌ Erro interno do sistema!")

def cadastrar_veiculo_interface(veiculos, vagas, historico, funcionarios):
    """Interface para cadastro de veículo"""
    print("\n=== CADASTRAR VEÍCULO ===")
    placa = input("Placa: ").strip().upper()
    cpf = input("CPF: ").strip()
    modelo = input("Modelo (deixe vazio se visitante): ").strip()
    nome = input("Nome: ").strip()
    bloco = input("Bloco: ").strip()
    apartamento = input("Apartamento: ").strip()
    
    resultado = cadastrar_veiculo(veiculos, placa, cpf, modelo, nome, bloco, apartamento)
    print(resultado)
    
    if "✅" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def estacionar_veiculo_interface(veiculos, vagas, historico, funcionarios):
    """Interface para estacionar veículo"""
    print("\n=== ESTACIONAR VEÍCULO ===")
    placa = input("Digite a placa do veículo: ").strip()
    
    resultado = estacionar_veiculo(placa, veiculos, vagas, historico)
    print(resultado)
    
    if "✅" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def liberar_vaga_interface(veiculos, vagas, historico, funcionarios):
    """Interface para liberar vaga"""
    print("\n=== REGISTRAR SAÍDA ===")
    placa = input("Placa do veículo: ").strip()
    matricula = input("Matrícula do funcionário: ").strip()
    
    resultado = liberar_vaga(placa, matricula, veiculos, vagas, historico, funcionarios)
    print(resultado)
    
    if "✅" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def remover_veiculo_interface(veiculos, vagas, historico, funcionarios):
    """Interface para remoção de veículo por CPF"""
    print("\n=== REMOVER VEÍCULO POR CPF ===")
    cpf = input("CPF do proprietário: ").strip()
    matricula = input("Matrícula do funcionário: ").strip()
    
    resultado = remover_veiculo_por_cpf(cpf, matricula, veiculos, vagas, historico, funcionarios)
    print(resultado)
    
    if "🗑️" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def cadastrar_funcionario_interface(veiculos, vagas, historico, funcionarios):
    """Interface para cadastro de funcionário"""
    print("\n=== CADASTRAR FUNCIONÁRIO ===")
    nome = input("Nome do funcionário: ").strip()
    matricula = input("Matrícula (4 dígitos): ").strip()
    
    resultado = cadastrar_funcionario(funcionarios, nome, matricula)
    print(resultado)
    
    if "✅" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def login_funcionario_interface(veiculos, vagas, historico, funcionarios):
    """Interface para login de funcionário"""
    print("\n=== LOGIN FUNCIONÁRIO ===")
    matricula = input("Digite sua matrícula: ").strip()
    
    resultado = registrar_entrada(matricula, funcionarios, historico)
    print(resultado)
    
    if "🔓" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def logout_funcionario_interface(veiculos, vagas, historico, funcionarios):
    """Interface para logout de funcionário"""
    print("\n=== LOGOUT FUNCIONÁRIO ===")
    matricula = input("Digite sua matrícula: ").strip()
    
    resultado = registrar_saida(matricula, funcionarios, historico)
    print(resultado)
    
    if "🔒" in resultado:
        salvar_dados(veiculos, vagas, historico, funcionarios)

def menu_supervisor_interface():
    """Interface para área do supervisor"""
    print("\n=== ACESSO RESTRITO - SUPERVISOR ===")
    from supervisor import menu_supervisor
    
    # Importar funções necessárias
    menu_supervisor(
        carregar_dados, 
        salvar_dados, 
        cadastrar_funcionario, 
        listar_funcionarios, 
        listar_veiculos_cadastrados
    )

if __name__ == "__main__":
    menu_principal() 