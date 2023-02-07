from django.db import models
from django.template.defaultfilters import slugify

from catalog.managers import ProductInStockManager


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
    info = models.TextField()

    objects = models.Manager()
    in_stock = ProductInStockManager()

    @property
    def is_in_stock(self) -> bool:
        return True if self.amount > 0 else False

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
    info = models.TextField()

    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'

    def __str__(self):
        return self.name


class Category(models.Model):
    DRUG_PRODUCTS = "DRUG"
    NUTRITIONAL_SUPPLEMENTS = "NUTR"
    MEDICAL_PRODUCTS = "MED"
    COSMETICS = "COSM"
    OTHER_PRODUCTS = "OTHER"
    HEALTHCARE_PRODUCTS = "MED HEALTH"
    MEDICAL_DEVICES = "MED DEV"

    CATEGORIES = [
        (DRUG_PRODUCTS, "Drug products"),
        (NUTRITIONAL_SUPPLEMENTS, "Nutritional supplements"),
        (MEDICAL_PRODUCTS, "Medical products"),
        (COSMETICS, "Cosmetics"),
        (OTHER_PRODUCTS, "Other products"),
        (HEALTHCARE_PRODUCTS, "Healthcare products"),
        (MEDICAL_DEVICES, "Medical devices"),
    ]

    title = models.CharField(choices=CATEGORIES, max_length=30, )
    slug = models.SlugField(max_length=100, unique=True, editable=False, primary_key=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE,
                                        null=True, blank=True, related_name="subcategories")

    @property
    def is_subcategory(self) -> bool:
        """Determines whether the category is a subcategory."""
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
