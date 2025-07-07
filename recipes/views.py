from django.db.models import Count

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    RecipeCategorySerializer, RecipeIngredientSerializer, RecipeSerializer, 
    RecipeAddUpdateSerializer, RecipeDetailsSerializer, RecipeIngredientAddSerializer, SimpleRecipeCategorySerializer,
    FavouriteRecipeSerializer, FavouriteRecipeAddSerializer
)

from .models import Recipe, RecipeCategory, RecipeIngredient, FavouriteRecipe
from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly

class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        qs = Recipe.objects.select_related('author', 'category')
        if self.action == 'retrieve':            
            return qs.prefetch_related('ingredients__product')
        elif self.action == 'create':
            return qs
        return qs.prefetch_related('ingredients')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailsSerializer
        elif self.action in ['create', 'update']:
            return RecipeAddUpdateSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class RecipeIngredientViewSet(mixins.RetrieveModelMixin,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    
    queryset = RecipeIngredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return RecipeIngredientAddSerializer
        return RecipeIngredientSerializer

class RecipeCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecipeCategory.objects.annotate(recipes_count=Count('recipes')).prefetch_related('recipes').order_by('name')

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return SimpleRecipeCategorySerializer
        return RecipeCategorySerializer
    
class FavourtiteRecipesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return FavouriteRecipeAddSerializer
        return FavouriteRecipeSerializer
    
    def get_queryset(self):
        return FavouriteRecipe.objects \
            .filter(user=self.request.user) \
            .select_related('recipe__category', 'recipe__author') \
            .prefetch_related('recipe__ingredients')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    