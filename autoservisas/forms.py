from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from autoservisas import models

class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email('Neteisingas el.paštas.')])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    patvirtinimas = PasswordField('Pakartokite slaptažodį', [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired(), Email('Neteisingas el.paštas.')])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')


class ProfilioForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email('Neteisingas el.paštas.')])
    is_admin = BooleanField('Adminas')
    is_employee = BooleanField('Darbuotojas')
    submit = SubmitField('Atnaujinti')
    

    def tikrinti_varda(self, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')

class CarForma(FlaskForm):
    modelis = StringField('Modelis', [DataRequired()])
    marke = StringField('Markė', [DataRequired()])
    gaminimo_metai = IntegerField('Gaminimo Metai', [DataRequired()])
    variklis = StringField('Variklis', [DataRequired()])
    valst_numeris = StringField('Valstybinis Numeris', [DataRequired()])
    vin = StringField('VIN Numeris', [DataRequired()])
    submit = SubmitField('Užsirašyti')

def user_car_query():
    return models.Car.query.filter_by(vartotojas_id = current_user.id)

class GedimoForma(FlaskForm):
    masina = QuerySelectField(
        query_factory=user_car_query,
        allow_blank=True,
        get_label=lambda obj: str(f'{obj.modelis} {obj.marke} {obj.gaminimo_metai}'),
        get_pk=lambda obj: str(obj)
        )
    gedimas = StringField('Gedimo Aprašymas', [DataRequired()])
    submit = SubmitField('Išsaugoti')
