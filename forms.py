from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    year = SelectField('Année', choices = [('2021', '2021'), ('2020', '2020')], validators=[DataRequired()])
    sexe = SelectField('Sexe', choices = [('Tous', 'Tous'), ('Homme', 'Homme'), ('Femme', 'Femme')], validators=[DataRequired()])
    submit = SubmitField('Sign In')