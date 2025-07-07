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

    def validate(self, data):
        fridge = self.context['request'].user.fridge
        product = data['product']
        if FridgeProduct.objects.filter(fridge=fridge, product=product).exists():
            raise serializers.ValidationError("This product is already in your fridge.")
        return data

class FridgeProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FridgeProduct
        fields = ['product', 'quantity', 'unit']

    def validate(self, data):
        fridge = self.context['request'].user.fridge
        product = data.get('product', None)

        # Pomijamy aktualny obiekt, żeby nie walidować go na duplikat z samym sobą (w przypadku zmiany quantity lub unit)
        if FridgeProduct.objects.filter(fridge=fridge, product=product).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This product is already in your fridge.")
        return data


class FridgeSerializer(serializers.ModelSerializer):
    fridge_products = FridgeProductSerializer(many=True, read_only=True)

    class Meta:
        model = Fridge
        fields = ['id', 'user', 'fridge_products']
        
