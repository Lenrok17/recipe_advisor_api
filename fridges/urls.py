from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MyFridgeView, FridgeProductViewSet, MyFridgeRecipesView

router = DefaultRouter()
router.register('products', FridgeProductViewSet, basename='fridge-product')

urlpatterns = [
    path('my-fridge/', MyFridgeView.as_view(), name='my-fridge'),
    path('my-fridge/', include(router.urls)),
    path('my-fridge/recipes/', MyFridgeRecipesView.as_view(), name='my-fridge-recipes')
]
