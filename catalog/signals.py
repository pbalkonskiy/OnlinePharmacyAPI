from django.db.models.signals import pre_save
from django.dispatch import receiver

from catalog.models import Category


@receiver(pre_save, sender=Category)
def my_handler(sender, instance: Category, **kwargs):
    print(kwargs, '->>>>>')
    if instance.title != 'MED':
        print('MED!')
        instance.parent_title = None
