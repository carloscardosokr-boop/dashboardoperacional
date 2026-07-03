from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registro(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    mes = db.Column(db.String(20), nullable=False)

    filial = db.Column(db.String(20), nullable=False)

    cte = db.Column(db.Integer, nullable=False)

    peso = db.Column(db.Float, nullable=False)

    mercadoria = db.Column(db.Float, nullable=False)

    frete = db.Column(db.Float, nullable=False)