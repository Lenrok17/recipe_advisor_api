from django.db.models import Count

from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductAddUpdateSerializer, ProductCategorySerializer, ProductCategoryDetailSerializer
from .filters import ProductCategoryFilter, ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('category').order_by('name')
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductAddUpdateSerializer
        return ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductCategoryFilter

    def get_queryset(self):
        if self.action != 'retrieve':
            return ProductCategory.objects.annotate(products_count=Count('products')).order_by('name')
        return ProductCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductCategoryDetailSerializer
        return ProductCategorySerializer