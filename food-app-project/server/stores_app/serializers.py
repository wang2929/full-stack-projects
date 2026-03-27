from rest_framework.serializers import ModelSerializer, SerializerMethodField
from stores_app.models import Store
from location_app.serializers import LocationSerializer
from food_app.serializers import FoodSerializer

class StoreSerializer(ModelSerializer):
    location = SerializerMethodField()
    store_foods = FoodSerializer(many=True)
    class Meta:
        model = Store
        fields = ['name', 'description', 'location', 'store_foods']
    def get_location(self, obj):
        ret = []
        for loc in obj.location.all():
            ret.append(loc.name)
        return ret

class StoreAllSerializer(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = Store
        fields = ['name']
    def get_name(self, obj):
        return f"{obj.name.title()} - {obj.description}"