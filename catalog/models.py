from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    brand = models.CharField(max_length=100)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    expiration_date = models.DateField()
    addition_date = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    amount = models.IntegerField()
    info = models.TextField()

    @property
    def in_stock(self):
        in_stock = True if self.amount > 0 else False
        return in_stock

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        default_related_name = 'product'
        ordering = ["addition_date"]

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    info = models.TextField()

    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORIES = [
        ("DRUG", "Drug products"),
        ("NUTR", "Nutritional supplements"),
        ("MED", "Medical products"),
        ("COSMETICS", "Cosmetics"),
        ("OTHER", "Other products"),
        ("MED / HEALTH", "Healthcare product"),
        ("MED / DEVICE", "Medical devices"),
    ]

    title = models.CharField(choices=CATEGORIES, max_length=25)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                        null=True, blank=True)

    @property
    def is_subcategory(self):
        return True if self.parent_category else False

    class Meta:
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.title
