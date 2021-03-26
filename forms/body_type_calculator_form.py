from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class BodyTypeCalculatorForm(FlaskForm):
    wrists = IntegerField('Обхват запястий, см', validators=[DataRequired()])
    gender = RadioField('Пол', choices=['Мужской', 'Женский'])
    submit = SubmitField('Рассчитать тип телосложения')
