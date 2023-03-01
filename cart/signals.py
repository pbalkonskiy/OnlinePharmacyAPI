from django.db.models import signals
from django.dispatch import receiver

from users.models import Customer

from cart.models import Cart

from order.models import Order
from order.stripe import delete_stripe_product


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


@receiver(signals.post_save, sender=Order)
def delete_cart_positions(sender, instance, created, **kwargs):
    """
    Fills fresh created customer order M2M field with positions related to the cart ('cart' field).
    To remove items added to an order from the cart, the 'cart' field of a 'Position' is assigned as 'None'.
    """
    if created:
        positions = Cart.objects.get(id=instance.customer.id).positions.all()
        for position in positions:
            instance.positions.add(position)
            instance.save()
            position.cart = None
            position.save()


@receiver(signals.pre_delete, sender=Order)
def update_cart_on_order_delete(sender, instance, **kwargs):
    """
    Deactivates order instance on the Stripe side.
    Positions from the order are transported to the customer's cart.
    """
    if instance.stripe_order_id:
        delete_stripe_product(instance.stripe_order_id)

    cart = Cart.objects.get(id=instance.customer.id)
    for position in instance.positions.all():
        position.cart = cart
        position.save()
