from users.models import CommonUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer

@receiver(post_save, sender=CommonUser)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)



