from django.db import models
from django.template.defaultfilters import slugify

from catalog.managers import ProductInStockManager
from catalog.constants import CATEGORIES


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    brand = models.CharField(max_length=100)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    expiration_date = models.DateField()
    addition_date = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=50)
    amount = models.IntegerField()
    info = models.TextField(blank=True)

    # Product model managers
    objects = models.Manager()
    in_stock = ProductInStockManager()

    @property
    def is_in_stock(self) -> bool:
        return True if self.amount > 0 else False

    @property
    def url(self) -> str:
        """
        Returns product URL for SimpleProductSerializer.
        """
        try:
            assert self.slug
        except AttributeError:
            raise Exception("Product error. Tried to get product URL, while 'slug' field wasn't defined.")
        return "http://127.0.0.1:8000/catalog/{}".format(self.slug)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        default_related_name = 'product'
        ordering = ["addition_date"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    info = models.TextField(blank=True)

    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(choices=CATEGORIES, max_length=30)
    slug = models.SlugField(max_length=100, unique=True, editable=False, primary_key=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                        null=True, blank=True, related_name="subcategories")

    @property
    def is_subcategory(self) -> bool:
        """
        Determines whether the category is a subcategory.
        """
        return True if self.parent_category else False

    @property
    def parent_title(self):
        return self.parent_category.title if self.parent_category else None

    class Meta:
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Rating(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='rating')
    rating_set = models.JSONField(default=dict, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True, editable=False)

    @property
    def average_rating(self):
        ratings = [rating for rating in self.rating_set.values()]
        return sum(ratings) / len(ratings) if len(ratings) > 0 else float(0)
