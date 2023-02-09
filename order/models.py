from decimal import Decimal
from datetime import timedelta

from django.db import models

from cart.models import Position
from order.constants import (DELIVERY_METHODS,
                             PAYMENT_METHODS,
                             PAYMENT_STATUS)


class Order(models.Model):
    positions = models.ManyToManyField(Position, related_name="order")
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=15)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=20)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20)
    address = models.TextField(null=True)
    post_index = models.IntegerField(null=True)

    @property
    def expiration_date(self) -> date:
        """
        Returns the expiration date of the order.
        The order will be automatically reset when the deadline for payment in the day expires.
        """
        return self.date + timedelta(days=1)

    @property
    def numb_of_positions(self) -> int:
        return self.positions.count()

    @property
    def total_price(self) -> Decimal:
        order_and_positions = self.positions.prefetch_related("product")  # simplified to only 3 requests
        amounts = [i.amount for i in order_and_positions.all()]
        prices = [i.product.price for i in order_and_positions.all()]
        return sum([i * j for i, j in zip(amounts, prices)])

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.id} order"
