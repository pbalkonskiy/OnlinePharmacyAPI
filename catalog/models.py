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
    def in_stock(self) -> bool:
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

    DRUG_PRODUCTS = "DRUG"
    NUTRITIONAL_SUPPLEMENTS = "NUTR"
    MEDICAL_PRODUCTS = "MED"
    COSMETICS = "COSM"
    OTHER_PRODUCTS = "OTHER"
    HEALTHCARE_PRODUCTS = "HEALTH"
    MEDICAL_DEVICES = "DEV"

    CATEGORIES = [
        (DRUG_PRODUCTS, "Drug products"),
        (NUTRITIONAL_SUPPLEMENTS, "Nutritional supplements"),
        (MEDICAL_PRODUCTS, "Medical products"),
        (COSMETICS, "Cosmetics"),
        (OTHER_PRODUCTS, "Other products"),
        (HEALTHCARE_PRODUCTS, "Healthcare products"),
        (MEDICAL_DEVICES, "Medical devices"),
    ]
    title = models.CharField(choices=CATEGORIES, max_length=30, primary_key=True)    #стоит ли стаивть primary_key?, не будет ли потом проблем, т.к. строка?


    # parent_category = models.ForeignKey('self', on_delete=models.CASCADE,            #Was commented: to have parent_category we need to add unnecessary entries
    #                                     null=True, blank=True)                       #Decision: I created one more choise field for parent_category


    PARENT_CATEGORY = [
        ('MED DEV', 'Medical devices'),
        ('MED EQ', 'Medical equipment'),
        ('NONE', None)
    ]
    parent_title=models.CharField(choices=PARENT_CATEGORY, max_length=50, null=True, default='None')

    # @property                                                                         #commnted property because i suspect, that we need to save this field
    # def is_subcategory(self) -> bool:                                                 #in db, in admin panel it won't be displayed, but in db +'
    #     """Determines whether the category is a subcategory."""
    #     return True if self.parent_category else False

    class Meta:
        verbose_name = 'product category'
        verbose_name_plural = 'product categories'

    def __str__(self):
        return self.title
