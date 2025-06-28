from rest_framework.routers import DefaultRouter
from .views import RecipeCategoryViewSet, RecipeViewSet, RecipeIngredientViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('categories', RecipeCategoryViewSet, basename='recipe-category')
router.register('ingredients', RecipeIngredientViewSet, basename='ingredient')
urlpatterns = router.urls
