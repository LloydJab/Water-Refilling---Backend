from django.contrib import admin
from .models import Account, Inventory, Order, Product

# Register your models here.
admin.site.register(Account)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Product)