from rest_framework import viewsets, generics
from rest_framework.exceptions import NotAuthenticated

from .serializers import FridgeSerializer, FridgeProductSerializer, FridgeProductAddSerializer, FridgeProductUpdateSerializer
from .models import Fridge, FridgeProduct
from .permissions import IsFridgeProductOwner

class MyFridgeView(generics.RetrieveAPIView):
    serializer_class = FridgeSerializer
    
    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You need to be logged in")
        return Fridge.objects.get(user=self.request.user)

    
class FridgeProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsFridgeProductOwner]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You need to be logged in")
        return FridgeProduct.objects.filter(fridge__user=user)

    def get_serializer_class(self):
        if self.action in 'create':
            return FridgeProductAddSerializer
        elif self.action in ['update', 'partial_update']:
            return FridgeProductUpdateSerializer
        return FridgeProductSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("You need to be logged in")
        fridge = Fridge.objects.get(user=self.request.user)
        serializer.save(fridge=fridge)