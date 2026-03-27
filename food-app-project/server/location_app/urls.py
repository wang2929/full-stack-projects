from django.urls import path
from .views import OneLocation, AllLocations

urlpatterns = [
    path('', AllLocations.as_view(), name='all_locations'),
    path('name/<str:name>/', OneLocation.as_view(), name='one_location')
]
