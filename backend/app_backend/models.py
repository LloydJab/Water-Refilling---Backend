from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    # Add extra fields if needed
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Inventory(models.Model): 
    product_1 = models.IntegerField(default=50)  # Used 5 Liter Purified Water
    product_2 = models.IntegerField(default=50)  # New 5 Liter Purified Water
    product_3 = models.IntegerField(default=50)  # Used 10 Liter Purified Water
    product_4 = models.IntegerField(default=50)  # New 10 Liter Purified Water
    product_5 = models.IntegerField(default=50)  # Used 20 Liter Empty Container


class Order(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    date = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    customerName = models.CharField(max_length=255)
    orderType = models.CharField(max_length=50)
    deliveryAddress = models.TextField(blank=True, null=True)
    contactNumber = models.CharField(max_length=50, blank=True, null=True)
    items = models.JSONField()
    totalAmount = models.FloatField()
    paymentMethod = models.CharField(max_length=50, default='cash')
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.customerName}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField(default=50)
    category = models.CharField(max_length=50, default='refills')

    def __str__(self):
        return self.name
