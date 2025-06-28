from django.db.models import Count
from rest_framework import viewsets, mixins

from .serializers import RecipeCategorySerializer, RecipeIngredientSerializer, RecipeSerializer, RecipeDetailsSerializer, RecipeIngredientAddSerializer, RecipeCategoryAddUpdateSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects \
        .select_related('author', 'category') \
        .prefetch_related('ingredients__product')

    def get_queryset(self):
        qs = Recipe.objects.select_related('author', 'category')
        if self.action == 'retrieve':            
            return qs.prefetch_related('ingredients__product')
        return qs.prefetch_related('ingredients')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailsSerializer
        return RecipeSerializer

class RecipeIngredientViewSet(mixins.RetrieveModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    
    queryset = RecipeIngredient.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return RecipeIngredientAddSerializer
        return RecipeIngredientSerializer

class RecipeCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecipeCategory.objects.annotate(recipes_count=Count('recipes')).prefetch_related('recipes')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipeCategoryAddUpdateSerializer
        return RecipeCategorySerializer