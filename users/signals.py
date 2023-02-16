
from users.models import CommonUser, Employee
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver

from .models import Customer

@receiver(post_delete, sender=Customer)
def delete_customer(sender, instance, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Employee)
def create_employee(sender, instance,  **kwargs):
    instance.user.delete()
