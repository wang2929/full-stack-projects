from django.db import models
from user_app.models import AppUser
from location_app.models import Location

# Create your models here.
class Store(models.Model):
    # enforce uniqueness by user in the post method
    name:str = models.CharField(null=False, blank=False)
    description:str = models.TextField(max_length=200)
    location = models.ManyToManyField(Location, blank=True, related_name="loc_stores")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - {self.description}"
