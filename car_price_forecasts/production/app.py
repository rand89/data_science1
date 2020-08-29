from flask import Flask, render_template, request, redirect, flash, url_for
from forms import PredictionForm
from datetime import datetime
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '2020'

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
	form = PredictionForm()
	if form.validate_on_submit():
		brand = request.form['mark']
		bodyType = request.form['bodyType']
		fuelType = request.form['fuelType']
		productionDate = request.form['productionDate']
		modelDate = request.form['modelDate']
		numberOfDoors = request.form['numberOfDoors']
		vehicleTransmission = request.form['vehicleTransmission']
		engineDisplacement = request.form['engineDisplacement']
		enginePower = define_power_category(request.form['enginePower'])
		mileage = define_mileage_category(request.form['mileage'])
		drive = request.form['drive']
		owners = request.form['owners']
		empty_features = [0]*45
		
		with open('features.list', 'r') as filehandle:
			features = json.load(filehandle)

		work_features = [bodyType, brand, fuelType, modelDate, numberOfDoors, productionDate,
			vehicleTransmission, engineDisplacement, enginePower, mileage, drive, owners]
		
		df = pd.DataFrame([work_features + empty_features], columns=features)
		price = predict_price(df)
		write_logs(work_features, features[:12], price)
		flash(f'Цена автомобиля {form.mark.data.upper()} {price} руб.', 'success')
	return render_template('predict.html', title='Predict', form=form)

def predict_price(test):
    from_file = CatBoostRegressor()
    model = from_file.load_model("catboost.model")
    return round(model.predict(test)[0])

def define_mileage_category(mileage):
    mileage = int(mileage) / 5000
    if mileage > 100:
        category = 101
    else:
        category = np.ceil(mileage).astype('int32')
    return category

def define_power_category(power):
    power = int(power) / 25
    power = np.ceil(power).astype('int32')
    return power

def write_logs(features, feature_names, price):
    uid = str(round(time.time()))
    with open(f'output/{uid}_{features[1]}.txt', 'w') as output:
        text = list(zip(feature_names, features))
        text = str(text) + '; Цена: ' + str(price) + ' руб.'
        output.write(text)

if __name__ == "__main__":
	#app.run(debug=True)
	app.run('0.0.0.0', port=5000)