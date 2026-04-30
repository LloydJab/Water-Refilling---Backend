from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer
from .models import Inventory
from .serializers import InventorySerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
