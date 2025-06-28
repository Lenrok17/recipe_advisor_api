from rest_framework import serializers

from products.serializers import SimpleProductSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient

###############################################
##### RECIPE CATEGORY SERIALIZERS #############
###############################################

class RecipeCategorySerializer(serializers.ModelSerializer):
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecipeCategory
        fields = ['id', 'name', 'recipes_count', 'recipes']

class RecipeCategoryAddUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ['id', 'name']

###############################################
##### RECIPE INGREDIENTS SERIALIZERS ##########
###############################################

class RecipeIngredientAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'product', 'quantity', 'unit']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'product', 'quantity', 'unit']

class SimpleRecipeIngredientSerializer(RecipeIngredientSerializer):
    product = serializers.CharField(source='product.name')

###############################################
############ RECIPE SERIALIZERS ###############
###############################################

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username')
    category = RecipeCategorySerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'author', 'prepare_time', 'ingredients', 'description', 'image']

class RecipeDetailsSerializer(RecipeSerializer):
    ingredients = SimpleRecipeIngredientSerializer(many=True, read_only=True)
