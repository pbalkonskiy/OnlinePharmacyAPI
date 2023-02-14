
from users.models import CommonUser
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save
from django.dispatch import receiver

from .models import Customer

# @receiver(post_save, sender=CommonUser)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)

@receiver(post_delete, sender=Customer)
def delete_customer(sender, instance, **kwargs):
    instance.user.delete()


# @receiver(pre_save, sender=Customer)
# def change_email(sender, instance, **kwargs):
#     print(instance.user.email)
#     instance.email = instance.user.email
#
