"""
Configurações centralizadas do Sistema de Estacionamento Rotativo
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# === CONFIGURAÇÕES GERAIS ===
class Config:
    # Diretórios
    BASE_DIR = Path(__file__).parent
    
    # === BANCO DE DADOS ===
    # URL do banco. Para PostgreSQL, use:
    # postgresql+psycopg2://USUARIO:SENHA@HOST:PORTA/NOME_BANCO
    # Driver padrão atualizado para psycopg (v3)
    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/estacionamento_rotativo"
    )
    
    # === REGRAS DE NEGÓCIO ===
    # Limite de tempo em horas (3 dias)
    LIMITE_HORAS_ESTACIONAMENTO = 72
    
    # Tipos de vagas disponíveis
    TIPOS_VAGA = ["comum", "visitante"]
    
    # Quantidade de vagas por tipo
    VAGAS_COMUNS = 20
    VAGAS_VISITANTES = 10
    
    # === CONFIGURAÇÕES DE TIMER ===
    # Intervalos em milissegundos
    INTERVALO_TIMER = 1000  # 1 segundo
    INTERVALO_AUTO_UPDATE = 30000  # 30 segundos
    
    # Porcentagens para alertas visuais
    PORCENTAGEM_WARNING = 25  # Amarelo quando restam 25%
    PORCENTAGEM_CRITICAL = 10  # Vermelho quando restam 10%
    
    # === SEGURANÇA ===
    # Senha do supervisor (variável de ambiente ou padrão)
    # Se a senha não estiver hasheada, será hasheada na primeira execução
    SENHA_SUPERVISOR = os.environ.get("SENHA_SUPERVISOR", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqxbQNoqFEa9VNm")  # Hash de "290479"
    
    # Chave secreta para tokens JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "seu_segredo_super_secreto_aqui")
    
    # Tempo de expiração do token JWT (em minutos)
    JWT_EXPIRATION_MINUTES = 60
    
    # === TIMEZONE ===
    TIMEZONE = os.environ.get("TZ", "America/Sao_Paulo")
    
    # === LOGGING ===
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # === MENSAGENS ===
    class Mensagens:
        # Sucessos
        VEICULO_CADASTRADO = "✅ Veículo {placa} cadastrado como {tipo}."
        VEICULO_ESTACIONADO = "✅ Veículo {placa} estacionado na vaga {numero} ({tipo})."
        VEICULO_LIBERADO = "✅ Veículo {placa} saiu da vaga {numero}. Tempo: {tempo} min."
        FUNCIONARIO_CADASTRADO = "✅ Funcionário {nome} cadastrado com matrícula {matricula}."
        LOGIN_REALIZADO = "🔓 Funcionário {nome} entrou."
        LOGOUT_REALIZADO = "🔒 Funcionário {nome} saiu."
        
        # Erros
        VEICULO_JA_CADASTRADO = "❌ Veículo já cadastrado com essa placa."
        VEICULO_NAO_CADASTRADO = "❌ Veículo não cadastrado."
        VEICULO_JA_ESTACIONADO = "⚠️ Este veículo já está estacionado."
        PLACA_INVALIDA = "❌ Placa inválida. Use formato ABC1234 ou ABC1D23."
        CPF_INVALIDO = "❌ CPF inválido. Verifique os dígitos."
        NOME_OBRIGATORIO = "❌ Nome do proprietário é obrigatório."
        VAGA_NAO_DISPONIVEL = "🚫 Nenhuma vaga disponível para tipo {tipo}."
        MATRICULA_INVALIDA = "❌ Matrícula inválida. Deve conter 4 dígitos."
        FUNCIONARIO_NAO_ENCONTRADO = "❌ Funcionário não encontrado."
        SENHA_INCORRETA = "❌ Acesso negado. Senha do supervisor incorreta!"
        DADOS_NAO_FORNECIDOS = "❌ Dados não fornecidos!"
        ERRO_INTERNO = "❌ Erro interno do servidor!"
        ERRO_BANCO = "❌ Erro ao acessar o banco de dados: {mensagem}"
        
        # Informativos
        NENHUM_VEICULO_CADASTRADO = "📭 Nenhum veículo cadastrado."
        NENHUMA_VAGA_CADASTRADA = "📭 Nenhuma vaga cadastrada."
        NENHUM_FUNCIONARIO_CADASTRADO = "📭 Nenhum funcionário cadastrado."
        TEMPO_ESGOTADO = "💥 TEMPO ESGOTADO"
        CARREGANDO = "⏳ Carregando..."

# === CONFIGURAÇÕES DE DESENVOLVIMENTO ===
class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"

# === CONFIGURAÇÕES DE PRODUÇÃO ===
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"
    
# === Configuração ativa ===
# Por padrão usa desenvolvimento, mas pode ser alterado via variável de ambiente
config_name = os.environ.get('FLASK_ENV', 'development')
if config_name == 'production':
    active_config = ProductionConfig()
else:
    active_config = DevelopmentConfig()

    