from user_app.views import UserView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from stores_app.models import Store
from .serializers import Location, LocationSerializer, AllLocationSerializer
from rest_framework import status as s

# Create your views here.
class AllLocations(UserView):
    def get(self, request):
        return Response(
            AllLocationSerializer(
                Location.objects.filter(user=request.user), 
                many=True).data,
            status=s.HTTP_200_OK)

class OneLocation(UserView):
    def get(self, request, name):
        location = get_object_or_404(
            Location.objects.filter(user=request.user), 
            name=name)
        return Response(LocationSerializer(location).data, status=s.HTTP_200_OK)
    
    def post(self, request, name):
        if (len(Location.objects.filter(user=request.user, name=name)) > 0):
            return Response("Name already exists", status=s.HTTP_400_BAD_REQUEST)
        new_loc = Location(name=name, description=request.data["description"], user=request.user)
        new_loc.save()
        # optionally add stores list
        for name in request.data.get('store', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            new_loc.loc_stores.add(store)
        return Response(f"Added location {new_loc}", status=s.HTTP_201_CREATED)
    
    def patch(self, request, name):
        loc = get_object_or_404(Location.objects.filter(user=request.user), name__iexact=name)
        data = request.data.copy()
        # patch to add/remove stores in many-to-many relationship
        for name in data.get('store', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            loc.loc_stores.add(store)
        data.pop('store', None)
        for name in request.data.get('remove', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            loc.loc_stores.remove(store)
        data.pop('remove', None)
        updated_loc = LocationSerializer(loc, data=data, partial=True)
        if updated_loc.is_valid():
            updated_loc.save()
            return Response(status=s.HTTP_204_NO_CONTENT)
        else:
            return Response(updated_loc.errors, status=s.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, name):
        loc = get_object_or_404(Location.objects.filter(user=request.user), name__iexact=name)
        loc.delete()
        return Response(status=s.HTTP_204_NO_CONTENT)
