from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeCategoryViewSet, RecipeViewSet, FavourtiteRecipesViewSet, MyRecipesView

router = DefaultRouter()
router.register('categories', RecipeCategoryViewSet, basename='recipe-category')
router.register('favourites', FavourtiteRecipesViewSet, basename='favourite')
router.register('', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('my/', MyRecipesView.as_view(), name='my-recipes'),
    path('', include(router.urls)),
]