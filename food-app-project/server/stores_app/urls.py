from django.urls import path
from .views import AllStores, OneStore

urlpatterns = [
    path('', AllStores.as_view(), name='all_locations'),
    path('name/<str:name>/', OneStore.as_view(), name='one_location')
]