"""
Sistema de validação com Pydantic para o Sistema de Estacionamento
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator, EmailStr
import re

class VeiculoCreate(BaseModel):
    """Modelo para criação de veículo"""
    placa: str = Field(..., min_length=6, max_length=8, description="Placa do veículo")
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do proprietário")
    cpf: str = Field(..., min_length=11, max_length=14, description="CPF do proprietário")
    modelo: str = Field(..., min_length=2, max_length=50, description="Modelo do veículo")
    bloco: str = Field(..., min_length=1, max_length=10, description="Bloco do apartamento")
    apartamento: str = Field(..., min_length=1, max_length=10, description="Número do apartamento")
    tipo: str = Field(..., regex="^(morador|visitante)$", description="Tipo de usuário")
    
    @validator('placa')
    def validar_placa(cls, v):
        """Valida formato da placa (Mercosul ou antiga)"""
        # Formato antigo: ABC1234
        # Formato Mercosul: ABC1D23
        if not re.match(r'^[A-Z]{3}[0-9]{1}[A-Z0-9]{1}[0-9]{2}$|^[A-Z]{3}[0-9]{4}$', v):
            raise ValueError('Formato de placa inválido. Use ABC1234 ou ABC1D23')
        return v.upper()
    
    @validator('cpf')
    def validar_cpf(cls, v):
        """Valida CPF"""
        # Remover caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', v)
        
        if len(cpf) != 11:
            raise ValueError('CPF deve ter 11 dígitos')
        
        # Verificar se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            raise ValueError('CPF inválido')
        
        # Validar dígitos verificadores
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        if cpf[-2:] != f"{digito1}{digito2}":
            raise ValueError('CPF inválido')
        
        return cpf
    
    @validator('nome')
    def validar_nome(cls, v):
        """Valida nome do proprietário"""
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v.strip().title()
    
    @validator('modelo')
    def validar_modelo(cls, v):
        """Valida modelo do veículo"""
        if not re.match(r'^[a-zA-Z0-9\s\-\.]+$', v):
            raise ValueError('Modelo contém caracteres inválidos')
        return v.strip()

class FuncionarioCreate(BaseModel):
    """Modelo para criação de funcionário"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome do funcionário")
    matricula: str = Field(..., min_length=4, max_length=10, description="Matrícula do funcionário")
    email: Optional[EmailStr] = Field(None, description="Email do funcionário")
    telefone: Optional[str] = Field(None, description="Telefone do funcionário")
    
    @validator('matricula')
    def validar_matricula(cls, v):
        """Valida matrícula do funcionário"""
        if not re.match(r'^[0-9]{4,10}$', v):
            raise ValueError('Matrícula deve conter apenas números (4-10 dígitos)')
        return v
    
    @validator('telefone')
    def validar_telefone(cls, v):
        """Valida telefone"""
        if v is None:
            return v
        
        # Remover caracteres não numéricos
        telefone = re.sub(r'[^0-9]', '', v)
        
        if len(telefone) not in [10, 11]:
            raise ValueError('Telefone deve ter 10 ou 11 dígitos')
        
        return telefone

class EstacionamentoRequest(BaseModel):
    """Modelo para requisição de estacionamento"""
    placa: str = Field(..., description="Placa do veículo")
    matricula: str = Field(..., description="Matrícula do funcionário")
    
    @validator('placa')
    def validar_placa(cls, v):
        return v.upper().strip()
    
    @validator('matricula')
    def validar_matricula(cls, v):
        if not re.match(r'^[0-9]{4,10}$', v):
            raise ValueError('Matrícula inválida')
        return v

class LiberacaoRequest(BaseModel):
    """Modelo para requisição de liberação de vaga"""
    placa: str = Field(..., description="Placa do veículo")
    matricula: str = Field(..., description="Matrícula do funcionário")
    motivo: Optional[str] = Field(None, max_length=200, description="Motivo da liberação")
    
    @validator('placa')
    def validar_placa(cls, v):
        return v.upper().strip()

class LoginRequest(BaseModel):
    """Modelo para requisição de login"""
    matricula: str = Field(..., description="Matrícula do funcionário")
    senha: str = Field(..., min_length=1, description="Senha do funcionário")

class SupervisorLoginRequest(BaseModel):
    """Modelo para login do supervisor"""
    senha: str = Field(..., min_length=1, description="Senha do supervisor")

class VagaStatus(BaseModel):
    """Modelo para status de vaga"""
    numero: int = Field(..., ge=1, le=30, description="Número da vaga")
    tipo: str = Field(..., regex="^(comum|visitante)$", description="Tipo da vaga")
    ocupada: bool = Field(..., description="Status de ocupação")
    entrada: Optional[datetime] = Field(None, description="Horário de entrada")
    veiculo: Optional[dict] = Field(None, description="Informações do veículo")

class VeiculoInfo(BaseModel):
    """Modelo para informações do veículo"""
    placa: str = Field(..., description="Placa do veículo")
    nome: str = Field(..., description="Nome do proprietário")
    cpf: str = Field(..., description="CPF do proprietário")
    modelo: str = Field(..., description="Modelo do veículo")
    bloco: str = Field(..., description="Bloco do apartamento")
    apartamento: str = Field(..., description="Número do apartamento")
    tipo: str = Field(..., description="Tipo de usuário")
    data_cadastro: Optional[datetime] = Field(None, description="Data de cadastro")

class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    error: str = Field(..., description="Descrição do erro")
    details: Optional[str] = Field(None, description="Detalhes adicionais")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp do erro")
    code: Optional[str] = Field(None, description="Código do erro")

class SuccessResponse(BaseModel):
    """Modelo para respostas de sucesso"""
    message: str = Field(..., description="Mensagem de sucesso")
    data: Optional[dict] = Field(None, description="Dados retornados")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")

# Funções de validação auxiliares
def validar_placa_mercosul(placa: str) -> bool:
    """Valida se a placa está no formato Mercosul"""
    return bool(re.match(r'^[A-Z]{3}[0-9]{1}[A-Z0-9]{1}[0-9]{2}$', placa.upper()))

def validar_placa_antiga(placa: str) -> bool:
    """Valida se a placa está no formato antigo"""
    return bool(re.match(r'^[A-Z]{3}[0-9]{4}$', placa.upper()))

def formatar_cpf(cpf: str) -> str:
    """Formata CPF com pontos e hífen"""
    cpf_limpo = re.sub(r'[^0-9]', '', cpf)
    if len(cpf_limpo) == 11:
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    return cpf

def normalizar_nome(nome: str) -> str:
    """Normaliza nome (primeira letra maiúscula)"""
    return ' '.join(word.capitalize() for word in nome.strip().split())

