from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
import uuid

ma = Marshmallow()


db = SQLAlchemy()


class Cliente(db.Model):
    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dataDeNascimento = db.Column(db.DateTime, nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    rendaMensal = db.Column(db.Float, nullable=False)


class Produto(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    susep = db.Column(db.String(50), unique=True, nullable=False)
    expiracaoDeVenda = db.Column(db.DateTime, nullable=False)
    valorMinimoAporteInicial = db.Column(db.Float, nullable=False)
    valorMinimoAporte = db.Column(db.Float, nullable=False)
    idadeDeEntrada = db.Column(db.Integer, nullable=False)
    idadeDeSaida = db.Column(db.Integer, nullable=False)
    carenciaInicialDeResgate = db.Column(db.Integer, nullable=False)
    carenciaEntreResgates = db.Column(db.Integer, nullable=False)


class Plano(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(
        uuid.uuid4()))  
    dataDaContratacao = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    saldo = db.Column(db.Float, nullable=False, default=0)
    idadeDeAposentadoria = db.Column(db.Integer, nullable=False)
    cliente_id = db.Column(db.String(36), nullable=False)
    produto_id = db.Column(db.String(36), nullable=False)


class Aporte(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    plano_id = db.Column(db.String(36), db.ForeignKey(
        'plano.id'), nullable=False)


class Resgate(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor = db.Column(db.Float, nullable=False)
    plano_id = db.Column(db.String(36), db.ForeignKey(
        'plano.id'), nullable=False)