from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class CalculatorForm(FlaskForm):
    height = IntegerField('Рост', validators=[DataRequired()])
    weight = IntegerField('Вес', validators=[DataRequired()])

    # remember_me = BooleanField('Рассчитать процент жира')
    submit = SubmitField('Рассчитать ИМТ')