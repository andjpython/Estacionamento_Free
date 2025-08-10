// === Funções de Login ===

// Função para fazer login do funcionário
async function loginFuncionario(matricula) {
  try {
    const response = await fetch('/login-funcionario', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(window.csrfToken ? { 'X-CSRFToken': window.csrfToken } : {})
      },
      body: JSON.stringify({ matricula })
    });

    const dados = await response.json();
    return { sucesso: response.ok, dados };
  } catch (erro) {
    return { sucesso: false, dados: { mensagem: 'Erro de conexão com o servidor' } };
  }
}

// Configurar formulário de login do funcionário
function configurarLoginFuncionario() {
  const form = document.getElementById('loginFuncionarioForm');
  if (!form) return;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Validar formulário
    if (!window.utils.validarFormulario(this)) {
      window.utils.mostrarErro('Preencha todos os campos obrigatórios');
      return;
    }
    
    const matricula = document.getElementById('matriculaFuncionario').value.trim();
    
    // Validar matrícula
    if (!window.utils.validarMatricula(matricula)) {
      window.utils.mostrarErro('Matrícula deve ter 4 dígitos');
      return;
    }
    
    // Mostrar loading
    const btnSubmit = this.querySelector('button[type="submit"]');
    window.utils.mostrarLoading(btnSubmit);
    
    try {
      const { sucesso, dados } = await loginFuncionario(matricula);
      
      if (sucesso) {
        localStorage.setItem('matriculaLogada', matricula);
        window.atualizarFuncionariosLogados();
        window.verificarAcessoSistema();
        atualizarBotaoSistemaCompleto();
        window.fecharModalLogin();
        window.utils.mostrarErro(dados.mensagem, 'success');
      } else {
        window.utils.mostrarErro(dados.mensagem);
      }
    } catch (err) {
      window.utils.mostrarErro('Erro de conexão com o servidor');
    } finally {
      window.utils.ocultarLoading(btnSubmit);
      document.getElementById('matriculaFuncionario').value = '';
    }
  });
}

// Função para atualizar visibilidade do botão de sistema completo
function atualizarBotaoSistemaCompleto() {
  const matriculaLogada = localStorage.getItem('matriculaLogada');
  const sistemaNaoLogado = document.getElementById('sistemaNaoLogado');
  const sistemaLogado = document.getElementById('sistemaLogado');
  
  if (matriculaLogada) {
    if (sistemaNaoLogado) sistemaNaoLogado.style.display = 'none';
    if (sistemaLogado) sistemaLogado.style.display = 'block';
  } else {
    if (sistemaNaoLogado) sistemaNaoLogado.style.display = 'block';
    if (sistemaLogado) sistemaLogado.style.display = 'none';
  }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
  configurarLoginFuncionario();
  atualizarBotaoSistemaCompleto(); // Verificar estado inicial
});
