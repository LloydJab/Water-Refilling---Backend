from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet
from .views import InventoryViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]