"""
Funções de validação para entrada de dados
"""
import re
from typing import Tuple

def validar_placa(placa: str) -> Tuple[bool, str]:
    """Valida placa de veículo no formato ABC1234 ou ABC1D23"""
    placa = placa.upper().strip()
    padrao_antigo = re.compile(r'^[A-Z]{3}[0-9]{4}$')
    padrao_mercosul = re.compile(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$')
    
    if padrao_antigo.match(placa) or padrao_mercosul.match(placa):
        return True, placa
    return False, "❌ Placa inválida. Use formato ABC1234 ou ABC1D23."

def validar_matricula(matricula: str) -> Tuple[bool, str]:
    """Valida matrícula de funcionário (4 dígitos)"""
    matricula = matricula.strip()
    if re.match(r'^\d{4}$', matricula):
        return True, matricula
    return False, "❌ Matrícula inválida. Deve conter 4 dígitos."

def validar_cpf(cpf: str) -> Tuple[bool, str]:
    """Valida CPF (apenas dígitos)"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False, "❌ CPF deve ter 11 dígitos."
        
    # Verifica se todos os dígitos são iguais
    if len(set(cpf)) == 1:
        return False, "❌ CPF inválido."
        
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito = (soma * 10) % 11
    if digito == 10:
        digito = 0
    if digito != int(cpf[9]):
        return False, "❌ CPF inválido."
        
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito = (soma * 10) % 11
    if digito == 10:
        digito = 0
    if digito != int(cpf[10]):
        return False, "❌ CPF inválido."
        
    return True, cpf

