from rest_framework import serializers

from products.serializers import SimpleProductSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient

from products.serializers import SimpleProductSerializer

###############################################
##### RECIPE CATEGORY SERIALIZERS #############
###############################################

class RecipeCategorySerializer(serializers.ModelSerializer):
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecipeCategory
        fields = ['id', 'name', 'recipes_count', 'recipes']

class SimpleRecipeCategorySerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        recipe = self.instance.recipe
        product = data['product']
        if RecipeIngredient.objects.filter(recipe=recipe, product=product).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This product is already in this recipe.")
        return data

class RecipeIngredientDetailsSerializer(RecipeIngredientSerializer):
    product = SimpleProductSerializer()

###############################################
############ RECIPE SERIALIZERS ###############
###############################################

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    category = SimpleRecipeCategorySerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'author', 'prepare_time', 'ingredients', 'description', 'image']

class RecipeDetailsSerializer(RecipeSerializer):
    ingredients = RecipeIngredientDetailsSerializer(many=True, read_only=True)

class RecipeAddUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'prepare_time', 'description', 'image']