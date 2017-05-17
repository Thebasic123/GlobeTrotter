var mongoose = require('mongoose');
var model = require('./models');

mongoose.model('country', model.country);
mongoose.model('city', model.city);
mongoose.model('attraction', model.attraction);
mongoose.model('restaurant', model.restaurant);
mongoose.model('itinerary', model.itinerary);
mongoose.model('user', model.user);

mongoose.connect('mongodb://localhost/globetrotter');