from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, InventoryViewSet, RegisterView, OrderViewSet, ProductViewSet, MaintenanceViewSet, predictions

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'products', ProductViewSet)
router.register(r'maintenance', MaintenanceViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('predictions/', predictions, name='predictions'),
    path('', include(router.urls)),
]
