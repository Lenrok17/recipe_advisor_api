from django.db import models

from accounts.models import User
from products.models import Product, Unit

class Fridge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fridge')

class FridgeProduct(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=30, choices=Unit.choices)

