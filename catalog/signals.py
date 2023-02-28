from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Product, Rating


@receiver(post_save, sender=Product)
def create_rating(sender, instance: Product, created, **kwargs):
    if created:
        Rating.objects.create(product=instance, slug=instance.slug)
