from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, InventoryViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, InventoryViewSet, RegisterView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]

