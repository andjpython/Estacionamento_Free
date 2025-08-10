# Sistema de Estacionamento Rotativo - Recantos das Flores I

## Sumário
1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Funcionalidades](#funcionalidades)
4. [Configuração](#configuração)
5. [API e Integrações](#api-e-integrações)
6. [Segurança](#segurança)
7. [Interface do Usuário](#interface-do-usuário)
8. [Desenvolvimento](#desenvolvimento)
9. [Manutenção](#manutenção)

## Visão Geral

### Descrição
Sistema de gestão de estacionamento rotativo desenvolvido para o condomínio Recantos das Flores I, oferecendo controle completo de vagas, veículos e usuários.

### Principais Características
- Gestão de vagas para moradores e visitantes
- Controle de tempo de permanência
- Interface responsiva e intuitiva
- Sistema de alertas em tempo real
- Registro completo de operações

### Tecnologias Principais
- Backend: Python 3.10+ com Flask 2.3.3
- Frontend: HTML5, CSS3, JavaScript ES6+
- Banco de Dados: PostgreSQL
- ORM: SQLAlchemy
- Migrações: Alembic

## Arquitetura

### Estrutura de Diretórios
```
estacionamento_rotativo/
├── app/
│   ├── services/         # Regras de negócio
│   ├── models/          # Modelos de dados
│   ├── routes/          # Endpoints da API
│   └── utils/           # Utilitários
├── static/              # Recursos estáticos
├── templates/           # Templates HTML
├── tests/              # Testes automatizados
├── alembic/            # Migrações
└── config/             # Configurações
```

### Camadas do Sistema
1. **Apresentação**: Interface web responsiva
2. **API**: Endpoints REST para operações
3. **Serviços**: Lógica de negócio
4. **Persistência**: Banco de dados PostgreSQL

## Funcionalidades

### Gestão de Veículos

#### Tipos e Regras
- **Moradores**
  - Acesso às vagas 1-20
  - Cadastro com modelo do veículo obrigatório
  - Identificação por placa e CPF

- **Visitantes**
  - Acesso às vagas 21-30
  - Cadastro simplificado
  - Tempo máximo de permanência: 72h

#### Validações
- Placa: Formatos ABC1234 ou ABC1D23 (Mercosul)
- CPF: Validação completa dos dígitos
- Dados normalizados automaticamente

### Sistema de Vagas

#### Configuração
- 20 vagas para moradores (1-20)
- 10 vagas para visitantes (21-30)
- Monitoramento em tempo real
- Sistema de alertas visual

#### Estados
- **Livre**: Disponível para uso
- **Ocupada**: Com registro de entrada
- **Em alerta**: Próximo ao limite de tempo

### Controle de Acesso

#### Níveis de Usuário
1. **Funcionários**
   - Cadastro de veículos
   - Operações de entrada/saída
   - Consulta de status

2. **Supervisor**
   - Gestão de funcionários
   - Relatórios gerenciais
   - Configurações do sistema

## Configuração

### Variáveis de Ambiente
```bash
# Banco de Dados
DATABASE_URL=postgresql://user:pass@localhost:5432/parking

# Ambiente
FLASK_ENV=production
SENHA_SUPERVISOR=hash_da_senha
```

### Parâmetros do Sistema
```python
# config.py
LIMITE_HORAS = 72
VAGAS_COMUNS = 20
VAGAS_VISITANTES = 10
INTERVALO_ATUALIZACAO = 30  # segundos
```

## API e Integrações

### Endpoints Principais
- `POST /veiculos`: Cadastro de veículos
- `POST /estacionar`: Registro de entrada
- `POST /liberar`: Registro de saída
- `GET /vagas`: Status do estacionamento

### Formato de Dados
```json
{
  "veiculo": {
    "placa": "ABC1234",
    "tipo": "morador",
    "entrada": "2025-01-10T14:30:00-03:00"
  }
}
```

## Segurança

### Autenticação
- Sessões de funcionários com timeout
- Senha do supervisor hasheada
- Validação em múltiplas camadas

### Auditoria
- Logs detalhados de operações
- Histórico de alterações
- Rastreamento de responsabilidades

## Interface do Usuário

### Design Responsivo
- Layout adaptativo
- Compatível com dispositivos móveis
- Acessibilidade WCAG 2.1

### Componentes
- Dashboard de status
- Formulários de operação
- Sistema de notificações
- Timer regressivo

## Desenvolvimento

### Requisitos
- Python 3.10+
- PostgreSQL 12+
- Node.js 16+ (build)

### Instalação
```bash
# Ambiente virtual
python -m venv venv
source venv/bin/activate

# Dependências
pip install -r requirements.txt

# Banco de dados
alembic upgrade head
```

### Testes
```bash
# Unitários
pytest tests/unit

# Integração
pytest tests/integration
```

## Manutenção

### Monitoramento
- Logs estruturados
- Métricas de uso
- Alertas automáticos

### Backup
- Banco de dados: diário
- Configurações: versionadas
- Logs: retenção de 90 dias

### Atualizações
1. Backup dos dados
2. Aplicar migrações
3. Atualizar dependências
4. Testes de regressão

---

## Informações do Projeto
- **Versão**: 2.1.0
- **Desenvolvedor**: Anderson Jacinto da Silveira
- **Contato**: [E-mail de Suporte]
- **Última Atualização**: Janeiro 2025

## Licença
Todos os direitos reservados. Uso exclusivo do Condomínio Recantos das Flores I.