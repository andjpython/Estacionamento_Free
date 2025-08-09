"""
Serviços para gerenciamento de funcionários
"""
from config import active_config

def cadastrar_funcionario(funcionarios, nome, matricula):
    """Cadastra um novo funcionário no sistema"""
    if any(f['matricula'] == matricula for f in funcionarios):
        return "❌ Matrícula já cadastrada."
    if not matricula or len(matricula) != 4 or not matricula.isdigit():
        return active_config.Mensagens.MATRICULA_INVALIDA
    if not nome:
        return "❌ Nome do funcionário é obrigatório."
    
    funcionarios.append({
        "nome": nome.strip(),
        "matricula": matricula.strip()
    })
    return active_config.Mensagens.FUNCIONARIO_CADASTRADO.format(nome=nome, matricula=matricula)

def listar_funcionarios(funcionarios):
    """Lista todos os funcionários cadastrados"""
    if not funcionarios:
        return active_config.Mensagens.NENHUM_FUNCIONARIO_CADASTRADO
    return "\n".join([f"Nome: {f['nome']} | Matrícula: {f['matricula']}" for f in funcionarios])

# === Buscar funcionário por matrícula ===
def buscar_funcionario_por_matricula(funcionarios, matricula):
    return next((f for f in funcionarios if f['matricula'] == matricula), None) 