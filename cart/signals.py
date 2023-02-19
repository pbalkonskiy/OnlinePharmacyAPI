from django.db.models import signals
from django.dispatch import receiver

from users.models import Customer
from cart.models import Cart


@receiver(signals.post_save, sender=Customer)
def create_customer_cart(sender, instance, created, **kwargs):
    """
    Creates a new record in the Customer table creates a new Cart
    with an id (pk) field corresponding to the id (pk) of the new Customer.
    """
    if created:
        cart = Cart.objects.create(id=instance.id)
        instance.cart = cart
        instance.save()


@receiver(signals.post_delete, sender=Customer)
def delete_customer_cart(sender, instance, **kwargs):
    """
    Deletes the Cart corresponding to the Customer.
    """
    Cart.objects.get(id=instance.id).delete()
