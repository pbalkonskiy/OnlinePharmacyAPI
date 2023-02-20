from django.db import models

from catalog.models import Product


class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='positions', null=True, blank=True)
    amount = models.IntegerField(default=1)

    @property
    def price(self):
        return self.product.price * self.amount

    class Meta:
        verbose_name_plural = 'positions'
        verbose_name = 'position'
        default_related_name = 'position'

    def __str__(self):
        try:
            return f"{self.product.title} -- ID {self.cart.id}"
        except AttributeError:
            return f"{self.product.title} -- in order."


class Cart(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @property
    def numb_of_positions(self) -> int:
        return self.positions.count()

    @property
    def total_price(self):  # don't use price in position cause takes many requests
        cart_and_positions = self.positions.select_related('product')  # use select_related just for one request
        amounts = [i.amount for i in cart_and_positions.all()]
        prices = [i.product.price for i in cart_and_positions.all()]
        return sum([i * j for i, j in zip(amounts, prices)])

    class Meta:
        verbose_name_plural = 'carts'
        verbose_name = 'cart'

    def __str__(self):
        return f"{self.id} cart"
