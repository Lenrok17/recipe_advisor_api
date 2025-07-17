from django.db import models
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter

from recipes.serializers import RecipeSerializer
from recipes.models import Recipe

from django_filters.rest_framework import DjangoFilterBackend

from recipes.filters import RecipeFilter

from .serializers import FridgeSerializer, FridgeProductSerializer, FridgeProductAddSerializer, FridgeProductUpdateSerializer
from .models import Fridge, FridgeProduct
from .utils import can_make_recipe

class MyFridgeView(generics.RetrieveAPIView):
    serializer_class = FridgeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Fridge.objects.prefetch_related('fridge_products__product').get(user=self.request.user)

    
class FridgeProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        return FridgeProduct.objects.filter(fridge__user=self.request.user).prefetch_related('product')

    def get_serializer_class(self):
        if self.action == 'create':
            return FridgeProductAddSerializer
        elif self.action in ['update', 'partial_update']:
            return FridgeProductUpdateSerializer
        return FridgeProductSerializer
    
    def perform_create(self, serializer):
        fridge = Fridge.objects.get(user=self.request.user)
        serializer.save(fridge=fridge)

class MyFridgeRecipesView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RecipeFilter
    ordering_fields = ['prepare_time', 'title', 'number_of_likes']
    ordering = ['-number_of_likes']

    def get_queryset(self):
        fridge_products = FridgeProduct.objects \
            .select_related('product') \
            .filter(fridge__user=self.request.user)

        recipes = Recipe.objects \
            .select_related('category', 'author') \
            .prefetch_related('ingredients') \
            .annotate(number_of_likes=models.Count('favouriterecipe')) \

        possible_ids = [
            r.id for r in recipes
            if can_make_recipe(r, fridge_products)
        ]

        return recipes.filter(id__in=possible_ids)
