# 🅿️ Sistema de Estacionamento Rotativo - Recantos das Flores I

Sistema profissional para gestão de estacionamento rotativo em condomínios, desenvolvido com Python (Flask), HTML5, CSS3 e JavaScript. Arquitetura modular, responsiva e segura, seguindo boas práticas de desenvolvimento.

---

## ✨ Funcionalidades Principais

### 🔐 **Controle de Acesso**
- Login/logout de funcionários com controle de sessão
- Área restrita do supervisor com senha configurável
- Auditoria completa de todas as operações

### 🚗 **Gestão de Veículos**
- Cadastro com validação de CPF e placas (antigo/Mercosul)
- Suporte a moradores e visitantes
- Sistema de tipos automático baseado no modelo

### 🅿️ **Controle de Vagas**
- 20 vagas comuns (moradores) + 10 visitantes
- Timer regressivo em tempo real (72h limite)
- Alertas visuais por cores (verde/amarelo/vermelho)
- Auto-refresh e cleanup de memória

### 📊 **Relatórios e Histórico**
- Histórico completo de operações
- Relatórios de tempo excedido
- Listagem de veículos e funcionários
- Logs estruturados para auditoria

### 🎨 **Interface Moderna**
- Design responsivo (mobile-first)
- Layout institucional profissional
- Animações CSS suaves
- Feedback imediato de operações

---

## 🏗️ Arquitetura Refatorada (v2.1.0)

### Estrutura Modular

```
📁 estacionamento_rotativo1
├── app.py                # Backend Flask (registra blueprints)
├── estacionamento.py     # Lógica principal de negócio
├── supervisor.py         # Funções de supervisão (terminal)
├── routes/               # Blueprints Flask (rotas)
│   ├── supervisor_routes.py
│   ├── funcionarios_routes.py
│   └── veiculos_routes.py
├── services/             # Lógica de negócio modularizada
│   ├── veiculo_service.py
│   ├── funcionario_service.py
│   ├── vaga_service.py
│   └── historico_service.py
├── models/               # (Reservado para modelos de dados)
├── dados/                # Dados persistentes em JSON
│   ├── vagas.json
│   ├── veiculos.json
│   ├── historico.json
│   └── funcionarios.json
├── static/
│   ├── style.css         # Estilo institucional e responsivo
│   ├── script.js         # JS moderno e integrado
│   └── imagens/          # Logos, fotos, imagens flutuantes
├── templates/
│   └── index.html        # Layout institucional e profissional
└── README.md
```

---

## 📸 Capturas de Tela

> **Adicione prints do sistema rodando aqui!**

---

## 📦 Como executar o projeto

1. Clone o repositório:
```bash
git clone <URL_DO_REPOSITORIO>
cd estacionamento_rotativo1
```
2. Instale as dependências:
```bash
pip install flask flask-cors
```
3. Defina a senha do supervisor (opcional):
```bash
set SENHA_SUPERVISOR=suasenha
```
4. Execute o sistema:
```bash
python app.py
```
5. Acesse no navegador:
```
http://127.0.0.1:5000/
```

---

## 🔐 Supervisor
- Acesso ao painel do supervisor (terminal ou web)
- Senha padrão: `290479` (ou variável de ambiente)
- Ações: cadastrar/remover funcionários, ver histórico, listar veículos

---

## 📋 Documentação

- **README.md**: Documentação principal do projeto
- **CHANGELOG.md**: Histórico de mudanças e versões
- **requirements.txt**: Dependências do projeto

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usar, estudar, adaptar e compartilhar.

---

## ✍️ Autor

Anderson Jacinto da Silveira  
Aluno de Engenharia de Software – UNIASSELVI