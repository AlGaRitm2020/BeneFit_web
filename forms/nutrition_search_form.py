from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, IntegerField, SelectField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class NutritionSearchForm(FlaskForm):
    query = StringField('Введите название продукта', validators=[DataRequired()])
    submit = SubmitField('Получить информацию о продукте')
