from rest_framework import serializers

from products.serializers import SimpleProductSerializer

from .models import Fridge, FridgeProduct

class FridgeProductSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = FridgeProduct
        fields = ['id', 'product', 'quantity', 'unit']

class FridgeProductAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = ['id', 'product', 'quantity', 'unit']

class FridgeProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = ['product', 'quantity', 'unit']


class FridgeSerializer(serializers.ModelSerializer):
    fridge_products = FridgeProductSerializer(many=True, read_only=True)

    class Meta:
        model = Fridge
        fields = ['id', 'user', 'fridge_products']
