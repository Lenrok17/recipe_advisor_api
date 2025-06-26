from django.db import models
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe

class User(AbstractUser):
    pass

class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')
