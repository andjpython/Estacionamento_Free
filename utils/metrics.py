"""
Sistema de métricas para monitoramento do Sistema de Estacionamento
"""
import time
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class MetricPoint:
    """Ponto de métrica com timestamp"""
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)

class MetricsCollector:
    """Coletor de métricas do sistema"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.lock = threading.Lock()
        
        # Métricas específicas do sistema
        self.system_metrics = {
            'veiculos_cadastrados': 0,
            'vagas_ocupadas': 0,
            'operacoes_por_minuto': 0,
            'tempo_medio_estacionamento': 0.0,
            'erros_por_hora': 0
        }
    
    def increment_counter(self, name: str, value: int = 1, labels: Optional[Dict[str, str]] = None):
        """Incrementa um contador"""
        with self.lock:
            key = self._format_key(name, labels)
            self.counters[key] += value
    
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Define valor de um gauge"""
        with self.lock:
            key = self._format_key(name, labels)
            self.gauges[key] = value
    
    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Registra valor em um histograma"""
        with self.lock:
            key = self._format_key(name, labels)
            self.histograms[key].append(value)
            
            # Manter apenas os últimos 1000 valores
            if len(self.histograms[key]) > 1000:
                self.histograms[key] = self.histograms[key][-1000:]
    
    def record_timing(self, name: str, duration: float, labels: Optional[Dict[str, str]] = None):
        """Registra tempo de execução"""
        self.record_histogram(f"{name}_duration", duration, labels)
    
    def _format_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Formata chave da métrica com labels"""
        if not labels:
            return name
        
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}[{label_str}]"
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Retorna resumo das métricas coletadas"""
        with self.lock:
            summary = {
                'timestamp': datetime.now().isoformat(),
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'system_metrics': dict(self.system_metrics),
                'histograms': {}
            }
            
            # Calcular estatísticas dos histogramas
            for name, values in self.histograms.items():
                if values:
                    summary['histograms'][name] = {
                        'count': len(values),
                        'min': min(values),
                        'max': max(values),
                        'avg': sum(values) / len(values),
                        'p95': self._percentile(values, 95),
                        'p99': self._percentile(values, 99)
                    }
            
            return summary
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calcula percentil de uma lista de valores"""
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def reset_metrics(self):
        """Reseta todas as métricas"""
        with self.lock:
            self.metrics.clear()
            self.counters.clear()
            self.gauges.clear()
            self.histograms.clear()

class MetricsMiddleware:
    """Middleware para coletar métricas automaticamente"""
    
    def __init__(self, app, metrics_collector: MetricsCollector):
        self.app = app
        self.metrics = metrics_collector
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        
        # Contar requisição
        self.metrics.increment_counter('http_requests_total', labels={
            'method': environ.get('REQUEST_METHOD', 'UNKNOWN'),
            'endpoint': environ.get('PATH_INFO', '/')
        })
        
        def custom_start_response(status, headers, exc_info=None):
            # Registrar status da resposta
            status_code = int(status.split()[0])
            self.metrics.increment_counter('http_responses_total', labels={
                'status_code': str(status_code)
            })
            
            # Registrar tempo de resposta
            duration = time.time() - start_time
            self.metrics.record_timing('http_request_duration', duration, labels={
                'endpoint': environ.get('PATH_INFO', '/')
            })
            
            return start_response(status, headers, exc_info)
        
        return self.app(environ, custom_start_response)

# Instância global do coletor de métricas
metrics_collector = MetricsCollector()

# Decorator para medir tempo de execução
def measure_time(metric_name: str, labels: Optional[Dict[str, str]] = None):
    """Decorator para medir tempo de execução de funções"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                metrics_collector.record_timing(metric_name, duration, labels)
        return wrapper
    return decorator
