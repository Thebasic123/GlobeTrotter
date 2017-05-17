from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'country$', views.country, name='country'),
    url(r'city$', views.city, name='city'),
    url(r'itinerary$', views.itinerary, name='itinerary'),
    url(r'^api/get_cities/', views.get_cities, name='get_cities'),
    url(r'user/logout$', views.logout, name='logout')
]
