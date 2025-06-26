from django.db import models
from django.conf import settings
from products.models import Product, Unit

class RecipeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prepare_time = models.PositiveSmallIntegerField() # in minutes
    description = models.TextField()
    image_path = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=30, choices=Unit.choices)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.product.name}"
    
