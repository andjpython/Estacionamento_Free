import os
import pytz
from datetime import datetime

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from estacionamento import (
    carregar_dados,
    salvar_dados
)
from routes.supervisor_routes import supervisor_bp
from routes.funcionarios_routes import funcionarios_bp
from routes.veiculos_routes import veiculos_bp

app = Flask(__name__)
CORS(app)

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
        veiculos, vagas, historico, funcionarios = carregar_dados()
        
        # Adicionar informações completas dos veículos
        vagas_completas = []
        for vaga in vagas:
            vaga_info = vaga.copy()
            if vaga['ocupada'] and vaga['veiculo']:
                # Buscar informações do veículo
                veiculo_info = next((v for v in veiculos if v['placa'] == vaga['veiculo']), None)
                if veiculo_info:
                    vaga_info['proprietario'] = veiculo_info['nome']
                    vaga_info['cpf'] = veiculo_info['cpf']
                    vaga_info['modelo'] = veiculo_info['modelo']
                    vaga_info['bloco'] = veiculo_info['bloco']
                    vaga_info['apartamento'] = veiculo_info['apartamento']
            
            vagas_completas.append(vaga_info)
        
        return jsonify(vagas_completas)
    except Exception as e:
        print(f"Erro ao carregar vagas completas: {str(e)}")
        return jsonify({'mensagem': f'Erro ao carregar vagas completas: {str(e)}'}), 500

# ---------------------- EXECUÇÃO ----------------------
if __name__ == '__main__':
    app.run(debug=True)


