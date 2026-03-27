from user_app.views import UserView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import Price, PriceSerializer
from food_app.models import Food
from rest_framework import status as s

# Create your views here.
class AllPrices(UserView):
    def get(self, request):
        return Response(
            PriceSerializer(
                Price.objects.filter(food__user=request.user),
                many=True).data,
            status=s.HTTP_200_OK)

class OnePrice(UserView):
    def get(self, request, name):
        price = get_object_or_404(
            Price.objects.filter(food__user=request.user), 
            name=name
        )
        return Response(PriceSerializer(price).data, status=s.HTTP_200_OK)
        
    def post(self, request, name):
        if (len(Price.filter(food__user=request.user, name=name)) > 0):
            return Response("Name already exists", status=s.HTTP_400_BAD_REQUEST)
        food = get_object_or_404(Food.objects.filter(user=request.user), name=request.data.get('food'))
        new_price = Price(amount=request.data.get('amount'), food=food)
        new_price.save()
        return Response(f"Added price {new_price}", status=s.HTTP_201_CREATED)
    
    # if you need to update date/time on a price, better to just... make a new one tbh
    def patch(self, request, name):
        price = get_object_or_404(Price.objects.filter(food__user=request.user), name=name)
        data = request.data.copy()
        if 'food' in data:
            data['food'] = get_object_or_404(Food.objects.filter(user=request.user, name=request.data.get('food')))
        updated_price = Price(price, data=data, partial=True)
        if updated_price.is_valid():
            updated_price.save()
            return Response(status=s.HTTP_204_NO_CONTENT)
        else:
            return Response(updated_price.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, name):
        food = get_object_or_404(Food.objects.filter(user=request.user), name=name)
        food.delete()
        return Response(status=s.HTTP_204_NO_CONTENT)