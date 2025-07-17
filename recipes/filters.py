import django_filters
from .models import Recipe, FavouriteRecipe

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='exact')
    category = NumberInFilter(field_name='category__id', lookup_expr='in')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    prepare_time_min = django_filters.NumberFilter(field_name='prepare_time', lookup_expr='gte')
    prepare_time_max = django_filters.NumberFilter(field_name='prepare_time', lookup_expr='lte')

    class Meta:
        model = Recipe
        fields = ['category', 'category_name', 'title', 'prepare_time_min', 'prepare_time_max']

class FavouriteRecipeFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name='recipe__category__id', lookup_expr='in')
    category_name = django_filters.CharFilter(field_name='recipe__category__name', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='recipe__title', lookup_expr='icontains')
    prepare_time_min = django_filters.NumberFilter(field_name='recipe__prepare_time', lookup_expr='gte')
    prepare_time_max = django_filters.NumberFilter(field_name='recipe__prepare_time', lookup_expr='lte')

    class Meta:
        model = FavouriteRecipe
        fields = ['category', 'category_name', 'title', 'prepare_time_min', 'prepare_time_max']