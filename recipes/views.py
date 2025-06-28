from rest_framework import viewsets, mixins

from .serializers import RecipeCategorySerializer, RecipeIngredientSerializer, RecipeSerializer, RecipeDetailsSerializer, RecipeIngredientAddSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient


class RecipeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == 'retrieve':
            return Recipe.objects.prefetch_related('ingredients__product')
        return Recipe.objects.prefetch_related('ingredients')

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
        if self.action == 'create':
            return RecipeIngredientAddSerializer
        return RecipeIngredientSerializer

class RecipeCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer