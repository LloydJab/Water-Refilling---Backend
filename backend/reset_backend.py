from app_backend.models import Order, Product, Maintenance, Inventory

# 1. Delete all orders
Order.objects.all().delete()
print("Orders deleted:", Order.objects.count())

# 2. Reset product stock to 50
Product.objects.all().update(stock=50)
print("Products reset:", Product.objects.values('name', 'stock'))

# 3. Reset maintenance
Maintenance.objects.all().update(liters_since_last_service=0)
print("Maintenance reset")

# 4. Reset inventory
Inventory.objects.all().update(
    product_1=50, product_2=50, product_3=50,
    product_4=50, product_5=50
)
print("Inventory reset")

print("✓ Fresh state complete")