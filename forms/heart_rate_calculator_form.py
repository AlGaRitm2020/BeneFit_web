from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class HeartRateCalculatorForm(FlaskForm):
    age = IntegerField('Рост', validators=[DataRequired()])



    # remember_me = BooleanField('Рассчитать процент жира')
    submit = SubmitField('Рассчитать ИМТ')
