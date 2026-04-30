from django.contrib import admin
from .models import Account
from .models import Inventory
# Register your models here.
admin.site.register(Account)
admin.site.register(Inventory)