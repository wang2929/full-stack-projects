from user_app.views import UserView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import Food, FoodSerializer, AllFoodSerializer
from stores_app.models import Store
from rest_framework import status as s

# Create your views here.
class AllFoods(UserView):
    def get(self, request):
        return Response(
            AllFoodSerializer(
                Food.objects.filter(user=request.user),
                many=True).data,
            status=s.HTTP_200_OK)

class OneFood(UserView):
    def get(self, request, name):
        food = get_object_or_404(
            Food.objects.filter(user=request.user), 
            name=name
        )
        return Response(FoodSerializer(food).data, status=s.HTTP_200_OK)
        
    def post(self, request, name):
        if (len(Food.objects.filter(user=request.user, name__iexact=name)) > 0):
            return Response("Name already exists", status=s.HTTP_400_BAD_REQUEST)
        new_food = Food(name=name, category=request.data.get('category'), description=request.data.get('description'), user=request.user)
        new_food.save()
        for name in request.data.get('store', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            new_food.stores.add(store)
        return Response(f"Added food {new_food}", status=s.HTTP_201_CREATED)
    
    # realistically only patching name, category, description, or store
    # patching name is actually super important
    def patch(self, request, name):
        food = get_object_or_404(Food.objects.filter(user=request.user), name__iexact=name)
        data = request.data.copy()
        # patch to add/remove stores in many-to-many relationship
        for name in data.get('store', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            food.stores.add(store)
        data.pop('store', None)
        for name in request.data.get('remove', []):
            store = get_object_or_404(Store.objects.filter(user=request.user), name__iexact=name)
            food.stores.remove(store)
        data.pop('remove', None)
        updated_food = FoodSerializer(food, data=data, partial=True)
        if updated_food.is_valid():
            updated_food.save()
            return Response(status=s.HTTP_204_NO_CONTENT)
        else:
            return Response(updated_food.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        food = get_object_or_404(Food.objects.filter(user=request.user), name__iexact=name)
        food.delete()
        return Response(status=s.HTTP_204_NO_CONTENT)

class FoodByCategory(UserView):
    def get(self, request, cat):
        return Response(
            AllFoodSerializer(
                Food.objects.filter(user=request.user, category__iexact=cat),
                many=True
            ).data, status=s.HTTP_200_OK)
