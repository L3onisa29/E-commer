from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo

class Registration_form(FlaskForm):
    user = StringField(label='Username', validators=[DataRequired(), Length(2, 20)])
    pass_ = PasswordField(label='Password', validators=[DataRequired()])
    pass_confirm = PasswordField(label='Confirm password', validators=[DataRequired(), EqualTo('pass_')])
    submit = SubmitField(label='Registrazione')


class Login_form(FlaskForm):
    user = StringField(label='Username', validators=[DataRequired(), Length(2, 20)])
    pass_ = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Accedi')


class Prodotto_form(FlaskForm):
    nome = StringField(label='Nome prodotto', validators=[DataRequired(), Length(2, 20)])
    produttore = StringField(label='Produttore', validators=[DataRequired(), Length(2, 20)])
    prezzo = FloatField(label='Prezzo', validators=[DataRequired(), Length(0, 1000000)])
    categoria = StringField(label='Categoria', validators=[DataRequired()])
    scorta = IntegerField(label='Scorta', validators=[DataRequired(), Length(1, 1000000)])
    submit = SubmitField(label='Carica articolo')