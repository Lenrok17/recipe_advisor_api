from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from recipes.serializers import RecipeSerializer
from recipes.models import Recipe

from .serializers import FridgeSerializer, FridgeProductSerializer, FridgeProductAddSerializer, FridgeProductUpdateSerializer
from .models import Fridge, FridgeProduct
from .utils import can_make_recipe

class MyFridgeView(generics.RetrieveAPIView):
    serializer_class = FridgeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Fridge.objects.get(user=self.request.user)

    
class FridgeProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FridgeProduct.objects.filter(fridge__user=self.request.user)

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

    def get_queryset(self):
        fridge = Fridge.objects.get(user=self.request.user)
        fridge_products = fridge.fridge_products.all()
        recipes = Recipe.objects.prefetch_related('ingredients__product')

        possible_recipes_id = [r.id for r in recipes if can_make_recipe(r, fridge_products)]

        return Recipe.objects.filter(id__in=possible_recipes_id)