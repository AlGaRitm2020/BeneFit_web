from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class BodyFatCalculatorForm(FlaskForm):
    height = IntegerField('Рост, см', validators=[DataRequired()])
    gender = RadioField('Пол', choices=['Мужской', 'Женский'])
    waist = IntegerField('Обхват талии, см', validators=[DataRequired()])
    neck = IntegerField('Обхват шеи, см', validators=[DataRequired()])
    hip = IntegerField('Обхват бедер, см (учитывается только для женщин)', validators=[DataRequired()])
    submit = SubmitField('Рассчитать процент жира')
