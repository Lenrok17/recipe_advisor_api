from django.db import models
from django.conf import settings
from products.models import Product, Unit

from accounts.models import User

class RecipeCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(RecipeCategory, on_delete=models.PROTECT, blank=True, null=True, related_name='recipes')
    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prepare_time = models.PositiveSmallIntegerField() # in minutes
    description = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=30, choices=Unit.choices)

    class Meta:
        unique_together = ('recipe', 'product')

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.product.name}"
    
class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} likes {self.recipe}'