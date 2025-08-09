// Configurações globais do timer do sistema de estacionamento
// NOTA: Sincronizado com config.py - LIMITE_HORAS_ESTACIONAMENTO
const TIMER_CONFIG = {
  // Tempo limite em horas (sincronizado com backend)
  LIMITE_HORAS: 72,
  
  // Intervalos de atualização
  INTERVALO_TIMER: 1000, // 1 segundo
  INTERVALO_AUTO_UPDATE: 30000, // 30 segundos
  
  // Porcentagens para alertas
  PORCENTAGEM_WARNING: 25, // Amarelo quando restam 25%
  PORCENTAGEM_CRITICAL: 10, // Vermelho quando restam 10%
  
  // Formatação
  FORMATO_DATA: 'pt-BR',
  
  // Mensagens
  MENSAGENS: {
    TEMPO_ESGOTADO: 'TEMPO ESGOTADO',
    CARREGANDO: 'Carregando...',
    ERRO_TIMER: 'Erro no timer'
  }
};

// Função utilitária para calcular milissegundos do limite
function obterLimiteEmMillis() {
  return TIMER_CONFIG.LIMITE_HORAS * 60 * 60 * 1000;
}

// Exportar configurações para uso global
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TIMER_CONFIG;
} 