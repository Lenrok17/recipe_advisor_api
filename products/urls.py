from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('categories', ProductCategoryViewSet, basename='category')
urlpatterns = router.urls
