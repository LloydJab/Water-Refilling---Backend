from django.db.models.signals import post_save
from django.dispatch import receiver
from app_backend.models import Order
from app_backend.ml import update_model_with_order

@receiver(post_save, sender=Order)
def update_model_on_order(sender, instance, created, **kwargs):
    if created:  # train on every new order
        update_model_with_order(instance)
