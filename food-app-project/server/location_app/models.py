from django.db import models
from user_app.models import AppUser

# Create your models here.
class Location(models.Model):
    # will have to enforce uniqueness at the user level
    name:str = models.CharField(null=False, blank=False, unique=False)
    description:str = models.TextField(max_length=500)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.email}: {self.name} - {self.description}"

# Create your models here.
class Location(models.Model):
    name:str = models.CharField(null=False, blank=False, unique=True)
    detail:str = models.TextField()
    
    def __str__(self):
        return f""
