var express = require('express');
var router = express.Router();

var yelp = require("yelp").createClient({
  consumer_key: "TlQfDC74QXEeSdRHc1Hv2g", 
  consumer_secret: "spQ6629HBOGaPyIpnol8OcIKkic",
  token: "JXjFuBEY5YJ08wz259MrfEqY1fXX5KBV",
  token_secret: "vKVTfekR_3iH_SNQp8qqiDwmp8c"
});

var useGoogleGeocode = function (query, callback) {
	var request = require('request');
	var requestUrl = "https://maps.googleapis.com/maps/api/geocode/json?address="+encodeURIComponent(query)
					+"&components=country:AUS&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs";
	request(requestUrl, function (error, response, body){
		if (!error && response.statusCode == 200) {
			callback(JSON.parse(body).results);
		} else {
			callback(error);
		}
	});
}

var getAttractions = function (location, callback) {
	var request = require('request');
	var requestUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+encodeURIComponent(location)
	+"&radius=500&types=attraction|tourism&key=AIzaSyAWZ3KcQJeY5f1l8RhMmAUJ_LE77PSM-Bs";
	request(requestUrl, function (error, response, body){
		if (!error && response.statusCode == 200) {
			callback(JSON.parse(body).results);
		} else {
			callback(error);
		}
	});
}

var getRestaurants = function (location, callback) {
	yelp.search({term: "food", location: location}, function(error, data) {
		if (error) throw error;
		callback(data.businesses);
	});
}

var getForecast = function (location, callback) {
	var request = require('request');
	var requestUrl = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22"+
		encodeURIComponent(location)+"%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys";
	request(requestUrl, function (error, response, body){
		if (!error && response.statusCode == 200) {
			callback(JSON.parse(body).query.results.channel);
		} else {
			callback(error);
		}
	});
}

var callback = function(data, cb) {
	var city = data[0];
	var address = city.formatted_address;
	var name = city.address_components[0].long_name;
	var location =  city.geometry.location.lat + ',' + city.geometry.location.lng;
	var events = new (require('events').EventEmitter);
	var topAttractions, topRestaurant, weather;

	var script = 
		"function initialize(){"+
				"var mapOptions = {"+
                "center: new google.maps.LatLng("+location+"),"+
                "zoom: 10,"+
                "mapTypeId: google.maps.MapTypeId.ROADMAP"+
            "};"+
            "var map = new google.maps.Map(document.getElementById('map'), mapOptions);"+
        "}"+
        "google.maps.event.addDomListener(window, 'load', initialize);"

	getAttractions(location, function(attractions){
		topAttractions = attractions.splice(1,8);
		if (topRestaurant != undefined && topAttractions != undefined && weather != undefined)
			events.emit('done');		
	});
	getRestaurants(address, function(data){
		topRestaurant = data.splice(1,8);
		if (topRestaurant != undefined && topAttractions != undefined && weather != undefined)
			events.emit('done');
	});
	getForecast(address, function(data){
		weather = data.item.forecast;
		if (topRestaurant != undefined && topAttractions != undefined && weather != undefined)
			events.emit('done');
	});
	events.on('done', function (){
		cb(script, address, name, topAttractions, topRestaurant, weather);
	});
};

router.post('/', function (req, res){
	var authorised = (req.session.user)? true: false;
	useGoogleGeocode(req.body.query, function (data){
		callback(data, function(script, address, name, topAttractions, topRestaurant, weather){
			res.render('city', {script: script, authorised: authorised, address: address, name: name, attractions: topAttractions, restaurant: topRestaurant, weather: weather});
		});
	});
});

router.get('/city', function (req, res){
	var authorised = (req.session.user)? true: false;
	useGoogleGeocode(req.query.name, function (data){
		callback(data, function(script, address, name, topAttractions, topRestaurant, weather){
			res.render('city', {script: script, authorised: authorised, address: address, name: name, attractions: topAttractions, restaurant: topRestaurant, weather: weather});
		});
	});
});

module.exports = router;