from rest_framework.serializers import ModelSerializer, SerializerMethodField
from food_app.models import Food

class FoodSerializer(ModelSerializer):
    stores = SerializerMethodField()
    class Meta:
        model = Food
        fields = ['name', 'category', 'stores', 'description']
    def get_stores(self, obj):
        ret = []
        for store in obj.stores.all():
            ret.append(store.name)
        return ret

class AllFoodSerializer(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = Food
        fields = ['name']
    def get_name(self, obj):
        return f"{obj.name.title()} - {obj.category.title()} Product - {obj.description}"