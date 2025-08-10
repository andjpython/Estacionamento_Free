// === Funções do Modal de Login ===

// Função para abrir o modal
function abrirModalLogin() {
  const modal = document.getElementById('modalLogin');
  if (modal) {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; // Previne scroll da página
    atualizarBotaoSistemaCompleto(); // Atualizar estado do botão ao abrir modal
  }
}

// Função para fechar o modal
function fecharModalLogin() {
  const modal = document.getElementById('modalLogin');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto'; // Restaura scroll da página
    // Limpar campos do formulário
    const matriculaInput = document.getElementById('matriculaFuncionario');
    const senhaInput = document.getElementById('senhaSupervisor');
    if (matriculaInput) matriculaInput.value = '';
    if (senhaInput) senhaInput.value = '';
  }
}

// Fechar modal ao clicar fora dele
window.onclick = function(event) {
  const modal = document.getElementById('modalLogin');
  if (event.target === modal) {
    fecharModalLogin();
  }
}

// Fechar modal com tecla ESC
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    fecharModalLogin();
  }
});
