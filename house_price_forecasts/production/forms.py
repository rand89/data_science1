from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class PredictionForm(FlaskForm):

   sqft = IntegerField('Площадь (кв. футы)', default='1500', validators=[DataRequired(), NumberRange(0)])
   baths_num = IntegerField('Количество ванных комнат', default='2', validators=[DataRequired()])
   beds_num = IntegerField('Количество спальных комнат', default='2', validators=[DataRequired()])
   story = IntegerField('Количество этажей', default='1', validators=[DataRequired()])
   age = IntegerField('Возраст дома (лет)', default='1', validators=[DataRequired()])
   schools_num = IntegerField('Количество школ поблизости', default='3', validators=[DataRequired()])
   schools_8_up = SelectField(u'Наличие школы с высоким рейтингом', validators=[DataRequired()], choices=[(['0', 'Нет']), (['1', 'Да'])])
   zipcode = IntegerField('Почтовый индекс', default='91352', validators=[DataRequired(), NumberRange(100, 100000)])
   condo = SelectField(u'Это кондоминиум', validators=[DataRequired()], choices=[(['0', 'Нет']), (['1', 'Да'])])
   mobile = SelectField(u'Это переносной дом', validators=[DataRequired()], choices=[(['0', 'Нет']), (['1', 'Да'])])
   submit = SubmitField('Оценить')
