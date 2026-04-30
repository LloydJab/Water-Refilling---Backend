from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Inventory(models.Model): 
    umbrella_cap = models.IntegerField()
    gallon = models.IntegerField()
    gallon_cap = models.IntegerField()
    cap_sticker = models.IntegerField()
    rock_salt = models.IntegerField()
    