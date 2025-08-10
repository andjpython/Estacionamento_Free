import os
import pytz
from datetime import datetime

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from utils.logger import system_logger
from utils.metrics import metrics_collector, MetricsMiddleware
from utils.rate_limiter import limiter

import os
from db import SessionLocal, init_db
from repositories import VagaRepository, VeiculoRepository
from routes.supervisor_routes import supervisor_bp, login_supervisor as login_supervisor_view
from routes.funcionarios_routes import funcionarios_bp, login_funcionario as login_funcionario_view
from routes.veiculos_routes import veiculos_bp
from utils.csrf import init_csrf

app = Flask(__name__)
CORS(app)

# Middleware de métricas
app.wsgi_app = MetricsMiddleware(app.wsgi_app, metrics_collector)  # type: ignore

# Rate limiter
limiter.init_app(app)

# Inicialização automática do banco (para ambientes como Render)
if os.environ.get('AUTO_INIT_DB', '1') == '1':
    try:
        init_db()
    except Exception as e:
        # Não derruba a aplicação por falha de criação inicial
        system_logger.error("Falha ao inicializar DB automaticamente", extra={"extra_data": {"erro": str(e)}})

# Configurar chave secreta para sessão e CSRF
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'seu_segredo_super_secreto_aqui')

# Inicializar CSRF
init_csrf(app)

app.register_blueprint(supervisor_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(veiculos_bp)

# Rotas diretas de fallback para evitar problemas de blueprint em alguns ambientes
app.add_url_rule(
    '/login-funcionario',
    view_func=login_funcionario_view,
    methods=['POST'],
    endpoint='login_funcionario_fallback'
)
app.add_url_rule(
    '/login-supervisor',
    view_func=login_supervisor_view,
    methods=['POST'],
    endpoint='login_supervisor_fallback'
)

# ---------------------- ROTAS PRINCIPAIS ----------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sistema')
def sistema():
    return render_template('sistema.html')

@app.route('/supervisor')
def supervisor_area():
    return render_template('supervisor.html', nome_supervisor='Anderson J Silveira')

@app.route('/supervisor-sistema')
def supervisor_sistema():
    return render_template('supervisor_sistema.html', nome_supervisor='Anderson J Silveira')

@app.route('/vagas-completas', methods=['GET'])
def listar_vagas_completas():
    """Lista todas as vagas com informações completas"""
    db = None
    try:
        db = SessionLocal()
        vaga_repo = VagaRepository(db)
        
        # Buscar vagas
        try:
            vagas = vaga_repo.get_vagas_completas()
        except Exception as e:
            print(f"Erro ao buscar vagas: {str(e)}")
            return jsonify({'mensagem': 'Erro ao buscar vagas no banco de dados'}), 500
        
        # Converter para dicionário
        vagas_completas = []
        for vaga in vagas:
            try:
                # Informações básicas da vaga
                # Converter valores das colunas SQLAlchemy
                try:
                    numero = vaga.numero.scalar() if hasattr(vaga.numero, 'scalar') else vaga.numero
                    tipo = vaga.tipo.scalar() if hasattr(vaga.tipo, 'scalar') else vaga.tipo
                    ocupada = vaga.ocupada.scalar() if hasattr(vaga.ocupada, 'scalar') else vaga.ocupada
                    entrada = vaga.entrada.scalar() if hasattr(vaga.entrada, 'scalar') else vaga.entrada
                except Exception as e:
                    print(f"Erro ao converter valores da vaga: {str(e)}")
                    numero = None
                    tipo = 'indefinido'
                    ocupada = False
                    entrada = None

                # Converter e validar valores
                tipo_str = str(tipo) if tipo is not None else 'indefinido'
                ocupada_bool = False
                if isinstance(ocupada, bool):
                    ocupada_bool = ocupada
                elif hasattr(ocupada, 'scalar'):
                    try:
                        ocupada_bool = bool(ocupada.scalar())
                    except:
                        ocupada_bool = False

                entrada_str = None
                if entrada is not None:
                    if hasattr(entrada, 'isoformat'):
                        entrada_str = entrada.isoformat()
                    elif hasattr(entrada, 'scalar'):
                        try:
                            entrada_val = entrada.scalar()
                            if entrada_val and hasattr(entrada_val, 'isoformat'):
                                entrada_str = entrada_val.isoformat()
                        except:
                            entrada_str = None

                vaga_info = {
                    'numero': numero,
                    'tipo': tipo_str,
                    'ocupada': ocupada_bool,
                    'entrada': entrada_str,
                    'veiculo': None
                }
                
                # Adicionar informações do veículo se ocupada
                if ocupada_bool and vaga.veiculo:
                    # Converter valores das colunas do veículo
                    def get_value(attr):
                        """Extrai valor de um atributo SQLAlchemy ou valor normal"""
                        if attr is None:
                            return None
                        try:
                            if hasattr(attr, 'scalar'):
                                return attr.scalar()
                            return attr
                        except:
                            return None

                    try:
                        veiculo_info = {
                            'placa': get_value(vaga.veiculo.placa),
                            'proprietario': get_value(vaga.veiculo.nome),
                            'cpf': get_value(vaga.veiculo.cpf),
                            'modelo': get_value(vaga.veiculo.modelo),
                            'bloco': get_value(vaga.veiculo.bloco),
                            'apartamento': get_value(vaga.veiculo.apartamento)
                        }
                        
                        # Converter valores para string se não forem None
                        vaga_info['veiculo'] = {
                            k: str(v) if v is not None else None
                            for k, v in veiculo_info.items()
                        }
                    except Exception as e:
                        print(f"Erro ao converter valores do veículo: {str(e)}")
                        vaga_info['veiculo'] = {
                            'placa': None,
                            'proprietario': None,
                            'cpf': None,
                            'modelo': None,
                            'bloco': None,
                            'apartamento': None
                        }
                
                vagas_completas.append(vaga_info)
                
            except Exception as e:
                print(f"Erro ao processar vaga {vaga.numero if vaga else 'desconhecida'}: {str(e)}")
                continue  # Pular vaga com erro e continuar
        
        # Verificar se alguma vaga foi processada
        if not vagas_completas:
            return jsonify({'mensagem': 'Nenhuma vaga encontrada ou erro ao processar todas as vagas'}), 404
            
        response = {
            'status': 'success',
            'total_vagas': len(vagas_completas),
            'vagas': vagas_completas
        }
        system_logger.info("Listagem de vagas completa", extra={"extra_data": {"total_vagas": len(vagas_completas)}})
        return jsonify(response)
        
    except Exception as e:
        print(f"Erro ao carregar vagas completas: {str(e)}")
        return jsonify({
            'status': 'error',
            'mensagem': 'Erro interno ao processar vagas',
            'erro': str(e)
        }), 500
        
    finally:
        if db:
            db.close()

# ---------------------- MÉTRICAS ----------------------
@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(metrics_collector.get_metrics_summary())

# Health HTTP
@app.route('/healthz', methods=['GET'])
def healthz():
    try:
        from db import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "fail", "erro": str(e)}), 500

# ---------------------- EXECUÇÃO ----------------------
if __name__ == '__main__':
    app.run(debug=True)