import django_filters
from .models import Recipe

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class RecipeFilter(django_filters.FilterSet):
    category = NumberInFilter(field_name='category__id', lookup_expr='in')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ['category', 'category_name', 'title']