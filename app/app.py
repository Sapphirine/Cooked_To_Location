from flask import Flask, render_template, jsonify, request, redirect
from yelpDB import *
from hist import *
from spark_classification import *
import requests




app = Flask(__name__)



@app.route("/homepage")
def home_page():
    return render_template('index_homepage.html')


@app.route("/location")
def location_page():
    return render_template('location.html')

@app.route("/location/recommend2", methods = ['POST'])


def rmd_location():

	db = minidatabase('data/yelpDB')


	zipcode = str(request.form['zipcode'])
	foodtype = str(request.form['foodtype'])

	if zipcode == '':
		zipcode_2 = 'null'
	else:
		zipcode_2 = int(zipcode)

	foodtype_2 = foodtype

	if foodtype_2 == 'Coffee & Tea':
		foodtype_2 = 'coffee'
	if foodtype_2 == 'Ice Cream & Frozen Yogurt':
		foodtype_2 = 'ice_cream'
	if foodtype_2 == 'Steakhouses':
		foodtype_2 = 'steak'

	foodtype_3 = foodtype_2.lower().replace(' ', '_')


	result = db.recommend_locations(foodtype_3, zipcode_2)
	hist = histogram(result[1], [str(zipcode_2)])

	rest_1_name = result[0][0][0]
	rest_1_addr = result[0][0][1]
	rest_1_rate = result[0][0][6]

	rest_2_name = result[0][1][0]
	rest_2_addr = result[0][1][1]
	rest_2_rate = result[0][1][6]

	rest_3_name = result[0][2][0]
	rest_3_addr = result[0][2][1]
	rest_3_rate = result[0][2][6]

	rest_4_name = result[0][3][0]
	rest_4_addr = result[0][3][1]
	rest_4_rate = result[0][3][6]

	rest_5_name = result[0][4][0]
	rest_5_addr = result[0][4][1]
	rest_5_rate = result[0][4][6]

	zip_1 = result[1][0][0]
	zip_2 = result[1][1][0]
	zip_3 = result[1][2][0]
	zip_4 = result[1][3][0]
	zip_5 = result[1][4][0]

	def zip_to_coor(zipcode):

		params = {
					"address": zipcode,
					"key":  "AIzaSyAE5i-SzXCyvzvCzdTfdzFak9P2N54Lkys"
		}
		coor = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params = params)
		coor = coor.json()
		lat = coor['results'][0]['geometry']['location']['lat']
		lng = coor['results'][0]['geometry']['location']['lng']
		addr = coor['results'][0]['formatted_address']
		coor_r = [lat, lng, addr]

		return coor_r


	cor_1 = zip_to_coor(zip_1)
	cor_2 = zip_to_coor(zip_2)
	cor_3 = zip_to_coor(zip_3)
	cor_4 = zip_to_coor(zip_4)
	cor_5 = zip_to_coor(zip_5)

	db.commit()
	db.close()

	return render_template('rmd_location.html', zipcode = zipcode, foodtype = foodtype, result = result, hist = hist, 
							rest_1_name = rest_1_name, rest_1_addr = rest_1_addr, rest_1_rate = rest_1_rate,
							rest_2_name = rest_2_name, rest_2_addr = rest_2_addr, rest_2_rate = rest_2_rate,
							rest_3_name = rest_3_name, rest_3_addr = rest_3_addr, rest_3_rate = rest_3_rate,
							rest_4_name = rest_4_name, rest_4_addr = rest_4_addr, rest_4_rate = rest_4_rate,
							rest_5_name = rest_5_name, rest_5_addr = rest_5_addr, rest_5_rate = rest_5_rate,
							cor_1 = cor_1, cor_2 = cor_2, cor_3 = cor_3, cor_4 = cor_4, cor_5 = cor_5)




@app.route("/cuisine")
def cuisine_page():

	return render_template('cuisine.html')


@app.route("/cuisine/recommend", methods = ['POST'])

def rmd_cusine():

	db = minidatabase('data/yelpDB')

	zipcode = str(request.form['zipcode'])

	lat = ''
	lng = ''



	if zipcode != '':
		zipcode_1 = int(zipcode)
		result = db.recommend_cuisines(zipcode_1)
		hist = histogram(result[1], [str(zipcode)])
	else:
		lat = float(request.form['lat'])
		lng = float(request.form['lng'])
		result = db.recommend_cuisines(lat = lat, long = lng)
		hist = histogram(result[1], [str(lat), str(lng)])

	rest_1_name = result[0][0][0]
	rest_1_addr = result[0][0][1]
	rest_1_rate = result[0][0][6]
	rest_1_lat = result[0][0][3]
	rest_1_lng = result[0][0][4]


	rest_2_name = result[0][1][0]
	rest_2_addr = result[0][1][1]
	rest_2_rate = result[0][1][6]
	rest_2_lat = result[0][1][3]
	rest_2_lng = result[0][1][4]

	rest_3_name = result[0][2][0]
	rest_3_addr = result[0][2][1]
	rest_3_rate = result[0][2][6]
	rest_3_lat = result[0][2][3]
	rest_3_lng = result[0][2][4]

	rest_4_name = result[0][3][0]
	rest_4_addr = result[0][3][1]
	rest_4_rate = result[0][3][6]
	rest_4_lat = result[0][3][3]
	rest_4_lng = result[0][3][4]

	rest_5_name = result[0][4][0]
	rest_5_addr = result[0][4][1]
	rest_5_rate = result[0][4][6]
	rest_5_lat = result[0][4][3]
	rest_5_lng = result[0][4][4]

	food_1 = result[1][0][0]
	food_1 = food_1.upper()
	food_2 = result[1][1][0]
	food_2 = food_2.upper()
	food_3 = result[1][2][0]
	food_3 = food_3.upper()
	food_4 = result[1][3][0]
	food_4 = food_4.upper()
	food_5 = result[1][4][0]
	food_5 = food_5.upper()

	db.commit()
	db.close()



	return render_template('rmd_cuisine.html', zipcode = zipcode, lat = lat, lng = lng, result = result, hist = hist,
							rest_1_name = rest_1_name, rest_1_addr = rest_1_addr, rest_1_rate = rest_1_rate, rest_1_lat = rest_1_lat, rest_1_lng = rest_1_lng,
							rest_2_name = rest_2_name, rest_2_addr = rest_2_addr, rest_2_rate = rest_2_rate, rest_2_lat = rest_2_lat, rest_2_lng = rest_2_lng,
							rest_3_name = rest_3_name, rest_3_addr = rest_3_addr, rest_3_rate = rest_3_rate, rest_3_lat = rest_3_lat, rest_3_lng = rest_3_lng,
							rest_4_name = rest_4_name, rest_4_addr = rest_4_addr, rest_4_rate = rest_4_rate, rest_4_lat = rest_4_lat, rest_4_lng = rest_4_lng,
							rest_5_name = rest_5_name, rest_5_addr = rest_5_addr, rest_5_rate = rest_5_rate, rest_5_lat = rest_5_lat, rest_5_lng = rest_5_lng,
							food_1 = food_1, food_2 = food_2, food_3 = food_3, food_4 = food_4, food_5 = food_5)


@app.route("/rating")
def rating_page():
    return render_template('rating.html')

@app.route("/rating/predict", methods = ['POST'])

def pred_rating():

	zipcode = str(request.form['zipcode'])
	foodtype = str(request.form['foodtype'])
	price = str(request.form['price'])
	delivery = str(request.form['delivery'])
	wifi = str(request.form['wifi'])
	happyhour = str(request.form['happyhour'])
	service = str(request.form['service'])
	state = str(request.form['state'])

	foodtype_2 = foodtype

	if foodtype_2 == 'Coffee & Tea':
		foodtype_2 = 'coffee'
	if foodtype_2 == 'Ice Cream & Frozen Yogurt':
		foodtype_2 = 'ice_cream'
	if foodtype_2 == 'Steakhouses':
		foodtype_2 = 'steak'

	foodtype_3 = foodtype_2.lower().replace(' ', '_')

	zipcode_3 = float(zipcode)
	price_3 = float(price)
	delivery_3 = delivery.upper()
	wifi_3 = wifi.lower()
	happyhour_3 = happyhour.upper()
	service_3 = service.upper()
	state_3 = state

	clf = classification()

	input_ls = [delivery_3, happyhour_3, service_3, wifi_3, price_3, foodtype_3, zipcode_3, state_3]

	features = clf.vecInput(input_ls)

	rating = clf.predict(features)

	clf.stopSC()



	return render_template('pred_rating.html', zipcode = zipcode, foodtype = foodtype, 
							price = price, delivery = delivery, wifi = wifi, happyhour = happyhour,
							service = service, state = state, rating = rating)

@app.route("/contact")
def contact_page():
    return render_template('contact.html')






if __name__ == '__main__':
    app.run(debug=True)