from django.db import transaction
from rest_framework import serializers

from products.serializers import SimpleProductSerializer
from .models import Recipe, RecipeCategory, RecipeIngredient, FavouriteRecipe

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

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'product', 'quantity', 'unit']

class RecipeIngredientDetailsSerializer(RecipeIngredientSerializer):
    product = SimpleProductSerializer()

###############################################
############ RECIPE SERIALIZERS ###############
###############################################

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    category = SimpleRecipeCategorySerializer(read_only=True)
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'author', 'number_of_likes', 'prepare_time', 'image']

    def get_number_of_likes(self, obj):
        # Jeśli to endpoint z annotate
        if hasattr(obj, 'number_of_likes'):
            return obj.number_of_likes
        # Brak annotate — pojedyncze zliczanie
        return obj.favouriterecipe_set.count()


class RecipeDetailsSerializer(RecipeSerializer):
    ingredients = RecipeIngredientDetailsSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['ingredients', 'description']

class RecipeAddUpdateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, write_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'prepare_time', 'ingredients', 'description', 'image']

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("You have to add at least one product.")
        product_ids = [v['product'].id for v in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("You cannot add the same product twice.")
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data, author=self.context['request'].user)
        self._create_ingredients(recipe, ingredients)
        return recipe

    def _create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient)

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if ingredients is not None:
            instance.ingredients.all().delete()
            self._create_ingredients(instance, ingredients)

        return instance

###############################################
####### FAVOURITE RECIPE SERIALIZERS ##########
###############################################

class FavouriteRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = FavouriteRecipe
        fields = ['id', 'recipe']

class FavouriteRecipeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteRecipe
        fields = ['id', 'recipe']

    def validate(self, data):
        user = self.context['request'].user
        recipe = data.get('recipe')
        if FavouriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("This recipe is already in your favourites.")
        return data