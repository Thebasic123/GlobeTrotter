var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var Country = new Schema({
	name: {type: String, lowercase: true, unique: true},
	cites: [{type: Schema.ObjectId, ref: 'city'}]
});
module.exports.country = Country;

var City = new Schema({
	name: {type: String, lowercase: true, unique: true},
	country: {type: Schema.ObjectId, ref: 'country'},
	attractions: [{type: Schema.ObjectId, ref: 'attraction'}],
	restaurants: [{type: Schema.ObjectId, ref: 'restaurant'}]
});
module.exports.city = City;

var Attraction = new Schema({

});
module.exports.attraction = Attraction;

var Restaurant = new Schema({

});
module.exports.restaurant = Restaurant;

var Itinerary = new Schema({
	user: {type: Schema.ObjectId, ref: 'user'},
	sharable: Boolean,
	attractions: [{type: Schema.ObjectId, ref: 'attraction'}],
	restaurants: [{type: Schema.ObjectId, ref: 'restaurant'}]
});
module.exports.itinerary = Itinerary;

var User = new Schema({
	email: {type: String, lowercase: true, unique: true},
	password: String,
	itinerary: {type: Schema.ObjectId, ref: 'itinerary'}
});
module.exports.user = User;
