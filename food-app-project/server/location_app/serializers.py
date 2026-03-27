from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Location

class LocationSerializer(ModelSerializer):
    stores = SerializerMethodField()
    class Meta:
        model = Location
        fields = ['name', 'description', 'stores']
    def get_stores(self, obj):
        ret = []
        for store in obj.loc_stores.all():
            ret.append(store.name)
        return ret

class AllLocationSerializer(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = Location
        fields = ['name']
    def get_name(self, obj):
        return f"{obj.name} - {obj.description}"