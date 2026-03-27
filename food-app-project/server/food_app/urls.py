from django.urls import path
from .views import AllFoods, OneFood, FoodByCategory

urlpatterns = [
    path('', AllFoods.as_view(), name='all_foods'),
    path('name/<str:name>/', OneFood.as_view(), name='one_food'),
    path('category/<str:cat>/', FoodByCategory.as_view(), name='food_by_cat')
]