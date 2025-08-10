// === Funções de Autenticação ===

// Verificar se token JWT está expirado
function tokenExpirado(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return Date.now() >= payload.exp * 1000;
  } catch (e) {
    return true;
  }
}

// Função para fazer requisições AJAX autenticadas
async function fazerRequisicaoAutenticada(url, dados = null, metodo = 'GET') {
  try {
    const token = localStorage.getItem('authToken');
    if (token && tokenExpirado(token)) {
      localStorage.removeItem('authToken');
      window.location.href = '/';
      return null;
    }

    const opcoes = {
      method: metodo,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    // Adicionar token JWT se disponível
    if (token) {
      opcoes.headers['Authorization'] = `Bearer ${token}`;
    }

    // Adicionar CSRF token se disponível
    const csrfToken = window.csrfToken || document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken) {
      opcoes.headers['X-CSRFToken'] = csrfToken;
    }

    if (dados) {
      opcoes.body = JSON.stringify(dados);
    }

    const resposta = await window.utils.retryFetch(url, opcoes);
    const resultado = await resposta.json();
    
    // Se receber erro de autenticação, limpar token e redirecionar para login
    if (resposta.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/';
      return null;
    }
    
    return { sucesso: resposta.ok, dados: resultado };
  } catch (erro) {
    return { sucesso: false, dados: { mensagem: 'Erro de conexão: ' + erro.message } };
  }
}

// Função para verificar se o usuário está autenticado
function verificarAutenticacao() {
  const token = localStorage.getItem('authToken');
  return !!token;
}

// Função para fazer logout
function fazerLogout() {
  localStorage.removeItem('authToken');
  window.location.href = '/';
}

// Expor funções globalmente
window.auth = {
  fazerRequisicaoAutenticada,
  verificarAutenticacao,
  fazerLogout
};
