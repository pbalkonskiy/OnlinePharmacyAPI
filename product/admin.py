from django.contrib import admin

from product.models import Product, Manufacturer, ProductType, MedicalDevice

# Register your models here.

admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(ProductType)
admin.site.register(MedicalDevice)