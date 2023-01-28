from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    brand= models.CharField(max_length=100)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    expiration_date = models.DateField()
    barcode = models.CharField(max_length=50)
    amount = models.IntegerField()
    #in_stock = models.BooleanField()
    info = models.TextField()

    @property                                                                #need to finish, problem with in_stock
    def in_stock(self):
        in_stock = True if self.amount > 0 else False
        return in_stock



    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        default_related_name = 'product'


    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    info = models.TextField()

    class Meta:
        verbose_name ='manufacturer'
        verbose_name_plural ='manufacturers'


    def __str__(self):
        return self.name


class ProductType(models.Model):
    title_of_type = models.CharField(max_length=100) #All titles of types: Лекарственный препарат БАД Медицинское изделие Косметическое средство

    medical_device = models.ForeignKey(
        'MedicalDevice',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='product_type')

    class Meta:
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


    def __str__(self):
        return self.title_of_type

class MedicalDevice(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name ='type of medical device'
        verbose_name_plural ='types of medical devices'
