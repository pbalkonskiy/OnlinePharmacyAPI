from datetime import timedelta

from config.celery import app

from order.models import Order


@app.task
def delete_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if not order.is_paid:
            order.delete()
    except Order.DoesNotExist:
        pass


@app.task
def check_order_payment_status(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.delivery_method and order.payment_method and order.payment_status and order.in_progress:
            delete_order.apply_async(args=(order.id,), eta=(order.date + timedelta(minutes=5)))
    except Order.DoesNotExist:
        pass
