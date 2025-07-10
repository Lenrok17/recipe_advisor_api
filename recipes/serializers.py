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

class RecipeIngredientAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'recipe', 'product', 'quantity', 'unit']

    def validate(self, data):
        recipe = data['recipe']
        product = data['product']

        if recipe.author != self.context['request'].user:
            raise serializers.ValidationError("You are not the author of this recipe.")

        if RecipeIngredient.objects.filter(recipe=recipe, product=product).exists():
            raise serializers.ValidationError("This product is already in this recipe.")

        return data

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
    class Meta:
        model = Recipe
        fields = ['id', 'category', 'title', 'prepare_time', 'description', 'image']

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