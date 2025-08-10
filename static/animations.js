// === Funções de Animação ===

function iniciarAnimacao() {
  // Adicionar classe de animação ao header
  const header = document.querySelector('.banner-condominio');
  if (header) {
    header.classList.add('animate-fade-in');
  }

  // Animar seções conforme scroll
  const sections = document.querySelectorAll('section');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in');
      }
    });
  }, { threshold: 0.1 });

  sections.forEach(section => {
    observer.observe(section);
  });

  // Animar elementos do painel
  const painelHorario = document.getElementById('painel-horario');
  const funcionariosBox = document.getElementById('funcionariosLogadosBox');

  if (painelHorario) {
    painelHorario.classList.add('animate-slide-in');
  }
  if (funcionariosBox) {
    funcionariosBox.classList.add('animate-slide-in');
  }
}

// Adicionar estilos de animação
const animationStyle = document.createElement('style');
animationStyle.textContent = `
  .animate-fade-in {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeIn 0.8s ease forwards;
  }

  .animate-slide-in {
    opacity: 0;
    transform: translateX(-20px);
    animation: slideIn 0.8s ease forwards;
  }

  @keyframes fadeIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes slideIn {
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
`;
document.head.appendChild(animationStyle);
