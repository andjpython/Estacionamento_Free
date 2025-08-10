import os
import pytz
from datetime import datetime

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

from db import SessionLocal
from repositories import VagaRepository, VeiculoRepository
from routes.supervisor_routes import supervisor_bp
from routes.funcionarios_routes import funcionarios_bp
from routes.veiculos_routes import veiculos_bp
from utils.csrf import init_csrf

app = Flask(__name__)
CORS(app)

# Configurar chave secreta para sessão e CSRF
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'seu_segredo_super_secreto_aqui')

# Inicializar CSRF
init_csrf(app)

app.register_blueprint(supervisor_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(veiculos_bp)

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
    try:
        db = SessionLocal()
        try:
            vaga_repo = VagaRepository(db)
            vagas = vaga_repo.get_vagas_completas()
            
            # Converter para dicionário e adicionar informações completas
            vagas_completas = []
            for vaga in vagas:
                vaga_info = {
                    'numero': vaga.numero,
                    'tipo': vaga.tipo,
                    'ocupada': vaga.ocupada,
                    'entrada': vaga.entrada.isoformat() if vaga.entrada else None
                }
                
                if vaga.ocupada and vaga.veiculo:
                    vaga_info['veiculo'] = vaga.veiculo.placa
                    vaga_info['proprietario'] = vaga.veiculo.nome
                    vaga_info['cpf'] = vaga.veiculo.cpf
                    vaga_info['modelo'] = vaga.veiculo.modelo
                    vaga_info['bloco'] = vaga.veiculo.bloco
                    vaga_info['apartamento'] = vaga.veiculo.apartamento
                else:
                    vaga_info['veiculo'] = None
                
                vagas_completas.append(vaga_info)
            
            return jsonify(vagas_completas)
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"Erro ao carregar vagas completas: {str(e)}")
        return jsonify({'mensagem': f'Erro ao carregar vagas completas: {str(e)}'}), 500

# ---------------------- EXECUÇÃO ----------------------
if __name__ == '__main__':
    app.run(debug=True)