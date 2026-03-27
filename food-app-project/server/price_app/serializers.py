from rest_framework.serializers import ModelSerializer
from food_app.serializers import FoodSerializer
from .models import Price

class PriceSerializer(ModelSerializer):
    food = FoodSerializer()
    class Meta:
        model = Price
        fields = ['date', 'food', 'amount']