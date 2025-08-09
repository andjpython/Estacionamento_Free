"""
Serviço de gerenciamento de veículos
"""
import re
from datetime import datetime
import pytz
from sqlalchemy.orm import Session
from config import active_config
from models import Veiculo
from repositories import VeiculoRepository

# === Funções de validação ===
def validar_placa(placa):
    """Valida placa nos formatos antigo (ABC1234) e Mercosul (ABC1D23)"""
    if not placa:
        return False
    
    placa = placa.replace(" ", "").upper()
    
    # Padrão antigo: ABC1234
    padrao_antigo = re.match(r'^[A-Z]{3}[0-9]{4}$', placa)
    # Padrão Mercosul: ABC1D23
    padrao_mercosul = re.match(r'^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$', placa)
    
    return bool(padrao_antigo or padrao_mercosul)

def validar_cpf(cpf):
    """Valida CPF com algoritmo de verificação dos dígitos"""
    if not cpf:
        return False
    
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se não são todos iguais (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False
    
    # Validação dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    
    return True

def normalizar_cpf(cpf):
    """Normaliza CPF removendo formatação"""
    if not cpf:
        return ""
    return re.sub(r'\D', '', cpf.strip())

def normalizar_placa(placa):
    """Normaliza placa removendo espaços e convertendo para maiúscula"""
    if not placa:
        return ""
    return placa.replace(" ", "").upper().strip()

# === Cadastro de veículo ===
def cadastrar_veiculo(db: Session, placa: str, cpf: str, modelo: str, nome: str, bloco: str, apartamento: str) -> str:
    """Cadastra um novo veículo no sistema"""
    repo = VeiculoRepository(db)
    
    # Normalizar dados de entrada
    placa = normalizar_placa(placa)
    cpf = normalizar_cpf(cpf)
    nome = nome.strip() if nome else ""
    modelo = modelo.strip() if modelo else ""
    bloco = bloco.strip() if bloco else ""
    apartamento = apartamento.strip() if apartamento else ""
    
    # Validações
    if repo.get_by_placa(placa):
        return active_config.Mensagens.VEICULO_JA_CADASTRADO
    
    if not validar_placa(placa):
        return active_config.Mensagens.PLACA_INVALIDA
    
    if not validar_cpf(cpf):
        return active_config.Mensagens.CPF_INVALIDO
    
    if not nome:
        return active_config.Mensagens.NOME_OBRIGATORIO
    
    # Determinar tipo baseado no modelo
    tipo = "morador" if modelo else "visitante"
    
    # Criar e salvar veículo
    veiculo = Veiculo(
        placa=placa,
        cpf=cpf,
        modelo=modelo,
        tipo=tipo,
        nome=nome,
        bloco=bloco,
        apartamento=apartamento
    )
    repo.create(veiculo)
    
    return active_config.Mensagens.VEICULO_CADASTRADO.format(placa=placa, tipo=tipo)

# === Listar veículos cadastrados ===
def listar_veiculos_cadastrados(db: Session) -> str:
    """Lista todos os veículos cadastrados no sistema"""
    repo = VeiculoRepository(db)
    veiculos = repo.get_all()
    
    if not veiculos:
        return active_config.Mensagens.NENHUM_VEICULO_CADASTRADO
    
    linhas = ["📄 VEÍCULOS CADASTRADOS:"]
    for v in veiculos:
        linhas.append(
            f"🔹 Placa: {v.placa} | Nome: {v.nome} | Tipo: {v.tipo.capitalize()} | "
            f"CPF: {v.cpf} | Modelo: {v.modelo or 'N/A'} | "
            f"Bloco: {v.bloco} | Apto: {v.apartamento}"
        )
    return "\n".join(linhas)

# === Buscar veículo por placa ===
def buscar_veiculo_por_placa(db: Session, placa: str) -> Veiculo:
    """Busca um veículo pela placa"""
    repo = VeiculoRepository(db)
    placa_normalizada = normalizar_placa(placa)
    return repo.get_by_placa(placa_normalizada)