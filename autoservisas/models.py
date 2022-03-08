from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from sqlalchemy import DateTime 
from autoservisas import db

class Vartotojas(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column('Vartotojo vardas', db.String(200), unique=True, nullable=False)
    el_pastas = db.Column('El.paštas', db.String(200), unique=True, nullable=False)
    slaptazodis = db.Column('Slaptažodis', db.String(200), nullable=False)
    masinos = db.relationship('Car', cascade="all,delete", backref='vartotojas')
    is_admin = db.Column(db.Boolean(), default=False)
    is_employee = db.Column(db.Boolean(), default=False)

    def __repr__(self) -> str:
        return self.vardas


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sukurta = db.Column('Sukurta', DateTime, default=datetime.utcnow())
    modelis = db.Column('Modelis', db.String(200), nullable=False)
    marke = db.Column('Markė', db.String(200), nullable=False)
    gaminimo_metai = db.Column('Metai', db.Integer, nullable=False)
    variklis = db.Column('Variklis', db.String(200), nullable=False)
    valst_numeris = db.Column('Valstybinis numeris', db.String(200), nullable=False)
    vin = db.Column('VIN', db.String(17), nullable=False)
    vartotojas_id = db.Column(db.Integer, db.ForeignKey('vartotojas.id'))
    gedimai = db.relationship('Gedimas', cascade='all,delete', backref='car')
    
    def __repr__(self) -> str:
        return f'{self.modelis} {self.marke} {self.gaminimo_metai}'


class Gedimas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sukurta = db.Column('Sukurta', DateTime, default=datetime.utcnow())
    gedimas = db.Column('Gedimas', db.String(200), default=False)
    gedimo_busena = db.Column('Gedimo būsena', db.String(200), default=False)
    gedimo_kaina = db.Column('Gedimo kaina', db.String(200), default=False)
    masina_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    
    def __repr__(self) -> str:
        return f'{self.gedimas}'


class AdminModel(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
