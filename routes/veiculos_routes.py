from flask import Blueprint, request, jsonify
from services.veiculo_service import cadastrar_veiculo, listar_veiculos_cadastrados, buscar_veiculo_por_placa, normalizar_placa
from services.vaga_service import verificar_tempo_excedido
from estacionamento import (
    carregar_dados, salvar_dados,
    estacionar_veiculo_por_dados, liberar_vaga, remover_veiculo_por_cpf
)
from routes.funcionarios_routes import funcionarios_logados
from datetime import datetime
import pytz
from config import active_config
from utils.logging_config import setup_logger, log_operation, log_error

# Configurar logger
logger = setup_logger(__name__)

veiculos_bp = Blueprint('veiculos', __name__)

# Cadastro de veículo
@veiculos_bp.route('/cadastrar-veiculo', methods=['POST'])
def cadastrar_veiculo_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        cpf = data.get('cpf', '').strip()
        modelo = data.get('modelo', '').strip()
        nome = data.get('nome', '').strip()
        bloco = data.get('bloco', '').strip()
        apartamento = data.get('apartamento', '').strip()
        matricula_func = data.get('matricula', '').strip()
        
        # Validações básicas
        if not placa or not cpf or not matricula_func or not nome:
            return jsonify({'mensagem': 'Placa, CPF, matrícula e nome são obrigatórios!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        
        # Verificar se funcionário existe
        funcionario = next((f for f in funcionarios if f['matricula'] == matricula_func), None)
        if not funcionario:
            return jsonify({'mensagem': 'Funcionário não encontrado!'}), 403
            
        # Verificar se funcionário está logado
        if matricula_func not in funcionarios_logados:
            return jsonify({'mensagem': 'Funcionário precisa estar logado para cadastrar veículo!'}), 403
            
        # Cadastrar veículo
        resposta = cadastrar_veiculo(veiculos, placa, cpf, modelo, nome, bloco, apartamento)
        
        # Se cadastro foi bem-sucedido, registrar no histórico
        if "✅" in resposta:
            historico.append({
                'acao': 'cadastro_veiculo',
                'data': datetime.now(pytz.timezone("America/Sao_Paulo")).isoformat(),
                'matricula': matricula_func,
                'nome_funcionario': funcionario['nome'],
                'placa': normalizar_placa(placa),
                'nome_proprietario': nome,
                'cpf': cpf,
                'modelo': modelo,
                'bloco': bloco,
                'apartamento': apartamento
            })
            
            # Salvar dados apenas uma vez
            salvar_dados(veiculos, vagas, historico, funcionarios)
            logger.info(f"Veículo {normalizar_placa(placa)} cadastrado por {funcionario['nome']}")
            
        return jsonify({'mensagem': resposta})
        
    except Exception as e:
        logger.error(f"Erro ao cadastrar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Listar veículos
@veiculos_bp.route('/veiculos', methods=['GET'])
def listar_veiculos():
    try:
        veiculos, vagas, historico, funcionarios = carregar_dados()
        return jsonify(veiculos)
    except Exception as e:
        logger.error(f"Erro ao listar veículos: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Estacionar veículo
@veiculos_bp.route('/estacionar', methods=['POST'])
def estacionar():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not placa or not matricula:
            return jsonify({'mensagem': 'Placa e matrícula são obrigatórios!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        
        # Verificar veículo e funcionário
        veiculo = buscar_veiculo_por_placa(veiculos, placa)
        funcionario = next((f for f in funcionarios if f['matricula'] == matricula), None)
        
        if not veiculo:
            return jsonify({'mensagem': '❌ Veículo não cadastrado. Faça o cadastro primeiro.'}), 404
        if not funcionario:
            return jsonify({'mensagem': '❌ Funcionário não cadastrado.'}), 403
        if matricula not in funcionarios_logados:
            return jsonify({'mensagem': '❌ Funcionário precisa estar logado.'}), 403
            
        resposta = estacionar_veiculo_por_dados(placa, veiculos, vagas, historico)
        
        if "✅" in resposta:
            salvar_dados(veiculos, vagas, historico, funcionarios)
            logger.info(f"Veículo {normalizar_placa(placa)} estacionado por {funcionario['nome']}")
            
            # Buscar informações da vaga
            placa_normalizada = normalizar_placa(placa)
            vaga = next((v for v in vagas if v['ocupada'] and v['veiculo'] == placa_normalizada), None)
            hora_entrada = vaga['entrada'] if vaga else None
            numero_vaga = vaga['numero'] if vaga else None
            
            proprietario = {
                'cpf': veiculo['cpf'],
                'nome': veiculo['nome'],
                'bloco': veiculo['bloco'],
                'apartamento': veiculo['apartamento'],
                'hora_entrada': hora_entrada
            }
            
            return jsonify({'mensagem': resposta, 'proprietario': proprietario, 'vaga': numero_vaga})
        else:
            return jsonify({'mensagem': resposta}), 400
            
    except Exception as e:
        logger.error(f"Erro ao estacionar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Liberar veículo
@veiculos_bp.route('/liberar', methods=['POST'])
def liberar_veiculo():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        placa = data.get('placa', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not placa or not matricula:
            return jsonify({'mensagem': 'Placa e matrícula são obrigatórios!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        
        # Verificar veículo e funcionário
        veiculo = buscar_veiculo_por_placa(veiculos, placa)
        funcionario = next((f for f in funcionarios if f['matricula'] == matricula), None)
        
        if not veiculo:
            return jsonify({'mensagem': '❌ Veículo não cadastrado.'}), 404
        if not funcionario:
            return jsonify({'mensagem': '❌ Funcionário não cadastrado.'}), 403
        if matricula not in funcionarios_logados:
            return jsonify({'mensagem': '❌ Funcionário precisa estar logado.'}), 403
            
        resposta = liberar_vaga(placa, matricula, veiculos, vagas, historico, funcionarios)
        
        if "✅" in resposta:
            salvar_dados(veiculos, vagas, historico, funcionarios)
            logger.info(f"Veículo {normalizar_placa(placa)} liberado por {funcionario['nome']}")
            
            # Buscar hora de saída no histórico
            placa_normalizada = normalizar_placa(placa)
            saida = None
            for h in reversed(historico):
                if h.get('acao') == 'saida_veiculo' and h.get('placa') == placa_normalizada:
                    saida = h.get('data_saida')
                    break
                    
            proprietario = {
                'cpf': veiculo['cpf'],
                'nome': veiculo['nome'],
                'bloco': veiculo['bloco'],
                'apartamento': veiculo['apartamento'],
                'hora_saida': saida
            }
            
            return jsonify({'mensagem': resposta, 'proprietario': proprietario})
        else:
            return jsonify({'mensagem': resposta}), 400
            
    except Exception as e:
        logger.error(f"Erro ao liberar veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Remover veículo por CPF
@veiculos_bp.route('/remover-veiculo-cpf', methods=['POST'])
def remover_veiculo_cpf():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados não fornecidos!'}), 400
            
        cpf = data.get('cpf', '').strip()
        matricula = data.get('matricula', '').strip()
        
        if not cpf or not matricula:
            return jsonify({'mensagem': 'CPF e matrícula são obrigatórios!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        
        # Verificar se funcionário está logado
        if matricula not in funcionarios_logados:
            return jsonify({'mensagem': 'Funcionário precisa estar logado!'}), 403
            
        resposta = remover_veiculo_por_cpf(cpf, matricula, veiculos, vagas, historico, funcionarios)
        
        if "🗑️" in resposta:  # Remoção bem-sucedida
            salvar_dados(veiculos, vagas, historico, funcionarios)
            funcionario = next((f for f in funcionarios if f['matricula'] == matricula), None)
            if funcionario:
                logger.info(f"Veículo removido por CPF {cpf} por {funcionario['nome']}")
                
        return jsonify({'mensagem': resposta})
        
    except Exception as e:
        logger.error(f"Erro ao remover veículo: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Histórico por matrícula
@veiculos_bp.route('/historico-matricula')
def historico_matricula():
    try:
        matricula = request.args.get('matricula', '').strip()
        if not matricula:
            return jsonify({'mensagem': 'Matrícula é obrigatória!'}), 400
            
        veiculos, vagas, historico, funcionarios = carregar_dados()
        historico_filtrado = [h for h in historico if str(h.get('matricula', '')).strip() == matricula]
        
        return jsonify(historico_filtrado)
        
    except Exception as e:
        logger.error(f"Erro ao buscar histórico: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Listar status das vagas
@veiculos_bp.route('/vagas', methods=['GET'])
def listar_vagas():
    try:
        veiculos, vagas, historico, funcionarios = carregar_dados()
        return jsonify(vagas)
    except Exception as e:
        logger.error(f"Erro ao listar vagas: {e}")
        return jsonify({'mensagem': 'Erro interno do servidor!'}), 500

# Verificar tempo excedido
@veiculos_bp.route('/tempo-excedido', methods=['GET'])
def tempo_excedido():
    try:
        veiculos, vagas, historico, funcionarios = carregar_dados()
        excedidos = verificar_tempo_excedido(vagas)
        
        if not excedidos:
            return jsonify({
                'mensagem': '✅ Nenhuma vaga excedeu o tempo.',
                'excedidos': [],
                'veiculos_excedidos': []
            })
        else:
            mensagens = []
            veiculos_excedidos = []
            
            for excedido in excedidos:
                mensagens.append(f"⚠️ Vaga {excedido['numero']} com veículo {excedido['veiculo']} está há {excedido['horas']} horas!")
                
                # Buscar informações completas do veículo
                veiculo_info = next((v for v in veiculos if v['placa'] == excedido['veiculo']), None)
                if veiculo_info:
                    veiculos_excedidos.append({
                        'placa': excedido['veiculo'],
                        'nome': veiculo_info['nome'],
                        'vaga': excedido['numero'],
                        'tempo_excedido': excedido['horas'] * 60,  # Converter para minutos
                        'bloco': veiculo_info.get('bloco', ''),
                        'apartamento': veiculo_info.get('apartamento', '')
                    })
            
            return jsonify({
                'mensagem': '\n'.join(mensagens),
                'excedidos': excedidos,
                'veiculos_excedidos': veiculos_excedidos
            })
            
    except Exception as e:
        logger.error(f"Erro ao verificar tempo excedido: {e}")
        return jsonify({
            'mensagem': f'Erro ao verificar tempo excedido: {str(e)}',
            'excedidos': [],
            'veiculos_excedidos': []
        }), 500 