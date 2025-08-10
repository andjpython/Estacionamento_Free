"""
Serviço de gerenciamento de veículos
"""
import re
from datetime import datetime
import pytz
from typing import List
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
    # Remover caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verificar tamanho
    if len(cpf) != 11:
        return False
        
    # Verificar se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False
        
    # Calcular primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verificar primeiro dígito
    if digito1 != int(cpf[9]):
        return False
        
    # Calcular segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verificar segundo dígito
    return digito2 == int(cpf[10])

def normalizar_cpf(cpf):
    """Remove caracteres não numéricos do CPF"""
    return re.sub(r'[^0-9]', '', cpf)

def normalizar_placa(placa):
    """Normaliza placa removendo espaços e convertendo para maiúsculas"""
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
    
    # Determinar e validar tipo
    tipo = "morador" if modelo else "visitante"
    if tipo == "morador" and not modelo:
        return "❌ Modelo do veículo é obrigatório para moradores."
    
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
def listar_veiculos_cadastrados(db: Session) -> List[Veiculo]:
    """Lista todos os veículos cadastrados no sistema, ordenados por placa"""
    repo = VeiculoRepository(db)
    return repo.get_all()