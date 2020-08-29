from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo
from datetime import datetime, date

class PredictionForm(FlaskForm):
    my_list = ['bmw', 'mercedes', 'volkswagen', 'kia', 'hyundai', 'vaz',
        'nissan', 'ford', 'toyota', 'audi', 'skoda', 'opel',
        'chevrolet', 'mitsubishi', 'mazda', 'renault', 'land_rover', 'volvo',
        'peugeot', 'honda', 'infiniti', 'lexus', 'citroen', 'subaru',
        'porsche', 'ssang_yong', 'suzuki', 'gaz', 'daewoo', 'jeep',
        'mini', 'saab', 'acura', 'cadillac', 'jaguar', 'haval',
        'lifan', 'geely', 'ravon', 'seat', 'alfa_romeo', 'isuzu']
    mark = SelectField(u'Марка', validators=[DataRequired()], choices=[(x,x) for x in my_list])
    
    my_list = ['седан', 'хэтчбек 5 дв.', 'внедорожник 5 дв.', 'купе',
       'компактвэн', 'лифтбек', 'родстер', 'седан 2 дв.', 'кабриолет',
       'универсал 5 дв.', 'хэтчбек 3 дв.', 'купе-хардтоп', 'минивэн',
       'внедорожник 3 дв.', 'пикап двойная кабина', 'лимузин',
       'внедорожник открытый', 'фургон', 'пикап одинарная кабина',
       'хэтчбек 4 дв.', 'пикап полуторная кабина', 'микровэн', 'тарга',
       'седан-хардтоп', 'фастбек']
    bodyType = SelectField(u'Тип кузова', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    my_list = ['бензин', 'дизель', 'электро', 'гибрид', 'газ']
    fuelType = SelectField(u'Тип топлива', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    productionDate = DateField('Год производства', default=date.today(), format='%Y', validators=[DataRequired()])
    modelDate = DateField('Год модели', default=date.today(), format='%Y', validators=[DataRequired()])

    my_list = ['4', '5', '2', '3']
    numberOfDoors = SelectField(u'Количество дверей', validators=[DataRequired()], choices=[(x,x) for x in my_list])
    
    my_list = ['механическая', 'автоматическая', 'роботизированная', 'вариатор']
    vehicleTransmission = SelectField(u'Коробка передач', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    my_list = ['2.0 LTR', '2.5 LTR', '1.6 LTR', '6.0 LTR', '4.4 LTR', '1.5 LTR',
       '3.0 LTR', '4.8 LTR', '3.3 LTR', '5.0 LTR', 'undefined LTR',
       '3.8 LTR', '4.0 LTR', '6.6 LTR', '1.9 LTR', '2.9 LTR', '2.2 LTR',
       '1.8 LTR', '5.4 LTR', '2.8 LTR', '2.4 LTR', '4.6 LTR', '3.4 LTR',
       '1.7 LTR', '3.5 LTR', '3.6 LTR', '4.9 LTR', '2.3 LTR', '4.7 LTR',
       '2.1 LTR', '1.3 LTR', '4.2 LTR', '5.5 LTR', '6.2 LTR', '4.3 LTR',
       '3.2 LTR', '5.8 LTR', '5.6 LTR', '1.4 LTR', '2.6 LTR', '3.7 LTR',
       '2.7 LTR', '1.2 LTR', '1.1 LTR', '1.0 LTR', '4.1 LTR', '0.8 LTR',
       '0.7 LTR', '4.5 LTR', '3.9 LTR', '5.2 LTR', '6.8 LTR', '6.1 LTR',
       '5.7 LTR', '6.3 LTR', '5.9 LTR', '3.1 LTR', '5.3 LTR', '7.0 LTR',
       '6.5 LTR', '8.1 LTR', '7.5 LTR', '7.4 LTR', '6.4 LTR']
    engineDisplacement = SelectField(u'Объем двигателя', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    enginePower = IntegerField('Мощность двигателя (л. с.)', default='100', validators=[DataRequired()])
    mileage = IntegerField('Пробег (км)', default='50000', validators=[DataRequired()])

    my_list = ['задний', 'полный', 'передний']
    drive = SelectField(u'Привод', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    my_list = ['1 владелец', '2 владельца', '3 или более']
    owners = SelectField(u'Владельцы', validators=[DataRequired()], choices=[(x,x) for x in my_list])

    submit = SubmitField('Оценить')
