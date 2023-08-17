from flask import Blueprint, jsonify, request
from flask_apispec import use_kwargs, marshal_with
from app.data_schemas import ClienteSchema, ProdutoSchema, PlanoSchema, AporteSchema, ResgateSchema
from app.models import Cliente, Produto, Plano, Aporte, Resgate, db
from datetime import datetime, timedelta, timezone
from app.models import Plano, Produto, Resgate

api = Blueprint('api', __name__)


@api.route('/cadastro/cliente', methods=['POST'])
def cadastro_cliente():
    try:
        dados = request.json

        campos_obrigatorios = ["cpf", "nome", "email",
                               "dataDeNascimento", "genero", "rendaMensal"]
        if not all(key in dados for key in campos_obrigatorios):
            campos_faltantes = [
                campo for campo in campos_obrigatorios if campo not in dados]
            return jsonify({"error": f"Dados inválidos, os campos {', '.join(campos_faltantes)} são obrigatórios"}), 400

        novo_cliente = Cliente(
            cpf=dados["cpf"],
            nome=dados["nome"],
            email=dados["email"],
            dataDeNascimento=datetime.strptime(
                dados["dataDeNascimento"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            genero=dados["genero"],
            rendaMensal=dados["rendaMensal"]
        )
        db.session.add(novo_cliente)
        db.session.commit()

        return jsonify({"id": str(novo_cliente.id)}), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500


@api.route('/cadastro/produto', methods=['POST'])
def cadastro_produto():
    try:
        dados = request.json

        campos_obrigatorios = ["nome", "susep", "expiracaoDeVenda", "valorMinimoAporteInicial",
                               "valorMinimoAporte", "idadeDeEntrada", "idadeDeSaida",
                               "carenciaInicialDeResgate", "carenciaEntreResgates"]
        if not all(key in dados for key in campos_obrigatorios):
            campos_faltantes = [
                campo for campo in campos_obrigatorios if campo not in dados]
            return jsonify({"error": f"Dados inválidos, os campos {', '.join(campos_faltantes)} são obrigatórios"}), 400

        novo_produto = Produto(
            nome=dados["nome"],
            susep=dados["susep"],
            expiracaoDeVenda=datetime.strptime(
                dados["expiracaoDeVenda"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            valorMinimoAporteInicial=dados["valorMinimoAporteInicial"],
            valorMinimoAporte=dados["valorMinimoAporte"],
            idadeDeEntrada=dados["idadeDeEntrada"],
            idadeDeSaida=dados["idadeDeSaida"],
            carenciaInicialDeResgate=dados["carenciaInicialDeResgate"],
            carenciaEntreResgates=dados["carenciaEntreResgates"]
        )
        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({"id": str(novo_produto.id)}), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500


@api.route('/contratacao/plano', methods=['POST'])
def contratacao_plano():
    try:
        dados = request.json

        campos_obrigatorios = ["cliente_id", "produto_id",
                               "aporte", "dataDaContratacao", "idadeDeAposentadoria"]
        if not all(key in dados for key in campos_obrigatorios):
            campos_faltantes = [
                campo for campo in campos_obrigatorios if campo not in dados]
            return jsonify({"error": f"Dados inválidos, os campos {', '.join(campos_faltantes)} são obrigatórios"}), 400

        produto = Produto.query.get(dados["produto_id"])
        if not produto:
            return jsonify({"error": "Produto não encontrado"}), 404

        if produto.expiracaoDeVenda < datetime.now():
            return jsonify({"error": "Produto com prazo de venda expirado"}), 400

        cliente = Cliente.query.get(dados["cliente_id"])
        if not cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404

        data_contratacao = datetime.strptime(
            dados["dataDaContratacao"], '%Y-%m-%dT%H:%M:%S.%fZ')

        idade_cliente_na_contratacao = (
            data_contratacao - cliente.dataDeNascimento).days // 365

        if idade_cliente_na_contratacao < produto.idadeDeEntrada:
            return jsonify({"error": f"Cliente não atende a idade mínima de entrada que é {produto.idadeDeEntrada} anos."}), 400

        if cliente.rendaMensal < produto.valorMinimoAporteInicial:
            return jsonify({"error": "Cliente não atende ao valor mínimo de aporte inicial"}), 400

        novo_plano = Plano(
            cliente_id=dados["cliente_id"],
            produto_id=dados["produto_id"],
            saldo=dados["aporte"],
            dataDaContratacao=data_contratacao,
            idadeDeAposentadoria=dados["idadeDeAposentadoria"]
        )
        db.session.add(novo_plano)
        db.session.commit()

        return jsonify({"id": str(novo_plano.id)}), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500


@api.route('/aporte', methods=['POST'])
def aporte():
    try:
        dados = request.json

        if not all(key in dados for key in ["idCliente", "idPlano", "valorAporte"]):
            return jsonify({"error": "Dados inválidos, os campos idCliente, idPlano e valorAporte são obrigatórios"}), 400

        plano = Plano.query.get(dados["idPlano"])
        if not plano:
            return jsonify({"error": "Plano não encontrado"}), 404

        cliente = Cliente.query.get(dados["idCliente"])
        if not cliente or cliente.id != plano.cliente_id:
            return jsonify({"error": "Cliente não encontrado ou não corresponde ao plano"}), 404

        produto = Produto.query.get(plano.produto_id)
        if not produto:
            return jsonify({"error": "Produto não encontrado"}), 404

        if dados["valorAporte"] < produto.valorMinimoAporte:
            return jsonify({"error": f"O valor do aporte deve ser maior ou igual a {produto.valorMinimoAporte}"}), 400

        plano.saldo += dados["valorAporte"]
        db.session.add(plano)

        novo_aporte = Aporte(
            plano_id=dados["idPlano"], valor=dados["valorAporte"])
        db.session.add(novo_aporte)

        db.session.commit()

        return jsonify({"id": str(novo_aporte.id)}), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao processar a requisição: {str(e)}"}), 500


@api.route('/resgate', methods=['POST'])
def resgate():
    data = request.json
    plano_id = data['idPlano']
    valor_resgate = data['valorResgate']

    plano = Plano.query.get(plano_id)
    if not plano:
        return jsonify({'error': 'Plano não encontrado'}), 404

    produto = Produto.query.get(plano.produto_id)

    data_contratacao_utc = plano.dataDaContratacao.astimezone(timezone.utc)

    data_fim_carencia_inicial = data_contratacao_utc + \
        timedelta(days=produto.carenciaInicialDeResgate)
    print(f"Data de fim de carência inicial: {data_fim_carencia_inicial}")

    if datetime.now(timezone.utc) < data_fim_carencia_inicial:
        return jsonify({'error': 'Período de carência inicial não satisfeito'}), 400

    ultimo_resgate = Resgate.query.filter_by(
        plano_id=plano_id).order_by(Resgate.data.desc()).first()

    if ultimo_resgate:
        data_fim_carencia_resgates = ultimo_resgate.data.astimezone(
            timezone.utc) + timedelta(days=produto.carenciaEntreResgates)
        print(
            f"Data de fim de carência entre resgates: {data_fim_carencia_resgates}")
        if datetime.now(timezone.utc) < data_fim_carencia_resgates:
            return jsonify({'error': 'Período de carência entre resgates não satisfeito'}), 400

    if plano.saldo < valor_resgate:
        return jsonify({'error': 'Saldo insuficiente'}), 400

    novo_resgate = Resgate(
        plano_id=plano_id, valor=valor_resgate, data=datetime.now(timezone.utc))
    db.session.add(novo_resgate)
    db.session.commit()

    return jsonify({'id': novo_resgate.id})