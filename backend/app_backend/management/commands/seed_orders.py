import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from app_backend.models import Order, Product

class Command(BaseCommand):
    help = "Seed 5000 random orders for testing"

    def handle(self, *args, **kwargs):
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR("No products found in DB. Seed products first."))
            return

        base_date = datetime(2026, 1, 1)
        names = ["Leifvash Cellan", "Lloyd Jabagat", "Rishi Zurita", "Charles Posadas"]

        orders_to_create = []
        for i in range(5000):
            order_date = base_date + timedelta(days=random.randint(0, 150))

            items = []
            total = 0
            for _ in range(random.randint(1, 3)):
                p = random.choice(products)
                qty = random.randint(1, 5)
                subtotal = p.price * qty
                total += subtotal
                items.append({
                    'productId': p.id,
                    'name': p.name,
                    'price': p.price,
                    'quantity': qty,
                    'subtotal': subtotal
                })

            orders_to_create.append(Order(
                id=str(1779800000000 + i),
                date=order_date.strftime('%m/%d/%Y'),
                time='12:00:00 PM',
                customerName=random.choice(names),
                orderType=random.choice(['walk-in', 'delivery']),
                items=items,
                totalAmount=round(total, 2),
                paymentMethod=random.choice(['cash', 'gcash']),
                isCompleted=True,
            ))

        # Bulk insert for speed
        Order.objects.bulk_create(orders_to_create)

        self.stdout.write(self.style.SUCCESS(f"✓ Seeded orders: {Order.objects.count()}"))
