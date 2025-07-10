from rest_framework.routers import DefaultRouter
from .views import RecipeCategoryViewSet, RecipeViewSet, RecipeIngredientViewSet, FavourtiteRecipesViewSet

router = DefaultRouter()
router.register('categories', RecipeCategoryViewSet, basename='recipe-category')
router.register('ingredients', RecipeIngredientViewSet, basename='ingredient')
router.register('favourites', FavourtiteRecipesViewSet, basename='favourite')
router.register('', RecipeViewSet, basename='recipe')
urlpatterns = router.urls
