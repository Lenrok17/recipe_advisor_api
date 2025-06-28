from django.db import models
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class FavouriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} likes {self.recipe}'