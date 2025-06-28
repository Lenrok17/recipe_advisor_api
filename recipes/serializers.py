from rest_framework import serializers

from products.serializers import SimpleProductSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient

class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id', 'name', 'recipes']

class RecipeIngredientAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'product', 'quantity', 'unit']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'product', 'quantity', 'unit']

class SimpleRecipeIngredientSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'product', 'quantity', 'unit']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username')
    category = RecipeCategorySerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'author', 'prepare_time', 'ingredients', 'description', 'image']

class RecipeDetailsSerializer(serializers.ModelSerializer):
    ingredients = SimpleRecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'author', 'prepare_time', 'ingredients', 'description', 'image']