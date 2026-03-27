from django.db import models
from stores_app.models import Store
from user_app.models import AppUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Food(models.Model):
    class Categories(models.TextChoices):
        FRESH = "FRESH", _("Fresh produce and herbs like fruits and vegetables")
        SALTY = "SALTY", _("Salty snacks like chips")
        SWEET = "SWEET", _("Sweet snacks like packaged cookies")
        EGGS = "EGGS", _("Egg products")
        DAIRY = "DAIRY", _("Dairy products like milk, butter, yogurt, etc.")
        MEAT = "MEAT", _("Red meat like beef or veal")
        PORK = "PORK", _("Pig meat products like pork chop, sausage, ham hocks")
        CHICKEN = "CHICKEN", _("Chicken products like whole chicken, breast, etc, not from frozen")
        SEAFOOD = "SEAFOOD", _("Seafood products like fish, crab, etc.")
        BREAD = "BREAD", _("Bread products e.g. tost style, loaf, baguette")
        BAKED_GOODS = "BAKED_GOODS", _("Baked goods like pies, pastries, muffins, cakes")
        DRIED = "DRIED", _("Dried food goods like beans, rice, bulgur")
        CANNED = "CANNED", _("Canned food goods like canned beans, meats, fish")
        SEASONING = "SEASONING", _("Dried seasonings like salt, paprika, kekik")
        FROZEN = "FROZEN", _("Frozen goods like frozen pizza, chicken tenders")
        OTHER = "Other", _("use this category for items that don't fit correctly in one category")
        
        __empty__ = "Unknown" # null
        
    # enforce unique at the post method
    name:str = models.CharField(null=False, blank=False)
    category:str = models.CharField(choices=Categories, default=Categories.OTHER)
    description:str = models.TextField(max_length=200)
    stores = models.ManyToManyField(Store, blank=True, related_name="store_foods")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.user}: {self.name} - {self.category} - {self.description}"
