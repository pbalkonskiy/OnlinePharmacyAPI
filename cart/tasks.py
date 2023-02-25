from config.celery import app

from cart.models import Position


@app.task
def check_positions():
    """
    Checks all instances of the 'Position' model whose 'cart' field is null
    whether they have any connection with any object of the 'Order' model or not.

    The task is performed to clear the database of irrelevant and unused items.
    """

    positions_out_of_cart = Position.objects.filter(cart__isnull=True)
    for position in positions_out_of_cart:
        if position.order.exists():
            pass
        else:
            position.delete()
