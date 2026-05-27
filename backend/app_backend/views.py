from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView, settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Inventory, Maintenance, Order, Product
from .serializers import AccountSerializer, InventorySerializer, MaintenanceSerializer, OrderSerializer, ProductSerializer

import os
import joblib
import numpy as np
from datetime import datetime, timedelta


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        maintenance = self.get_object()
        maintenance.liters_since_last_service = 0
        maintenance.last_serviced_at = timezone.now()
        maintenance.save()
        return Response(MaintenanceSerializer(maintenance).data)
    
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']  # allows ?date=YYYY-MM-DD
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.isCompleted = True
        order.save()
        return Response(OrderSerializer(order).data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def predictions(request):
    MODEL_PATH = os.path.join(settings.BASE_DIR, "app_backend", "sales_model.pkl")

    if not os.path.exists(MODEL_PATH):
        return Response({'error': 'Model not trained yet'}, status=404)

    model = joblib.load(MODEL_PATH)

    predictions = []
    today = datetime.now()

    for i in range(1, 8):
        future_date = today + timedelta(days=i)
        day_of_week = future_date.weekday()
        day_of_month = future_date.day
        month = future_date.month
        is_weekend = 1 if day_of_week >= 5 else 0

        # Align with training features
        order_type_encoded = 0  # assume walk-in by default, or adjust dynamically

        features = np.array([[day_of_week, day_of_month, month, is_weekend, order_type_encoded]])
        predicted_revenue = model.predict(features)[0]

        predictions.append({
            'date': future_date.strftime('%b %d'),
            'day': future_date.strftime('%A'),
            'predicted_revenue': round(max(predicted_revenue, 0), 2),
        })

    return Response({
        'predictions': predictions,
        'model_info': {
            'algorithm': 'SGDRegressor',
            'features': ['day_of_week', 'day_of_month', 'month', 'is_weekend', 'order_type_encoded'],
            'trained_on': f"{Order.objects.count()} orders",
        }
    })