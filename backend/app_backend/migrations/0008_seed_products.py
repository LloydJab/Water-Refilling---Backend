from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model('app_backend', 'Product')
    
    initial_products = [
        {'id': 1, 'name': 'Used 5 Liter\nPurified Water', 'price': 5.0, 'stock': 50, 'category': 'refills'},
        {'id': 2, 'name': 'New 5 Liter\nPurified Water', 'price': 20.0, 'stock': 50, 'category': 'refills'},
        {'id': 3, 'name': 'Used 10 Liter\nPurified Water', 'price': 80.0, 'stock': 50, 'category': 'refills'},
        {'id': 4, 'name': 'New 10 Liter\nPurified Water', 'price': 160.0, 'stock': 50, 'category': 'refills'},
        {'id': 5, 'name': 'Used 20 Liter\nEmpty Container', 'price': 20.0, 'stock': 50, 'category': 'refills'},
        {'id': 6, 'name': 'New 20 Liter\nEmpty Container', 'price': 350.0, 'stock': 50, 'category': 'refills'},
    ]
    
    for prod_data in initial_products:
        Product.objects.update_or_create(id=prod_data['id'], defaults=prod_data)

def reverse_seed_products(apps, schema_editor):
    Product = apps.get_model('app_backend', 'Product')
    Product.objects.filter(id__in=[1, 2, 3, 4, 5, 6]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('app_backend', '0007_product'),
    ]

    operations = [
        migrations.RunPython(seed_products, reverse_seed_products),
    ]
