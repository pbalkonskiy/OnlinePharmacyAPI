from django.db import models


class ProductInStockManager(models.Manager):
    """
    Manager for Product model. Returns all products in stock or out of stock.
    """
    def get_queryset(self):
        return super().get_queryset().filter(amount__gt=0)
