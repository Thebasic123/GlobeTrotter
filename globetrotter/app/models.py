from django.db import models
import json
import re


# Create your models here.
class Country(models.Model):
	name = models.CharField(max_length=100, primary_key=True)


class City(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	country = models.ForeignKey(Country)


class User(models.Model):
	email = models.EmailField(primary_key=True)
	password = models.CharField(max_length=100)

	def getJSON(this):
		jsonD = {
			"email": this.email,
			"password": this.password
		}
		return jsonD #erulo


class Itinerary(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	shareable = models.BooleanField(default=False)


class Attraction(models.Model):
	place_id = models.TextField(primary_key=True)
	#important relations/keys
	city = models.ForeignKey(City)
	itinerary = models.ManyToManyField(Itinerary)

	name = models.TextField()
	address = models.TextField()
	rating = models.DecimalField(max_digits=2, decimal_places=1)
	longitude = models.DecimalField(max_digits=12, decimal_places=6)
	latitude = models.DecimalField(max_digits=12, decimal_places=6)
	picture = models.TextField()


class Restaurant(models.Model):
	restaurant_id = models.TextField(primary_key=True)
	city = models.ForeignKey(City)
	itinerary = models.ManyToManyField(Itinerary)

	name = models.TextField()
	address = models.TextField()
	url = models.TextField(default="https://www.yelp.com")
	longitude = models.DecimalField(default=0, max_digits=12, decimal_places=6)
	latitude = models.DecimalField(default=0, max_digits=12, decimal_places=6)
	image = models.TextField(default="")
	rating = models.DecimalField(max_digits=2, decimal_places=1)
