from rest_framework.routers import DefaultRouter
from .views import RecipeCategoryViewSet, RecipeViewSet, RecipeIngredientViewSet, FavourtiteRecipesViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('categories', RecipeCategoryViewSet, basename='recipe-category')
router.register('ingredients', RecipeIngredientViewSet, basename='ingredient')
router.register('favourite', FavourtiteRecipesViewSet, basename='favourite')
urlpatterns = router.urls
