from user_app.views import UserView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import Store, StoreSerializer, StoreAllSerializer
from location_app.models import Location
from rest_framework import status as s

# Create your views here.
class AllStores(UserView):
    def get(self, request):
        return Response(
            StoreAllSerializer(
                Store.objects.filter(user=request.user),
                many=True).data,
            status=s.HTTP_200_OK)

class OneStore(UserView):
    def get(self, request, name):
        store = get_object_or_404(
            Store.objects.filter(user=request.user), 
            name=name
        )
        return Response(StoreSerializer(store).data, status=s.HTTP_200_OK)
        
    def post(self, request, name):
        if (len(Store.objects.filter(user=request.user, name__iexact=name)) > 0):
            return Response("Name already exists", status=s.HTTP_400_BAD_REQUEST)
        new_store = Store(name=name, user=request.user, description=request.data["description"])
        new_store.save()
        for name in request.data.get('location', []):
            location = get_object_or_404(Location.objects.filter(user=request.user), name__iexact=name)
            new_store.location.add(location)
        return Response(f"Added store {new_store}", status=s.HTTP_201_CREATED)
    
    def patch(self, request, name):
        store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
        data = request.data.copy()
        # patch to add/remove locations in many-to-many relationship
        for name in request.data.get('location', []):
            location = get_object_or_404(Location.objects.filter(user=request.user), name__iexact=name)
            store.location.add(location)
        data.pop('location', None)
        for name in request.data.get('remove', []):
            location = get_object_or_404(Location.objects.filter(user=request.user), name__iexact=name)
            store.location.remove(location)
        data.pop('remove', None)
        updated_store = StoreSerializer(store, data=data, partial=True)
        if updated_store.is_valid():
            updated_store.save()
            return Response(status=s.HTTP_204_NO_CONTENT)
        else:
            return Response(updated_store.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
        store.delete()
        return Response(status=s.HTTP_204_NO_CONTENT)
