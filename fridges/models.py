from django.db import models
from django.conf import settings
from products.models import Product, Unit

class Fridge(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fridge')

    def __str__(self):
        return f'{self.user}\'s fridge'

class FridgeProduct(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=30, choices=Unit.choices)

    def __str__(self):
        return f'{self.quantity} {self.unit} {self.product} in {self.fridge}'

