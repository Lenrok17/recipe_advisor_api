from django.db.models import Count

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RecipeCategorySerializer, RecipeIngredientSerializer, RecipeSerializer, RecipeAddUpdateSerializer, RecipeDetailsSerializer, RecipeIngredientAddSerializer, SimpleRecipeCategorySerializer
from .models import Recipe, RecipeCategory, RecipeIngredient
from .filters import RecipeFilter

class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

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