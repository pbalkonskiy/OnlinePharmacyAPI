from django.db import models

from catalog.models import Product


class Product_template(models.Model):
    product = models.ForeignKey(Product, related_name='prod_in_cart', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    @property
    def price(self):
        return self.product.price


    class Meta:
        verbose_name_plural = 'product templates'
        verbose_name = 'product template'

    def __str__(self):
        return self.product.title


class Cart(models.Model):
    products = models.ManyToManyField(Product_template, related_name='cart')

    @property
    def numb_of_positions(self)->int:
        return self.products.count()

    @property
    def total_price(self):
        return sum([p.price*p.amount for p in self.products.all()])

    status = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'carts'
        verbose_name = 'cart'

    def __str__(self):
        return f"{self.id} cart"

