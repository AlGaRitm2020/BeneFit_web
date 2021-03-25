from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class HeartRateCalculatorForm(FlaskForm):
    age = IntegerField('Возраст, лет', validators=[DataRequired()])


    submit = SubmitField('Рассчитать ЧСС')
