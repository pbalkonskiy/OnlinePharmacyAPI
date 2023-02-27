from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from catalog.models import Product, Raiting


@receiver(post_save, sender=Product)
def create_rating(sender, instance: Product, created, **kwargs):
    if created:
        Raiting.objects.create(product=instance, slug=instance.slug)

