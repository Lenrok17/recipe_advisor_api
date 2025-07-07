from rest_framework import permissions

from .models import Recipe, RecipeIngredient

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Recipe):
            return obj.author == request.user
        if isinstance(obj, RecipeIngredient):
            return obj.recipe.author == request.user
        return False