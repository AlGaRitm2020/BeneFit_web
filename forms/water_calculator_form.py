from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class WaterCalculatorForm(FlaskForm):
    gender = RadioField('Пол', choices=['Мужской', 'Женский'])
    weight = IntegerField('Вес', validators=[DataRequired()])
    activity = SelectField(u'Укажите ваш уровень физической активности',
                           choices=[('Очень низкая', 0), ('Низкая', 1), ('Средняя', 2), ('Высокая', 3),
                                    ('Очень высокая', 4)],
                           validators=[DataRequired()])
    # remember_me = BooleanField('Рассчитать процент жира')
    submit = SubmitField('Рассчитать ИМТ')