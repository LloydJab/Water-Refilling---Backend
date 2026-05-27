from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, InventoryViewSet, RegisterView, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]
