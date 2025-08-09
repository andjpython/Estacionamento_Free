# Sistema de Estacionamento Rotativo

Sistema de gerenciamento de estacionamento desenvolvido em Python com Flask e PostgreSQL.

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Dependências Python listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/estacionamento-rotativo.git
cd estacionamento-rotativo
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:

   a. Crie um arquivo `.env` baseado no `.env.example`:
   ```bash
   cp env.example .env
   ```
   
   b. Edite o `.env` com suas configurações:
   ```
   DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/estacionamento
   FLASK_ENV=development
   SENHA_SUPERVISOR=sua_senha_aqui
   ```

5. Crie o banco de dados:
```bash
createdb estacionamento
```

6. Execute as migrations:
```bash
alembic upgrade head
```

7. Popule o banco com dados iniciais:
```bash
python scripts/seed.py
```

## Executando o Sistema

1. Inicie o servidor Flask:
```bash
flask run
```

2. Acesse no navegador:
```
http://localhost:5000
```

## Estrutura do Projeto

- `alembic/` - Migrations do banco de dados
- `models/` - Modelos ORM SQLAlchemy
- `repositories/` - Camada de acesso ao banco de dados
- `routes/` - Rotas da API Flask
- `services/` - Lógica de negócio
- `static/` - Arquivos estáticos (CSS, JS, imagens)
- `templates/` - Templates HTML
- `utils/` - Utilitários e configurações

## Funcionalidades

- Cadastro e gestão de veículos
- Controle de vagas (comuns e visitantes)
- Registro de entrada/saída
- Histórico de operações
- Gestão de funcionários
- Interface web responsiva
- API REST

## Desenvolvimento

Para contribuir com o projeto:

1. Crie uma branch para sua feature:
```bash
git checkout -b feature/nova-funcionalidade
```

2. Faça suas alterações e commit:
```bash
git commit -m "Adiciona nova funcionalidade"
```

3. Envie um pull request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.