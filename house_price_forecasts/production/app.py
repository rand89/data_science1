from flask import Flask, render_template, request, redirect, flash, url_for
from forms import PredictionForm
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = '2020'
forest_reg = joblib.load('forest_reg_best.compressed')

with open('scaler.pkl', 'rb') as pkl_file:
	scaler = pickle.load(pkl_file)

with open('zipcodes.pkl', 'rb') as pkl_file:
	zipcodes = pickle.load(pkl_file)

@app.route('/')
def index():
	return render_template('index.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
	form = PredictionForm()
	if form.validate_on_submit():
		sqft = request.form['sqft']
		sqft_log = np.log(int(sqft))
		baths_num = set_baths(request.form['baths_num'])
		beds_num = set_beds(request.form['beds_num'])
		story = set_story(request.form['story'])
		age = set_age(request.form['age'])
		schools_num = set_schools(request.form['schools_num'])
		schools_8_up = check_select(request.form['schools_8_up'])
		zipcode = int(request.form['zipcode'])
		zipcode_expensive = set_zipcode(zipcode)
		condo = check_select(request.form['condo'])
		mobile = check_select(request.form['mobile'])

		feature_names = ['sqft_log', 'zipcode_expensive', 'zipcode',
			'age', 'baths_num', 'schools_8_up', 'story', 'Condo',
			'beds_num', 'schools_num', 'mobile']

		work_features = [sqft_log, zipcode_expensive, zipcode,
			age, baths_num, schools_8_up, story, condo,
			beds_num, schools_num, mobile]
		
		x_test = pd.DataFrame([work_features], columns=feature_names)
		x_test = scaler.transform(x_test)
		price = predict_price(x_test)
		flash(f'Прогнозируемая цена {price} $', 'success')
	return render_template('predict.html', title='Predict', form=form)

def predict_price(test):
	y_pred = forest_reg.predict(test)
	return round(np.exp(y_pred[0]))

def set_baths(baths_num):
    baths_num = int(baths_num)
    if baths_num > 6:
        baths_num = 6
    elif baths_num < 1:
        baths_num = 1
    return baths_num

def set_beds(beds_num):
    beds_num = int(beds_num)
    if beds_num > 7:
        beds_num = 7
    elif beds_num < 1:
        beds_num = 1
    return beds_num

def set_story(story):
    story = int(story)
    if story > 5:
        story = 5
    elif story < 1:
        story = 1
    return story

def set_age(age):
    age = int(age)
    if age > 138:
        age = 138
    elif age < 0:
        age = 0
    return age

def set_schools(schools_num):
    schools_num = int(schools_num)
    if schools_num > 7:
        schools_num = 7
    elif schools_num < 0:
        schools_num = 0
    return schools_num

def set_zipcode(zipcode):
    if zipcode in zipcodes:
        return 1
    return 0

def check_select(value):
    try:
        value = int(value)
        if value != 0 and value != 1:
            return 0
        else:
            return value
    except:
        return 0

if __name__ == "__main__":
	#app.run(debug=True)
	app.run()