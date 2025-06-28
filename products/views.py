from django.db.models import Count
from rest_framework import viewsets
from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductAddUpdateSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('category')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductAddUpdateSerializer
        return ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action != 'retrieve':
            return ProductCategory.objects.annotate(products_count=Count('products'))
        return ProductCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductCategoryDetailSerializer
        return ProductCategorySerializer