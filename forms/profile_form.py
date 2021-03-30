from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    weight = IntegerField('Вес, кг', validators=[DataRequired()])
    height = IntegerField('Рост, см', validators=[DataRequired()])
    age = IntegerField('Возраст, лет', validators=[DataRequired()])
    gender = RadioField('Пол', choices=['Мужской', 'Женский'])

    activity = SelectField(u'Укажите ваш уровень физической активности',
                           choices=[(0, 'Сидячий образ жизни'),
                                    (1, 'Редкие тренировки'),
                                    (2, 'Тренировки 3 - 4 раза в неделю'),
                                    (3, 'Тренировки 5 - 6 раз в неделю'),
                                    (4, 'Ежедневные интенсивные тренировки')],
                           validators=[DataRequired()])

    wrists = IntegerField('Обхват запястий, см', validators=[DataRequired()])
    waist = IntegerField('Обхват талии, см', validators=[DataRequired()])
    neck = IntegerField('Обхват шеи, см', validators=[DataRequired()])
    hip = IntegerField('Обхват бедер, см (учитывается только для женщин)',
                       validators=[DataRequired()])
    # remember_me = BooleanField('Рассчитать процент жира')
    submit = SubmitField('Сохранить')
