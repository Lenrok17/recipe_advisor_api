from rest_framework import serializers

from .models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'name']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']

class ProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name']

class ProductCategoryDetailSerializer(serializers.ModelSerializer):
    products = SimpleProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'products']