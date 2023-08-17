from marshmallow import Schema, fields

class ClienteSchema(Schema):
    cpf = fields.Str(required=True)
    nome = fields.Str(required=True)
    email = fields.Str(required=True)
    dataDeNascimento = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True)
    genero = fields.Str(required=True)
    rendaMensal = fields.Float(required=True)

class ProdutoSchema(Schema):
    nome = fields.Str(required=True)
    susep = fields.Str(required=True)
    expiracaoDeVenda = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True)
    valorMinimoAporteInicial = fields.Float(required=True)
    valorMinimoAporte = fields.Float(required=True)
    idadeDeEntrada = fields.Int(required=True)
    idadeDeSaida = fields.Int(required=True)
    carenciaInicialDeResgate = fields.Int(required=True)
    carenciaEntreResgates = fields.Int(required=True)

class PlanoSchema(Schema):
    cliente_id = fields.Int(required=True)
    produto_id = fields.Int(required=True)
    aporte = fields.Float(required=True)
    dataDaContratacao = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True)
    idadeDeAposentadoria = fields.Int(required=True)

class AporteSchema(Schema):
    idCliente = fields.Int(required=True)
    idPlano = fields.Int(required=True)
    valorAporte = fields.Float(required=True)

class ResgateSchema(Schema):
    idPlano = fields.Int(required=True)
    valorResgate = fields.Float(required=True)
