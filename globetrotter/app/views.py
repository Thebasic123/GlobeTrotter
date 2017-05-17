from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader
import requests
import json
from urllib.parse import quote
from requests_oauthlib import OAuth1
from operator import itemgetter
import hashlib
from .models import *
#import simplejson
#from django.utils import simplejson

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'TlQfDC74QXEeSdRHc1Hv2g'
CONSUMER_SECRET = 'spQ6629HBOGaPyIpnol8OcIKkic'
TOKEN = 'JXjFuBEY5YJ08wz259MrfEqY1fXX5KBV'
TOKEN_SECRET = 'vKVTfekR_3iH_SNQp8qqiDwmp8c'

BLANK = 0
SUCCESSFUL_LOGIN = 1
SUCCESSFUL_SIGN_UP = 2
ERROR_AUTH = 3
ERROR_PASSWORD_MISMATCH = 4
ERROR_NO_USER = 5


def farenheightToCelcius(f):
	return round((f - 32)*5/9, 2)


def getWeatherForecast(cName):
	yahooUrl = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22" + quote(cName) + "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	response = requests.get(yahooUrl)
	data = json.loads(response.text)
	forecast = data['query']['results']['channel']['item']['forecast']

	#convert from farenheight to celsius
	for f in forecast:
		f['high'] = farenheightToCelcius(int(f['high']))
		f['low'] = farenheightToCelcius(int(f['low']))

		if("Snow" in f['text']):
			f['picUrl'] = "weather/snowing.svg"
		elif("Thunder" in f['text']):
			f['picUrl'] = "weather/thunderStorm.svg"
		elif("Rain" in f['text']):
			f['picUrl'] = "weather/rainy.svg"
		elif("Showers" in f['text']):
			f['picUrl'] = "weather/rainy.svg"
		elif("Windy" in f['text']):
			f['picUrl'] = "weather/windy.svg"
		elif("Partly Cloudy" in f['text']):
			f['picUrl'] = "weather/partlyCloudy.svg"
		elif("Cloudy" in f['text']):
			f['picUrl'] = "weather/cloudy.svg"
		else:
			f['picUrl'] = "weather/sunny.svg"
	return forecast


def getGeocode(query):
	countryName = "AUS"
	url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + quote(query) +"&components=country:" + countryName + "&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs"
	response = requests.get(url)
	data = json.loads(response.text)
	return data['results'][0]

def recommendAttractions(cityObject, location):
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + quote(location) + "&radius=100&types=attraction&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs"
	response = requests.get(url)
	data = json.loads(response.text)
	allAttractions = []
	for r in data['results']:
		if(r['types'].count('locality') == 0):
			name = r['name']
			#rating = r['rating']
			place_id = r['place_id']
			detailURL = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + r['place_id'] + "&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs"
			response2 = requests.get(detailURL)
			detailData = json.loads(response2.text)
			address = detailData['result']['formatted_address']
			#latitude/longitude
			latitude = detailData['result']['geometry']['location']['lat']
			longitude = detailData['result']['geometry']['location']['lng']
			pic = detailData['result']['icon']
			try:
				rating = detailData['result']['rating']
			except KeyError:
				rating = 0

			thisAttraction = {
				"pk": place_id,
				"name": name,
				"address": address,
				"rating": rating,
				"longitude": longitude,
				"latitude": latitude,
				"picture": pic,
				"city": cityObject.name
			}
			allAttractions.append(thisAttraction)
			if len(allAttractions) == 3:
				break
	#only add top 3
	top3 = allAttractions

	return top3

def getAttractions(cityObject, location):
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + quote(location) + "&radius=2000&types=attraction&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs"
	response = requests.get(url)
	data = json.loads(response.text)
	allAttractions = []
	for r in data['results']:
		if(r['types'].count('locality') == 0):
			name = r['name']
			#rating = r['rating']
			place_id = r['place_id']
			detailURL = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + r['place_id'] + "&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs"
			response2 = requests.get(detailURL)
			detailData = json.loads(response2.text)
			address = detailData['result']['formatted_address']
			#latitude/longitude
			latitude = detailData['result']['geometry']['location']['lat']
			longitude = detailData['result']['geometry']['location']['lng']
			if "photos" in detailData['result']:
				getImageUrl = "https://maps.googleapis.com/maps/api/place/photo?key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs&maxwidth=250&photoreference="+detailData['result']['photos'][0]['photo_reference']
				pic = getImageUrl
			else :
				pic = detailData['result']['icon']
			try:
				rating = detailData['result']['rating']
			except KeyError:
				rating = 0

			thisAttraction = {
				"pk": place_id,
				"name": name,
				"address": address,
				"rating": rating,
				"longitude": longitude,
				"latitude": latitude,
				"picture": pic
			}
			allAttractions.append(thisAttraction)
	#only add top 8
	allAttractions = sorted(allAttractions, key=itemgetter('rating'))
	allAttractions.reverse()
	top8 = allAttractions[:8]

	for a in top8:
		addThis = Attraction(place_id=a['pk'], city=cityObject, address=a['address'], name=a['name'], rating=a['rating'], longitude=a['longitude'], latitude=a['latitude'], picture=a['picture'])
		addThis.save()
	return top8

def recommendRestaurants(cityObject, location):
	#load restaurants
	urlYelp = "http://api.yelp.com/v2/search?term=food&location=" + quote(cityObject.name) + "&cll=" + quote(location) + "&limit=3&sort=2"
	allRestaurants = []
	auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
	response = requests.get(urlYelp, auth=auth)
	data2 = json.loads(response.text)
	for r in data2['businesses']:
		name = r['name']
		rId = r['id']
		rating = r['rating']
		address = ' '.join(r['location']['address'])
		latitude = r['location']['coordinate']['latitude']
		longitude = r['location']['coordinate']['longitude']
		image = r['image_url']
		thisRestaurant = {
			"name": name,
			"city": cityObject.name,
			"address": address,
			"rating": rating,
			"latitude": latitude,
			"longitude": longitude,
			"rId": rId,
			"url": r['url'],
			"image": image
		}
		allRestaurants.append(thisRestaurant)
	return allRestaurants

def getRestaurants(cityObject, cityString):
	#load restaurants
	urlYelp = "http://api.yelp.com/v2/search?term=food&location=" + quote(cityString) + "&limit=8&sort=2"
	allRestaurants = []
	auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)
	response = requests.get(urlYelp, auth=auth)
	data2 = json.loads(response.text)
	for r in data2['businesses']:
		name = r['name']
		rId = r['id']
		rating = r['rating']
		address = ' '.join(r['location']['address'])
		longitude = r['location']['coordinate']['longitude']
		latitude = r['location']['coordinate']['latitude']
		try:
			image = r['image_url']
		except KeyError:
			image = "blank"
		thisRestaurant = {
			"name": name,
			"address": address,
			"rating": rating,
			"rId": rId,
			"url": r['url'],
			"image": image
		}
		allRestaurants.append(thisRestaurant)
		newRestaurant = Restaurant(restaurant_id=rId, city=cityObject, name=name, url=r['url'], rating=rating, address=address, longitude=longitude, latitude=latitude, image=image)
		newRestaurant.save()
	return allRestaurants


def getLoggedInUser(request):
	if 'user' in request.session:
		userLoggedIn = True
		user = request.session['user']
	else:
		userLoggedIn = False
		user = "Null"
	retUser = {
		'isLoggedIn': userLoggedIn,
		'email': user
	}
	return retUser


# Create your views here.
def home(request):
	user = getLoggedInUser(request)
	template = loader.get_template('index.html')
	modalActivate = "#"
	if('logInInitiated' in request.POST):
		try:
			m = User.objects.get(email=request.POST['email'])
			if (m.password == request.POST['pass']):
				request.session['user'] = m.email
				user = getLoggedInUser(request)
			else:
				modalActivate = "#loginFail"
		except User.DoesNotExist:
			modalActivate = "#loginFail"
	elif('signupInitiated' in request.POST):
		newEmail = request.POST['email']
		password = request.POST['pass']
		if(not User.objects.filter(email=newEmail).exists()):
			newUser = User(email=newEmail, password=password)
			newUser.save()
			newItinerary = Itinerary(user=newUser)
			newItinerary.save()
			request.session['user'] = newEmail
			user = getLoggedInUser(request)
			modalActivate = '#signupSuccess'
		else:
			modalActivate = '#signupFail'
	context = RequestContext(request, {
		'isLoggedIn': user['isLoggedIn'],
		'userEmail': user['email'],
		'activateThis': modalActivate
	})
	return HttpResponse(template.render(context))


def country(request):
	user = getLoggedInUser(request)
	try:
		country = Country.objects.get(name=request.GET['query'])
		n = country.name
		cityObjects = country.city_set.all()
		cityDicts = []
		for co in cityObjects:
			cName = co.name
			attractions = co.attraction_set.all().order_by('-rating')
			totalRating = 0
			for a in attractions:
				totalRating += float(a.rating)
			topOne = attractions.first()
			attractionPic = topOne.picture
			addThis = {
				'name': cName,
				'picture': attractionPic,
				'totalRating': totalRating
			}
			cityDicts.append(addThis)
			newlist = sorted(cityDicts, key=itemgetter('totalRating'), reverse=True)
	except Country.DoesNotExist:
		n = name
		cityDicts = []
		newCountry = Country(name=n, country_code="AUS")
		newCountry.save()
	template = loader.get_template('countryTemplate.html')
	context = RequestContext(request, {
		'name': n,
		'cities': newlist,
		'isLoggedIn': user['isLoggedIn'],
		'userEmail': user['email']
	})
	return HttpResponse(template.render(context))

def city(request):
	if(request.GET['query'] == "Australia"):
		return redirect('/country?query=Australia')
	else:
		user = getLoggedInUser(request)
		template = loader.get_template('cityTemplate.html')
		HttpResponse(template.render())

		if(user['isLoggedIn']):
			thisUser = User.objects.get(email=user['email'])
			usersItinerary = thisUser.itinerary
			if('attractionId' in request.POST):
				attractionId = request.POST['attractionId']
				addThis = Attraction.objects.get(place_id=attractionId)
				addThis.itinerary.add(usersItinerary)
			elif('restaurantId' in request.POST):
				restaurantId = request.POST['restaurantId']
				addThis = Restaurant.objects.get(restaurant_id=restaurantId)
				addThis.itinerary.add(usersItinerary)
			usersItinerary.save()
			thisUser.save()

		data = getGeocode(request.GET['query'])
		cName = str(data['address_components'][0]['long_name'])
		location = str(data['geometry']['location']['lat']) + "," + str(data['geometry']['location']['lng'])
		try:
			city = City.objects.get(name=cName)
			n = city.name
			country = city.country.name
			attractions = city.attraction_set.all()[:8]
			restaurants = city.restaurant_set.all()[:8]
			forecast = getWeatherForecast(cName)
		except City.DoesNotExist:
			n = cName
			country = str(data['address_components'][2]['long_name'])
			forecast = getWeatherForecast(cName)

			#check that its country exists
			try:
				countryObject = Country.objects.get(name=country)
			except Country.DoesNotExist:
				countryObject = Country(name=country)
			finally:
				countryObject.save()
			city = City(name=n, country=countryObject)
			attractions = getAttractions(city, location)
			city.save()
			restaurants = getRestaurants(city, cName)
			city.save()

		template = loader.get_template('cityTemplate.html')
		context = RequestContext(request, {
			'name': n,
			'country': country,
			'attractions': attractions,
			'restaurants': restaurants,
			'forecast': forecast,
			'isLoggedIn': user['isLoggedIn'],
			'userEmail': user['email']
		})
		return HttpResponse(template.render(context))


def itinerary(request):
	user = getLoggedInUser(request)
	template = loader.get_template('itineraryTemplate.html')
	activateThis = "#"

	if(user['isLoggedIn']):
		thisUser = User.objects.get(email=user['email'])
		usersItinerary = thisUser.itinerary

		if('toggleSharing' in request.POST):
			usersItinerary.shareable = not usersItinerary.shareable
		if('addAttraction' in request.POST):
			attractionId = request.POST['attractionId']
			try:
				addThis = Attraction.objects.get(place_id=attractionId)
			except Attraction.DoesNotExist:
				city = City.objects.get(name=request.POST['attractionCity'])
				addThis = Attraction(place_id=request.POST['attractionId'],
				city=city,
				address=request.POST['attractionAddress'],
				name=request.POST['attractionName'],
				rating=request.POST['attractionRating'],
				longitude=request.POST['attractionLongitude'],
				latitude=request.POST['attractionLatitude'],
				picture=request.POST['attractionPic'])
			addThis.itinerary.add(usersItinerary)
			addThis.save()
		elif('addRestaurant' in request.POST):
			restaurantId = request.POST['restaurantId']
			try:
				addThis = Restaurant.objects.get(restaurant_id=restaurantId)
			except Restaurant.DoesNotExist:
				city = City.objects.get(name=request.POST['restaurantCity'])
				addThis = Restaurant(place_id=request.POST['restaurantId'],
				city=city,
				address=request.POST['restaurantAddress'],
				name=request.POST['restaurantName'],
				url=request.POST['restaurantUrl'],
				rating=request.POST['restaurantRating'],
				longitude=request.POST['restaurantLongitude'],
				latitude=request.POST['restaurantLatitude'],
				image=request.POST['restaurantPic'])
			addThis.itinerary.add(usersItinerary)
			addThis.save()
		elif('removeRestaurant' in request.POST):
			restaurantId = request.POST['restaurantId']
			removeThis = Restaurant.objects.get(restaurant_id=restaurantId)
			removeThis.itinerary.remove(usersItinerary)
			removeThis.save()
		elif('removeAttraction' in request.POST):
			attractionId = request.POST['attractionId']
			removeThis = Attraction.objects.get(place_id=attractionId)
			removeThis.itinerary.remove(usersItinerary)
			removeThis.save()
		elif('shareToggle' in request.POST):
			usersItinerary.shareable = not usersItinerary.shareable
			if (usersItinerary.shareable == True):
				activateThis = "#sharingModal"
		usersItinerary.save()
		thisUser.save()

		attractions = Attraction.objects.filter(itinerary=usersItinerary)
		restaurants = Restaurant.objects.filter(itinerary=usersItinerary)

		#load recommendations
		allRecomendations = []
		for a in attractions:
			location = str(a.latitude) + "," + str(a.longitude)
			for rec in recommendAttractions(a.city, location):
				allRecomendations.append(rec)

		for r in allRecomendations:
			if Attraction.objects.filter(name=r['name']).count() > 0:
				allRecomendations.remove(r)
		allRecomendations = sorted(allRecomendations, key=itemgetter('rating'))
		allRecomendations.reverse()
		final3 = allRecomendations[:3]

		allRecomendations = []
		for r in restaurants:
			location = str(r.latitude) + "," + str(r.longitude)
			for rec in recommendRestaurants(r.city, location):
				allRecomendations.append(rec)

		for r in allRecomendations:
			if Attraction.objects.filter(name=r['name']).count() > 0:
				allRecomendations.remove(r)

		context = RequestContext(request, {
			'attractions': attractions,
			'restaurants': restaurants,
			'recommendedAttractions': final3,
			'recommendedRestaurants': allRecomendations,
			'shareable': usersItinerary.shareable,
			'isLoggedIn': user['isLoggedIn'],
			'userEmail': user['email'],
			'activateThis': activateThis
		})
		return HttpResponse(template.render(context))
	else:
		username = request.GET['user']
		thisUser = User.objects.get(email=username)
		usersItinerary = thisUser.itinerary
		if(usersItinerary.shareable == True):
			attractions = Attraction.objects.filter(itinerary=usersItinerary)
			restaurants = Restaurant.objects.filter(itinerary=usersItinerary)
			context = RequestContext(request, {
				'attractions': attractions,
				'restaurants': restaurants,
				'recommendedAttractions': {},
				'recommendedRestaurants': {},
				'isLoggedIn': user['isLoggedIn'],
				'shareable': True,
				'userEmail': username,
				'activateThis': activateThis
			})
		else:
			context = RequestContext(request, {
				'attractions': {},
				'restaurants': {},
				'recommendedAttractions': {},
				'recommendedRestaurants': {},
				'shareable': False,
				'isLoggedIn': user['isLoggedIn'],
				'userEmail': username,
				'activateThis': activateThis
			})
		return HttpResponse(template.render(context))


def get_cities(request):
	if request.is_ajax():
		q = request.GET.get('term', '')
		cities = City.objects.filter(name__icontains = q)[:20]
		results = []
		for city in cities:
			city_json = {}
			city_json['id'] = city.name
			city_json['label'] = city.name
			city_json['value'] = city.name
			results.append(city_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data,mimetype)


def logout(request):
	#clears session and cookie
	request.session.flush()
	template = loader.get_template('index.html')
	context = RequestContext(request, {
		'isLoggedIn': False,
		'userEmail': "",
		'activateThis': 0
	})
	return HttpResponse(template.render(context))


#use MD5 hash password
def hashPassword(password):
	m=hashlib.md5()
	password=password.encode('utf-8')
	m.update(password)
	return m.hexdigest()


def register(request):
	email = request.POST['email']
	password = request.POST['pass']
	passconfirm = request.POST['passconfirm']
	if(len(password) < 6):  #if user password is too short
		print ('Your password is too short,it should be longer than 6 characters.')
	else:
		if(password == passconfirm):
			hashedPassword=hashPassword(password)
			newUser = User(email=email, password=password)
			newUser.save()
			newItinerary = Itinerary(user=newUser)
			newItinerary.save()
			request.session['user']=email
			template = loader.get_template('SUCCESSFUL_SIGN_UP.html')
		else:
			template = loader.get_template('ERROR_PASSWORD_MISMATCH.html')
	return HttpResponse(template.render())
