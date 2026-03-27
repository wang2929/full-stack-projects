from django.urls import path
from .views import AllPrices, OnePrice

urlpatterns = [
    path('', AllPrices.as_view(), name='all_foods'),
    path('name/', OnePrice.as_view(), name='one_food')
]