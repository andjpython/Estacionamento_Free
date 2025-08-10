// === Funções de Autenticação ===

// Função para fazer requisições AJAX autenticadas
async function fazerRequisicaoAutenticada(url, dados = null, metodo = 'GET') {
  try {
    const opcoes = {
      method: metodo,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    // Adicionar token JWT se disponível
    const token = localStorage.getItem('authToken');
    if (token) {
      opcoes.headers['Authorization'] = `Bearer ${token}`;
    }

    if (dados) {
      opcoes.body = JSON.stringify(dados);
    }

    const resposta = await fetch(url, opcoes);
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
