from datetime import timedelta

from django.utils import timezone
from config.celery import app

from order.models import Order


@app.task
def deactivate_unpaid_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if not order.is_paid:
            order.in_progress = False
    except Order.DoesNotExist:
        pass


@app.task
def deactivate_overdue_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if not order.is_paid and not order.is_closed:
            eta_time = order.receipt_datetime() + timedelta(hours=1)
            if timezone.now() > eta_time:
                order.delete()
    except Order.DoesNotExist:
        pass


@app.task
def check_order_payment_status(order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        pass
    else:
        if order.delivery_method == "Door delivery" and order.payment_method == "Prepayment" and order.in_progress:
            deactivate_unpaid_order.apply_async(args=(order.id,), eta=(order.created_at + timedelta(minutes=30)))
        pass
