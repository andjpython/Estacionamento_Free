// === Funções Utilitárias ===

// Validação de matrícula (4 dígitos)
function validarMatricula(matricula) {
  return /^\d{4}$/.test(matricula);
}

// Feedback visual durante requisições
function mostrarLoading(elemento) {
  elemento.classList.add('loading');
  elemento.disabled = true;
}

function ocultarLoading(elemento) {
  elemento.classList.remove('loading');
  elemento.disabled = false;
}

// Tratamento de erros amigável
function mostrarErro(mensagem, tipo = 'error') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${tipo}`;
  toast.textContent = mensagem;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
}

// Retry em caso de erro de rede
async function retryFetch(url, options, maxRetries = 3) {
  let lastError;
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response;
    } catch (error) {
      lastError = error;
      await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
    }
  }
  throw lastError;
}

// Validação de formulários
function validarFormulario(form) {
  const inputs = form.querySelectorAll('input[required]');
  let valido = true;
  inputs.forEach(input => {
    if (!input.value.trim()) {
      input.classList.add('invalid');
      valido = false;
    } else {
      input.classList.remove('invalid');
    }
  });
  return valido;
}

// Acessibilidade
function melhorarAcessibilidade() {
  // Adicionar roles e aria-labels
  document.querySelectorAll('button').forEach(btn => {
    if (!btn.getAttribute('aria-label')) {
      btn.setAttribute('aria-label', btn.textContent.trim());
    }
  });
  
  // Adicionar feedback de foco
  document.querySelectorAll('a, button, input').forEach(el => {
    el.addEventListener('focus', () => el.classList.add('focused'));
    el.addEventListener('blur', () => el.classList.remove('focused'));
  });
}

// Expor funções globalmente
window.utils = {
  validarMatricula,
  mostrarLoading,
  ocultarLoading,
  mostrarErro,
  retryFetch,
  validarFormulario,
  melhorarAcessibilidade
};

