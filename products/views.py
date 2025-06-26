from rest_framework import viewsets
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductAddSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('category')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductAddSerializer
        return ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductCategoryDetailSerializer
        return ProductCategorySerializer