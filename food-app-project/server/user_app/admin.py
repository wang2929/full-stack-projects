from django.contrib import admin
from food_app.models import Food
from price_app.models import Price
from stores_app.models import Store
from location_app.models import Location
from user_app.models import AppUser

# Register your models here.
admin.site.register([AppUser, Location, Store, Food, Price])
