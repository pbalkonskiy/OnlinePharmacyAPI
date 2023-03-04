from django.db.models.signals import post_save
from django.dispatch import receiver

from order.models import Order


# @receiver(post_save, sender=Order)
# def change_delivery_status(sender, instance: Order, created, **kwargs):
#     if instance.is_paid and instance.delivery_method == "Door delivery" and instance.delivery_method == 'Without action':
#         instance.delivery_method = 'Packed in stock'
#         instance.save()
