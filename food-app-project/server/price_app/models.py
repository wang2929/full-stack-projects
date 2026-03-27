from django.db import models
from food_app.models import Food

# Create your models here.
class Price(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.food.user}: {self.date} - {self.food.name} - {self.amount}"
