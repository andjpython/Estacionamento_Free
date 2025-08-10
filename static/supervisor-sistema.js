// Funções do Supervisor
let supervisorLogado = false;

// Função para marcar supervisor como logado
function marcarSupervisorLogado() {
    supervisorLogado = true;
    verificarAcessoSistema();
}

// Função para marcar supervisor como deslogado
function marcarSupervisorDeslogado() {
    supervisorLogado = false;
    localStorage.removeItem('authToken');
    verificarAcessoSistema();
}

// Função para verificar acesso ao sistema
function verificarAcessoSistema() {
    const sistemaNaoLogado = document.querySelector('.sistema-nao-logado');
    const sistemaLogado = document.querySelector('.sistema-logado');
    
    if (supervisorLogado) {
        sistemaNaoLogado.style.display = 'none';
        sistemaLogado.style.display = 'block';
    } else {
        sistemaNaoLogado.style.display = 'block';
        sistemaLogado.style.display = 'none';
    }
}

// Função para fazer logout do supervisor
async function logoutSupervisor() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) {
            console.log('Token não encontrado, redirecionando...');
            window.location.href = '/';
            return;
        }

        console.log('Iniciando logout...');
        const response = await fetch('/logout-supervisor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                'X-CSRFToken': window.csrfToken || ''
            }
        });

        // Verifica se a resposta é JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            console.error('Resposta não é JSON:', contentType);
            throw new Error('Resposta inválida do servidor');
        }

        const dados = await response.json();
        console.log('Resposta do servidor:', dados);

        if (response.ok) {
            localStorage.removeItem('authToken');
            marcarSupervisorDeslogado();
            window.location.href = '/';
        } else {
            if (response.status === 401) {
                console.log('Token expirado ou inválido');
                localStorage.removeItem('authToken');
                window.location.href = '/';
            } else {
                console.error('Erro no logout:', dados);
                alert(dados.mensagem || 'Erro ao fazer logout');
            }
        }
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
        localStorage.removeItem('authToken'); // Remove o token por segurança
        window.location.href = '/';
    }
}

// Adicionar event listeners quando o documento estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Botão de logout do supervisor
    const btnLogoutSupervisor = document.querySelector('.logout-supervisor');
    if (btnLogoutSupervisor) {
        btnLogoutSupervisor.addEventListener('click', logoutSupervisor);
    }
    
    // Verificar se supervisor está logado (tem token)
    const token = localStorage.getItem('authToken');
    if (token) {
        marcarSupervisorLogado();
    } else {
        marcarSupervisorDeslogado();
    }
});